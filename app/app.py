from flask import Flask
from .routes import deployment, github

app = Flask(__name__)

app.register_blueprint(deployment)
app.register_blueprint(github)

if __name__ == '__main__':
    app.run()
