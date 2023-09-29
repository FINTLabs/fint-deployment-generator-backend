from flask import Blueprint, request, jsonify
from services import GithubService

github = Blueprint('github', __name__)
github_service = GithubService()


@github.route('/github/check-repository', methods=['POST'])
def check_repository():
    github_request = request.get_json()
    if github_service.repo_exists(github_request):
        return jsonify(status="success", message="Repository exists"), 200
    else:
        return jsonify(status="error", message="Repository not found"), 404


@github.route('/github/get-flais', methods=['POST'])
def check_flais():
    github_request = request.get_json()
    flais_content = github_service.get_flais(github_request)

    if flais_content is not None:
        return jsonify(status="success", content=flais_content), 200
    else:
        return jsonify(status="error", message="Flais file not found"), 404


@github.route('/github/check-kustomize', methods=['POST'])
def check_kustomize():
    github_request = request.get_json()

    if github_service.kustomize_exists(github_request):
        return jsonify(status="success", message="Kustomize exists"), 200
    else:
        return jsonify(status="error", message="Kustomize not found"), 404


@github.route('/github/get-kustomize', methods=['POST'])
def get_kustomize():
    github_request = request.get_json()
    if github_service.repo_exists(github_request) is True:
        return github_service.get_flais(github_request)
    else:
        return jsonify(status="error", message="Repo doesnt exist"), 404