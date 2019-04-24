from flask import Flask

from newsapi.api import api


app = Flask(__name__,
            static_folder="../../frontend/static",
            template_folder="../../frontend")


# @app.route("/")
# def hello():
#     response = {'msg': 'Hello World'}
#     return jsonify(response)


def create_app(app_name='NEWS'):
    app = Flask(app_name)
    app.register_blueprint(api, url_prefix="/")

    return app


