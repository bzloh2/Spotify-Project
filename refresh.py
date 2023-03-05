from dotenv import load_dotenv
import os

import json
import requests
import os
import base64
from requests import post, delete
import json


from datetime import date


client_id = "*"
client_secret = "*"
base64_cid_csec="*="
spotify_user_id = "*"
sotd_id = "*"
refresh_token="*"

def refresh():
    query = "https://accounts.spotify.com/api/token"
    response = requests.post(query, data={"grant_type": "refresh_token", "refresh_token": refresh_token}, headers={"Authorization": "Basic " + base64_cid_csec})
    tresponse = response.json()
    print(tresponse)
    
    return tresponse["access_token"]

def get_auth_header(new_token):
    return {"Content-Type":"application/json", "Authorization": "Bearer " + new_token}


class DeleteSongs:
    def __init__(self):
        self.spotify_token = refresh()
        self.tracks = []
        self.header = get_auth_header(self.spotify_token)

    

    def delete_songs(self):

        print("Finding songs in SOTD...")
        print(self.spotify_token)
        # Loop through playlist tracks, add them to list

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            sotd_id)

        response = requests.get(query,
                                headers=self.header)

        response_json = response.json()

        print(response)

        for i in response_json["items"]:
            track_dict = {"uri":i['track']['uri']}
            self.tracks.append(track_dict)
        #add songs to a dictionary of tracks which is needed for deletion
        params={"tracks":self.tracks}
        self.tracks=params
        self.delete_sotd_songs()

    def delete_sotd_songs(self):
        # add all songs to new playlist
        print("Deleting songs...")

        #self.new_playlist_id = self.create_playlist()
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            sotd_id)

        response = requests.delete(query, headers=self.header,data=json.dumps(self.tracks))

        print(response.json)

