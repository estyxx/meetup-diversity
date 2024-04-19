import json
from pathlib import Path
from dataclasses import dataclass
from typing import Mapping, Optional
import requests
from djangolondon.env import Env


token_file_path = Path("tokens.json")
import webbrowser


@dataclass
class Tokens:
    access_token: str
    refresh_token: str

    def to_dict(self) -> Mapping[str, str]:
        return {"access_token": self.access_token, "refresh_token": self.refresh_token}


def save_tokens(access_token: str, refresh_token: Optional[str]):
    """Save the access and refresh tokens to a JSON file."""
    tokens = {"access_token": access_token, "refresh_token": refresh_token}
    token_file_path.parent.mkdir(parents=True, exist_ok=True)
    with token_file_path.open("w") as file:
        json.dump(tokens, file)


def get_tokens(env: Env) -> Tokens:
    """Retrieve the access and refresh tokens from a JSON file, refresh if necessary."""
    if token_file_path.exists():
        with token_file_path.open("r") as file:
            tokens_data = json.load(file)
            tokens = Tokens(**tokens_data)
            if is_token_valid(tokens.access_token):
                return tokens
            else:
                if tokens.refresh_token:
                    print("Refreshing token...")
                    refreshed_tokens = refresh_access_token(env, tokens.refresh_token)
                    if "access_token" in refreshed_tokens:
                        save_tokens(
                            refreshed_tokens["access_token"],
                            refreshed_tokens.get("refresh_token", tokens.refresh_token),
                        )
                        return Tokens(**refreshed_tokens)
                    else:
                        print("Failed to refresh token. Need reauthorization.")
                print("No valid refresh token. Need reauthorization.")
    raise Exception("Authorization is required.")


def is_token_valid(access_token: str) -> bool:
    """Check if the access token is still valid using a lightweight API call."""
    url = "https://api.meetup.com/gql"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {"query": "query { self { id } }"}
    response = requests.post(url, headers=headers, json=payload)
    return response.status_code == 200


def request_access_token(env: Env, code: str):
    url = "https://secure.meetup.com/oauth2/access"
    data = {
        "client_id": env.MEETUP_COM_KEY,
        "client_secret": env.MEETUP_COM_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": env.MEETUP_COM_REDIRECT_URI,
        "code": code,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=data, headers=headers)

    return response.json()


def refresh_access_token(env: Env, refresh_token: str) -> Mapping[str, str]:
    """Refresh the access token using the refresh token."""
    url = "https://secure.meetup.com/oauth2/access"
    data = {
        "client_id": env.MEETUP_COM_KEY,
        "client_secret": env.MEETUP_COM_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return response.json()  # Handle error better in practice


def authorize(env: Env):
    try:
        get_tokens(env)
        print("Token is valid, continuing...")
    except Exception as e:
        print(e)
        # Redirect to authorization URL if no valid token is found
        url = f"https://secure.meetup.com/oauth2/authorize?client_id={env.MEETUP_COM_KEY}&response_type=code&redirect_uri={env.MEETUP_COM_REDIRECT_URI}"
        print("Redirecting for authorization:", url)
        webbrowser.open(url)


def graphql_query(query: str, variables: Optional[dict] = None) -> dict:
    """
    Perform a GraphQL query using the provided query string and variables.
    Automatically handles token retrieval and refresh.
    """

    env = Env.get_env()
    try:
        tokens = get_tokens(
            env
        )  # This will ensure we have a valid access token or handle necessary actions
        access_token = tokens.access_token
        url = "https://api.meetup.com/gql"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        payload = {"query": query, "variables": variables}
        response = requests.post(url, headers=headers, json=payload)
        return response.json()  # Returns the JSON response from the API
    except Exception as e:
        print(f"Error occurred while trying to make a GraphQL query: {str(e)}")
        return {"error": str(e)}  # Returns a dictionary with error details
