
from flask import Flask, render_template, request, redirect, url_for

from rfd.server.views.home import view as home_view


HOST = "127.0.0.1"
PORT = 8000
APP = Flask(__name__)


@APP.route('/')
def index():
    return render_template('index.html')


@APP.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    APP.run(host=HOST, port=PORT, debug=True)
