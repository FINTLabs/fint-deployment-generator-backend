import yaml

from github import ContentFile

ONE_PASSWORD_ITEM = ""
INGRESS = ""
PG_USER = ""
KAFKA = ""
DEPLOYMENT = ""


def from_kustomize_to_json(kustomize_encoded_content: list[ContentFile]) -> dict:
    kustomize_json = {}
    for x in kustomize_encoded_content:
        content = dict(yaml.safe_load(x.decoded_content))
        kind = content.get("kind")
        kustomize_json[kind] = content
    return kustomize_json


class FlaisConverter:
    def __init__(self):
        pass

    def kustomize_content_to_flais(self):
        pass

    def one_password_item(self, one_password: dict):
        # OnePasswordItem
        pass

    def ingress(self, ingress: dict):
        # IngressRoute
        pass

    def pg_user(self, pg_user: dict):
        # PGUser
        pass

    def kafka(self, kafka: dict):
        # KafkaUserAndAcl
        pass

    def deployment(self, deployment: dict):
        # deployment
        pass
