from github import Github, UnknownObjectException
from services.flais_updater import from_flais_to_json
import os
import yaml

FINTLABS = "FINTLabs"
KUSTOMIZE_BASE_PATH = "kustomize/base"
FLAIS_PATH = os.path.join(KUSTOMIZE_BASE_PATH, "flais.yaml")


class GithubService:
    def __init__(self):
        self.github = Github(os.environ.get("fint.github.token"))

    def __get_repo_and_branch_name(self, github_request: dict):
        repo_name = github_request.get("repo", "")
        repo_path = os.path.join(FINTLABS, repo_name)
        return self.github.get_repo(repo_path), github_request.get("branch", "main")

    def __get_repo_content(self, github_request: dict, path: str):
        """Utility method to fetch repo content."""
        repo, branch = self.__get_repo_and_branch_name(github_request)
        try:
            content = repo.get_contents(path, ref=branch)
            if isinstance(content, list):
                return content

            return content.decoded_content

        except UnknownObjectException:
            return None

    def flais_exists(self, github_request: dict):
        return bool(self.__get_repo_content(github_request, FLAIS_PATH))

    def get_flais(self, github_request: dict):
        content = self.__get_repo_content(github_request, FLAIS_PATH)
        if content:
            return from_flais_to_json(yaml.safe_load(content))
        return None

    def get_kustomize_encoded_content(self, github_request: dict):
        return self.__get_repo_content(github_request, KUSTOMIZE_BASE_PATH)

    def repo_exists(self, github_request: dict) -> bool:
        try:
            repo_name = github_request.get("repo", "")
            repo_path = os.path.join(FINTLABS, repo_name)
            self.github.get_repo(repo_path)
            return True
        except UnknownObjectException:
            return False

    def kustomize_exists(self, github_request: dict) -> bool:
        return bool(self.__get_repo_content(github_request, KUSTOMIZE_BASE_PATH))
