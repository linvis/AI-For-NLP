# from newsapi.application import create_app
#
#
# if __name__=='__main__':
#     app = create_app()
#     app.run()

from flask import Flask, render_template
from flask_cors import CORS
app = Flask(__name__,
            static_folder="../frontend/dist/static",
            template_folder="../frontend/dist")

CORS(app)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")
