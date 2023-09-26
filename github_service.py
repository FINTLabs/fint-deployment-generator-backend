import requests

FLAIS_FILE_NAME = "flais.yaml"
FLAIS_FILE_URL = "https://raw.githubusercontent.com/FINTLabs/{repo_name}/{branch}/kustomize/base/" + FLAIS_FILE_NAME


class GithubService:
    def get_flais_content(self, request):
        repo_name = "" if "repo" not in request else request["repo"]
        branch = "main" if "branch" not in request else request["branch"]

        search_url = FLAIS_FILE_URL.format(repo_name=repo_name, branch=branch)
        response = requests.get(search_url)

        if response.status_code == 200:
            return response.content
        else:
            return None
