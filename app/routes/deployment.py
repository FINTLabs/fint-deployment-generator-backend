from flask import Blueprint, request, jsonify
from app.services import FlaisUpdater

deployment = Blueprint('deployment', __name__)
flais_updater = FlaisUpdater()


@deployment.route('/deployment', methods=['POST'])
def download_flais_application():
    flais = flais_updater.translate_request_to_flais(request.get_json())
    return jsonify(flais)
