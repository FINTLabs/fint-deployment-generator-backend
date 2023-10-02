import re

from resources import flais_default
from constants import FINTLABS_NO, KUBERNETES_IO

MEMORY_UNIT_MEBIBYTE = "Mi"
MEMORY_UNIT_GIBIBYTE = "Gi"

BACKEND_COMPONENT = "backend"


def from_flais_to_json(flais: dict):
    metadata = flais.get("metadata")
    labels = metadata.get("labels")

    name = metadata.get("name")
    component = labels.get("app.kubernetes.io/component")
    part_of = labels.get("app.kubernetes.io/part-of")
    team = labels.get("fintlabs.no/team")

    del flais["metadata"]
    del flais["apiVersion"]
    del flais["kind"]

    flais["component"] = component
    flais["partOf"] = part_of
    flais["team"] = team
    flais["name"] = name

    return flais


class FlaisUpdater:
    """A class responsible for updating Flais objects."""

    def translate_request_to_flais(self, flais_request):
        """Translates a request to the Flais object by updating its fields."""
        flais = dict(flais_default)

        self.__update_metadata(flais_request, flais)
        self.__update_spec(flais_request, flais)
        self.__set_jvm_arguments(flais_request, flais)
        flais["spec"]["image"] = f"ghcr.io/fintlabs/{flais_request['name']}:latest"

        return flais

    @staticmethod
    def __update_metadata(flais_request, flais):
        """Updates the metadata of the Flais object."""
        metadata = flais["metadata"]
        metadata["name"] = flais_request["name"]

        labels = metadata["labels"]
        labels[f"{KUBERNETES_IO}/name"] = flais_request["name"]
        labels[f"{KUBERNETES_IO}/instance"] = f"{flais_request['name']}_{{org_dash}}"
        labels[f"{KUBERNETES_IO}/component"] = flais_request["component"]
        labels[f"{KUBERNETES_IO}/part-of"] = flais_request["partOf"]
        labels[f"{FINTLABS_NO}/team"] = flais_request["team"]

    @staticmethod
    def __update_spec(flais_request, flais):
        """Updates the spec of the Flais object."""
        if "spec" not in flais_request:
            return

        for spec_key, spec_value in enumerate(flais_request["spec"]):
            flais["spec"][spec_key] = spec_value

    def __set_jvm_arguments(self, flais_request, flais):
        """Sets the JVM arguments for the Flais object if the component is a backend."""
        if flais_request["component"] != BACKEND_COMPONENT:
            return

        flais["spec"].setdefault("env", []).append({
            "name": "JAVA_TOOL_OPTIONS",
            "value": self.__generate_jvm_arguments(flais_request, flais)
        })

    @staticmethod
    def __generate_jvm_arguments(flais_request, flais):
        """Generates JVM arguments based on the memory limits."""
        limit = flais_request.get("resources", {}).get("limits", {}).get("memory", None)
        if limit is None:
            limit = flais["spec"]["resources"]["limits"]["memory"]
            print(limit)

        match = re.match(r"(\d+)(Mi|Gi)", limit)
        if not match:
            raise ValueError("Unsupported memory unit in request_limit")

        value, unit = match.groups()
        total_memory = int(value) / (1024.0 if unit == "Mi" else 1.0)

        if not (total_memory <= 250):
            raise ValueError("Memory out of the 250GB range")

        if total_memory <= 10:
            overhead_percentage = 0.3 - 0.01 * (total_memory - 1)
        else:
            overhead_percentage = 0.2 - 0.0004 * (total_memory - 10)

        heap_memory = total_memory * (1 - overhead_percentage)
        recommended_value = int(heap_memory * (1024 if unit == "Mi" else 1))
        unit = unit[0]  # Convert 'Mi' to 'M' and 'Gi' to 'G'

        return f"-XX:+ExitOnOutOfMemoryError -Xmx{recommended_value}{unit} -verbose:gc"
