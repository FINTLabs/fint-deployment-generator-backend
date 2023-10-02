from github import Github, UnknownObjectException
from app.services.flais_updater import from_flais_to_json, FlaisUpdater
import os
import yaml

FINTLABS = "FINTLabs"
KUSTOMIZE_BASE_PATH = "kustomize/base"
FLAIS_PATH = os.path.join(KUSTOMIZE_BASE_PATH, "flais.yaml")


class GithubService:
    def __init__(self, flais_updater: FlaisUpdater):
        self.github = Github(os.environ.get("fint.github.token"))
        self.flais_updater = flais_updater

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

    def create_pull_request(self, github_request: dict):
        try:
            new_branch_name = "Deployment-Generator"
            repo, branch_name = self.__get_repo_and_branch_name(github_request)

            base_branch = repo.get_branch(branch_name)
            repo.create_git_ref(ref=f"refs/heads/{new_branch_name}", sha=base_branch.commit.sha)
            contents = repo.get_contents(FLAIS_PATH, ref=new_branch_name)

            repo.update_file(
                contents.path,
                "Updated by flais generator",
                self.flais_updater.translate_request_to_flais(github_request),
                contents.sha, branch=new_branch_name
            )

            repo.create_pull(
                title="Deployment Generated Flais",
                body="Flais updated by the Deployment generator",
                head=new_branch_name,
                base=branch_name
            )
        except Exception as error:
            raise error
