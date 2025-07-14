
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
    try:
        resp = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
        resp.raise_for_status()
        return resp.json().get("access_token")
    except Exception as e:
        print(f"[Auth Error] Failed to get token: {e}")
        return None

def search_track(track_name, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "q": track_name,
        "type": "track",
        "limit": 1
    }
    try:
        resp = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
        resp.raise_for_status()
        items = resp.json().get("tracks", {}).get("items", [])
        if not items:
            print(f"[Not Found] No track match for: '{track_name}'")
        return items[0] if items else None
    except Exception as e:
        print(f"[Search Error] '{track_name}' → {e}")
        return None

def get_audio_features(track_id, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        resp = requests.get(f"https://api.spotify.com/v1/audio-features/{track_id}", headers=headers)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[Feature Error] Track ID '{track_id}' → {e}")
        return None


def decode_key_mode(key, mode):
    key_name = {0: 'C', 1: 'C♯/D♭', 2: 'D', 3: 'D♯/E♭', 4: 'E', 5: 'F', 6: 'F♯/G♭', 7: 'G', 8: 'G♯/A♭', 9: 'A', 10: 'A♯/B♭', 11: 'B'}.get(key, '?')
    return f"{key_name} {'Major' if mode == 1 else 'Minor'}" if key_name != '?' else None

def fetch_bpm(track_name):
    token = get_access_token()
    if not token:
        print(f"[Fallback] No token. Skipping '{track_name}'")
        return {
            "BPM": None,
            "Match Name": None,
            "Match Artist": None,
            "Key": None,
            "Energy": None
        }
    track_data = search_track(track_name, token)
    if not track_data:
        return {
            "BPM": None,
            "Match Name": None,
            "Match Artist": None,
            "Key": None,
            "Energy": None
        }
    features = get_audio_features(track_data["id"], token)
    if not features:
        return {
            "BPM": None,
            "Match Name": track_data["name"],
            "Match Artist": track_data["artists"][0]["name"],
            "Key": None,
            "Energy": None
        }
    key_mode = decode_key_mode(features.get("key"), features.get("mode"))
    return {
        "BPM": int(features.get("tempo")),
        "Match Name": track_data["name"],
        "Match Artist": track_data["artists"][0]["name"],
        "Key": key_mode,
        "Energy": features.get("energy")
    }
