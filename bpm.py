
import requests
import base64

CLIENT_ID = "a57e42d0f05f4372b2d10ae9c6a2780d"
CLIENT_SECRET = "ef91b554085e46ac98a88e97c31a2bcb"

def get_access_token():
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }
    resp = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    return resp.json().get("access_token")

def search_track(track_name, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "q": track_name,
        "type": "track",
        "limit": 1
    }
    resp = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    items = resp.json().get("tracks", {}).get("items", [])
    return items[0]["id"] if items else None

def get_bpm(track_id, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    resp = requests.get(f"https://api.spotify.com/v1/audio-features/{track_id}", headers=headers)
    return int(resp.json().get("tempo")) if resp.ok else None

def fetch_bpm(track_name):
    token = get_access_token()
    if not token:
        return None
    track_id = search_track(track_name, token)
    if not track_id:
        return None
    return get_bpm(track_id, token)
