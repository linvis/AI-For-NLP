from flask import Flask
from flask import render_template


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World"


@app.route("/hello/")
@app.route("/hello/<name>")
def show_hello(name=None):
    return render_template('hello.html', name=name)
