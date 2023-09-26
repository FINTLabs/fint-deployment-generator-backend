from flask import Flask, request, jsonify
from flais_updater import FlaisUpdater

app = Flask(__name__)
flais_updater = FlaisUpdater()


@app.route('/deployment', methods=['POST'])
def download_flais_application():
    flais = flais_updater.translate_request_to_flais(request.get_json())
    return jsonify(flais)


if __name__ == '__main__':
    app.run()
