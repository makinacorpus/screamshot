import logging
from functools import wraps

from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    url_for,
    redirect,
    jsonify,
    make_response,
)
from flask.wrappers import Response

from jwt import encode, decode

# logger = logging.getLogger('werkzeug')
# logger.setLevel(logging.ERROR)


app = Flask(__name__, static_url_path="")
app.config["SECRET_KEY"] = "8OpElGqFyUritA-IQPYg8jMYkUHjRSjBmtkLirWsktg"
app.config[
    "TOKEN"
] = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFraW5hIn0.jUTxi6c2-o3nHJ6Bq7zRXFoKixUyYetgPX3cToOayiA"


class OwnResponse(Response):
    def __init__(
        self,
        response=None,
        status=None,
        headers=None,
        mimetype=None,
        content_type=None,
        direct_passthrough=False,
    ):
        super().__init__(
            response,
            status,
            {"token": app.config["TOKEN"]},
            mimetype,
            content_type,
            direct_passthrough,
        )


@app.route("/")
def index():
    return redirect(url_for("static", filename="index.html"))


@app.route("/other")
def other_page():
    return redirect(url_for("static", filename="other.html"))


def shutdown_server():
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


@app.route("/close")
def close():
    shutdown_server()
    return "Server shutting down..."


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("token")
        auth = request.authorization
        if not token and (
            not auth or auth.username != "makina" or auth.password != "makina"
        ):
            return make_response(
                "Missing token",
                401,
                {"WWW-Authenticate": 'Basic realm="Login Required"'},
            )
        if not auth:
            try:
                data = decode(token, app.config["SECRET_KEY"])
            except:
                return make_response("Invalid token", 403)
        return f(*args, **kwargs)

    return decorated


@app.route("/protected_index")
@token_required
def protected_index_page():
    return redirect(url_for("static", filename="index.html"))


if __name__ == "__main__":
    app.run(debug=True)
