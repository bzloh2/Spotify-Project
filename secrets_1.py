
import os
import base64
from requests import post
import json

client_id = "*"
client_secret = "*"

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token    



spotify_user_id = "1266557971"
discover_weekly_id = "6y7ZL1JO0qCb2sEMZxDHls"
refresh_token = get_token()
base_64 = ""