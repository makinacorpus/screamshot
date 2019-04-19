from flask import Flask, render_template, request, send_from_directory, url_for, redirect


app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/close')
def close():
    shutdown_server()
    return 'Server shutting down...'

