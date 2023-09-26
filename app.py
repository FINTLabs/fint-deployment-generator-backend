from flask import Flask, request, jsonify, abort
from flais_updater import FlaisUpdater
from github_service import GithubService


app = Flask(__name__)
flais_updater = FlaisUpdater()
github_service = GithubService()

@app.route('/deployment', methods=['POST'])
def download_flais_application():
    flais = flais_updater.translate_request_to_flais(request.get_json())
    return jsonify(flais)

@app.route('/github/check-flais', methods=['POST'])
def check_flais():
    repo_name = request.get_json()["repo"]
    if github_service.flais_exist(repo_name):
        return jsonify(github_service.)
    else:
        abort(404)


if __name__ == '__main__':
    app.run()
