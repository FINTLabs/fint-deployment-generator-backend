import yaml

from github import ContentFile
from resources import flais_default

ONE_PASSWORD = ""
INGRESS = ""
PG_USER = ""
KAFKA = ""
DEPLOYMENT = ""

FLAIS_ONE_PASSWORD = "onePassword"
FLAIS_INGRESS = "ingress"
FLAIS_PG_USER = "database"
FLAIS_KAFKA = "kafka"


def from_kustomize_to_json(kustomize_encoded_content: list[ContentFile]) -> dict:
    kustomize_json = {}
    for x in kustomize_encoded_content:
        content = dict(yaml.safe_load(x.decoded_content))
        kind = content.get("kind")
        kustomize_json[kind] = content
    return kustomize_json


class FlaisConverter:
    def __init__(self):
        self.key_to_function_mapping = {
            DEPLOYMENT: (self.deployment, "deployment"),
            INGRESS: (self.ingress, FLAIS_INGRESS),
            PG_USER: (self.pg_user, FLAIS_PG_USER),
            KAFKA: (self.kafka, FLAIS_KAFKA),
            ONE_PASSWORD: (self.one_password_item, FLAIS_ONE_PASSWORD)
        }

    def kustomize_content_to_flais(self, kustomize_content: dict):
        flais = flais_default
        for key, value in kustomize_content.items():
            if key in self.key_to_function_mapping:
                process_func, target_key = self.key_to_function_mapping[key]
                flais["spec"][target_key] = process_func(value, flais)

    def one_password_item(self, one_password: dict):
        # OnePasswordItem
        pass

    def ingress(self, kustomize_ingress: dict, flais: dict):
        pass

    def pg_user(self, pg_user: dict, flais: dict):
        # PGUser
        pass

    def kafka(self, kafka: dict, flais: dict):
        # KafkaUserAndAcl
        pass

    def deployment(self, deployment: dict, flais: dict):
        print("CONFIGURING DEPLOYMENT")
        pass
