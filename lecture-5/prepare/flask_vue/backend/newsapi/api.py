from flask import Blueprint, jsonify, request, render_template
from .models import NewsExtract


api = Blueprint('news', __name__,
                static_folder="./../../frontend/news-spa/static",
                template_folder="../../frontend/news-spa")


# @api.route("/")
@api.route('/', defaults={'path': ''})
@api.route('/<path:path>')
def news():
    # response = {'msg': "Hello world"}
    #
    # return jsonify(response)
    return render_template("index.html")
