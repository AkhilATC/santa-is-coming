from flask import Flask
from controllers.santa_controller import santa

app = Flask(__name__,template_folder="template")


def create_app():
    app.config.update({"code": "dededede"})
    app.register_blueprint(santa)
    return app
