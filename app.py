from flask import Flask, request

from meetup.env import Env
from meetup.meetup import request_access_token, save_tokens

app = Flask(__name__)


@app.route("/")
def index() -> str:
    return "Welcome to the Meetup Auth App!"


@app.route("/redirect")
def redirect_uri() -> str:
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
