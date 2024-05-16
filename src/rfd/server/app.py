
from flask import Flask, render_template, request, redirect, url_for

from rfd.server.views.home import view as home_view


HOST = "127.0.0.1"
PORT = 5000
APP = Flask(__name__)


@APP.route('/', methods=["GET", "POST"])
def index():
    return home_view(request, {"title": "Risk Decomp"})


if __name__ == '__main__':
    APP.run(host=HOST, port=PORT, debug=True)
