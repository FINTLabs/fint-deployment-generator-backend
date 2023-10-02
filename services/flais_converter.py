import yaml

from github import ContentFile
from resources import flais_default
from services.github_service import GithubService

ONE_PASSWORD = ""
INGRESS = ""
PG_USER = ""
KAFKA = ""
DEPLOYMENT = "Deployment"

FLAIS_ONE_PASSWORD = "onePassword"
FLAIS_INGRESS = "ingress"
FLAIS_PG_USER = "database"
FLAIS_KAFKA = "kafka"


class FlaisConverter:
    def __init__(self, github_service: GithubService):
        self.github_service = github_service

        self.key_to_function_mapping = {
            INGRESS: (self.ingress, FLAIS_INGRESS),
            PG_USER: (self.pg_user, FLAIS_PG_USER),
            KAFKA: (self.kafka, FLAIS_KAFKA),
            ONE_PASSWORD: (self.one_password_item, FLAIS_ONE_PASSWORD)
        }

    def get_flais_from_kustomize(self, github_request: dict):
        list_of_kustomize_encoded_content = self.github_service.get_kustomize_encoded_content(github_request)
        decoded_content = self.__decode_kustomize_enconded_content(list_of_kustomize_encoded_content)
        return self.kustomize_content_to_flais(decoded_content)

    @staticmethod
    def __decode_kustomize_enconded_content(list_of_kustomize_encoded_content: list[ContentFile]) -> dict:
        decoded_kustomize_content = {}
        for enconded_content in list_of_kustomize_encoded_content:
            decoded_content = yaml.safe_load(enconded_content.decoded_content)
            kind = decoded_content.get("kind")
            decoded_kustomize_content[kind] = decoded_content
        return decoded_kustomize_content

    def kustomize_content_to_flais(self, kustomize_content: dict) -> dict:
        flais = flais_default

        self.update_flais_from_kustomize_deployment(kustomize_content.get(DEPLOYMENT, None), flais)

        for key, value in kustomize_content.items():
            if key in self.key_to_function_mapping:
                process_func, target_key = self.key_to_function_mapping[key]
                flais["spec"][target_key] = process_func(value)

    def update_flais_from_kustomize_deployment(self, deployment: dict, flais: dict):
        if deployment is None:
            return

        self.__update_metadata_from_deployment(deployment, flais)
        pass

    def __update_metadata_from_deployment(self, deployment, flais):
        project_name = deployment.get("metadata").get("name")
        metadata = flais.get("metadata")
        labels = metadata.get("labels")

        metadata["name"] = project_name

        pass

    def one_password_item(self, one_password):
        return one_password["spec"]

    def ingress(self, kustomize_ingress: dict, flais: dict):
        pass

    def pg_user(self, pg_user: dict):
        return pg_user["spec"]

    def kafka(self, kafka: dict):
        # KafkaUserAndAcl
        pass

    def config_map(self, config_map: dict):
        data = config_map.get("data")
        env = []

        for key, value in data.items():
            env.append({
                key: value
            })

        return env

    def deployment(self, deployment: dict, flais: dict):
        print("CONFIGURING DEPLOYMENT")
        pass
