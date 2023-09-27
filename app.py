from flask import Flask, request, jsonify, abort
from flais_updater import FlaisUpdater
from github_service import GithubService
import yaml


app = Flask(__name__)
flais_updater = FlaisUpdater()
github_service = GithubService()


@app.route('/deployment', methods=['POST'])
def download_flais_application():
    flais = flais_updater.translate_request_to_flais(request.get_json())
    return jsonify(flais)


@app.route('/github/check-flais', methods=['POST'])
def check_flais():
    repo_name = request.get_json()
    flais_content = github_service.get_flais_content(repo_name)

    if flais_content is not None:
        return yaml.safe_load(flais_content)
    else:
        abort(404)

@app.route('/github/check-kustomize', methods=['POST'])
def check_kustomize():
    repo_name = request.get_json()

    kustomize = github_service.get_kustomize(repo_name)

    if kustomize is True:
        return "true"
    else:
        return abort(404)

if __name__ == '__main__':
    app.run()
