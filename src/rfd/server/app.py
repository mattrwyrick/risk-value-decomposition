import os
import logging
from flask import Flask, render_template, request, redirect, url_for

from rfd.settings import SRC_DIR
from rfd.server.views.home import view as home_view
from rfd.server.views.decomposition import view as decomposition_view
from rfd.server.views.test import view as test_view



HOST = "127.0.0.1"
PORT = 5500
app = Flask(__name__)

info_handler = logging.FileHandler(os.path.join(SRC_DIR, 'riskdecomposition.com.server.log'))
info_handler.setLevel(logging.INFO)  # Only log INFO level and above
info_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
info_handler.setFormatter(info_formatter)
app.logger.addHandler(info_handler)


@app.route('/', methods=["GET", "POST"])
def index():
    return home_view(request, {"title": "Risk Factor Decomposition"})


@app.route('/decomposition', methods=["GET", "POST"])
def decomposition():
    return decomposition_view(request, {"title": "Risk Factor Decomposition"})

@app.route('/test', methods=["GET", "POST"])
def test():
    return test_view(request, {"title": "Risk Factor Decomposition"})


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
