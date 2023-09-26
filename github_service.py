import requests

FLAIS_FILE_NAME = "flais.yaml"
FLAIS_FILE_URL = "https://github.com/FINTLabs/{repo_name}/kustomize/base/" + FLAIS_FILE_NAME


class GithubService:
    def get_flais_content(self, repo_name):
        search_url = FLAIS_FILE_URL.format(repo_name=repo_name)
        response = requests.get(search_url)

        if response.status_code == 200:
            return response.content
        else:
            return False
