import yaml
import re

BASE_YAML_PATH = "resources/flais-base.yaml"
LABEL_PREFIX_KUBERNETES = "app.kubernetes.io"
LABEL_PREFIX_FINTLABS = "fintlabs.no"
MEMORY_UNIT_MEBIBYTE = "Mi"
MEMORY_UNIT_GIBIBYTE = "Gi"
BACKEND_COMPONENT = "backend"


class FlaisUpdater:
    def translate_request_to_flais(self, flais_request):
        """Translates a request to a Flais object by updating its fields."""
        with open(BASE_YAML_PATH, "r") as file:
            flais = yaml.safe_load(file)

        self.__update_metadata(flais_request, flais)
        self.__update_spec(flais_request, flais)
        return flais

    @staticmethod
    def __update_metadata(flais_request, flais):
        metadata = flais["metadata"]
        metadata["name"] = flais_request["name"]
        metadata["namespace"] = flais_request["orgId"]

        labels = metadata["labels"]
        labels[f"{LABEL_PREFIX_KUBERNETES}/name"] = flais_request["name"]
        labels[f"{LABEL_PREFIX_KUBERNETES}/instance"] = f"{flais_request['name']}_{flais_request['orgId']}"
        labels[f"{LABEL_PREFIX_KUBERNETES}/component"] = flais_request["component"]
        labels[f"{LABEL_PREFIX_KUBERNETES}/part-of"] = flais_request["partOf"]
        labels[f"{LABEL_PREFIX_FINTLABS}/team"] = flais_request["team"]
        labels[f"{LABEL_PREFIX_FINTLABS}/org-id"] = flais_request["orgId"]

    def __update_spec(self, flais_request, flais):
        spec = flais["spec"]
        spec["port"] = flais_request["port"]
        spec["orgId"] = flais_request["orgId"]
        spec["resources"] = flais_request["resources"]
        spec["image"] = f"ghcr.io/fintlabs/{flais_request['name']}:latest"

        self.__update_spec_value("prometheus", flais_request, spec)
        self.__update_spec_value("onePassword", flais_request, spec)
        self.__update_spec_value("env", flais_request, spec)
        self.__update_spec_value("database", flais_request, spec)
        self.__update_spec_value("envFrom", flais_request, spec)
        self.__update_spec_value("ingress", flais_request, spec)
        self.__update_spec_value("kafka", flais_request, spec)
        self.__update_spec_value("url", flais_request, spec)

        self.__set_jvm_arguments(flais_request, spec)

    @staticmethod
    def __delete_value_if_not_present(value, flais_request, spec):
        """Deletes the value from the spec if it's not present in the request."""
        if value not in flais_request:
            del spec[value]
            return True
        return False

    def __update_spec_value(self, name, flais_request, spec):
        if self.__delete_value_if_not_present(name, flais_request, spec):
            return
        spec[name] = flais_request[name]

    @staticmethod
    def __generate_jvm_arguments(flais_request):
        """Generates JVM arguments based on the memory limits."""
        # Extract memory value and its unit (Mi/Gi) from the request.
        limit = flais_request["resources"]["limits"]["memory"]
        match = re.match(r"(\d+)(Mi|Gi)", limit)
        if not match:
            raise ValueError("Unsupported memory unit in request_limit")

        value, unit = match.groups()
        total_memory = int(value) / (1024.0 if unit == "Mi" else 1.0)  # Convert Mi to GB or leave Gi as is

        if not (1 <= total_memory <= 250):
            raise ValueError("Memory out of the 1GB-250GB range")

        # Calculate overhead percentage
        if total_memory <= 10:
            overhead_percentage = 0.3 - 0.01 * (total_memory - 1)
        else:
            overhead_percentage = 0.2 - 0.0004 * (total_memory - 10)

        # Calculate heap memory and the recommended value
        heap_memory = total_memory * (1 - overhead_percentage)
        recommended_value = int(heap_memory * (1024 if unit == "Mi" else 1))
        unit = unit[0]  # Convert 'Mi' to 'M' and 'Gi' to 'G'

        # Construct the JVM arguments string
        return f"-XX:+ExitOnOutOfMemoryError -Xmx{recommended_value}{unit} -verbose:gc"

    def __set_jvm_arguments(self, flais_request, spec):
        if flais_request["component"] != BACKEND_COMPONENT:
            return

        spec.setdefault("env", []).append({
            "name": "JAVA_TOOL_OPTIONS",
            "value": self.__generate_jvm_arguments(flais_request)
        })
