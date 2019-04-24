import logging

from flask import Flask, render_template, request, send_from_directory, url_for, redirect


logger = logging.getLogger('werkzeug')
logger.setLevel(logging.ERROR)


app = Flask(__name__, static_url_path='')


@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))


@app.route('/other')
def otherPage():
    return redirect(url_for('static', filename='other.html'))


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/close')
def close():
    shutdown_server()
    return 'Server shutting down...'


if __name__ == '__main__':
    app.run()
