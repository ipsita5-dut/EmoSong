import requests
from base64 import b64encode

SPOTIFY_CLIENT_ID = "79fd69d47eb74d6d96e36e76b351dfa0"
SPOTIFY_CLIENT_SECRET = "c5115519ccb543b095773cda41b1680d"

def check_spotify_keys(client_id, client_secret):
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + b64encode(f"{client_id}:{client_secret}".encode()).decode()
    }
    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print("Keys are valid!")
        print("Access Token:", response.json().get("access_token"))
    else:
        print("Invalid keys!")
        print(response.json())

check_spotify_keys(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
