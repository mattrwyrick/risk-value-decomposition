
from flask import Flask, render_template, request, redirect, url_for

from rfd.server.views.home import view as home_view
from rfd.server.views.decomposition import view as decomposition_view


HOST = "127.0.0.1"
PORT = 5000
APP = Flask(__name__)


@APP.route('/', methods=["GET", "POST"])
def index():
    return home_view(request, {"title": "Risk Factor Decomposition"})


@APP.route('/decomposition', methods=["GET", "POST"])
def index():
    return home_view(request, {"title": "Risk Factor Decomposition"})


if __name__ == '__main__':
    APP.run(host=HOST, port=PORT, debug=True)
