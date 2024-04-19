from flask import Flask, request

from djangolondon.env import Env
from djangolondon.meetup import request_access_token
from djangolondon.meetup import save_tokens

app = Flask(__name__)


@app.route("/")
def index():
    return "Welcome to the Meetup Auth App!"


@app.route("/redirect")
def redirect_uri():

    env = Env.get_env()
    code = request.args.get("code")
    state = request.args.get("state")

    if code:
        token_response = request_access_token(env, code)
        save_tokens(token_response["access_token"], token_response["refresh_token"])

        return f"Access Token Response: {token_response}"
    return f"Failed to retrieve authorization code. State: {state}"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
