import os

import json
import requests
import os
import base64
import json


from datetime import date

client_id = "*"
client_secret = "*"
base64_cid_csec="*"
spotify_user_id = "*"
#old all id 2m8zz6DW4pvVS11HQFYqah
sotd_all_id = "*"
sotd_id = "*"
refresh_token="*"
real_token="*"

def refresh():
    query = "https://accounts.spotify.com/api/token"
    response = requests.post(query, data={"grant_type": "refresh_token", "refresh_token": refresh_token}, headers={"Authorization": "Basic " + base64_cid_csec})
    tresponse = response.json()
    #print(tresponse)
    
    return tresponse["access_token"]

def get_auth_header(new_token):
    return {"Content-Type":"application/json", "Authorization": "Bearer " + new_token}


class SaveSongs:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = refresh()
        self.tracks = ""
        self.header = get_auth_header(self.spotify_token)



    def find_songs(self):

        print("Finding songs in SOTD...")
        # Loop through playlist tracks, add them to list

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            sotd_id)

        response = requests.get(query,
                                headers=self.header)

        response_json = response.json()

        print(response)

        for i in response_json["items"]:
            self.tracks += (i['track']['uri'] + ",")
        self.tracks = self.tracks[:-1]
        
        self.add_to_playlist()

    def add_to_playlist(self):
        # add all songs to SOTD All playlist
        print("Adding songs to SOTD ALL Playlist...")


        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(
            sotd_all_id, self.tracks)

        response = requests.post(query, headers=self.header)

        print(response.json)

class DeleteSongs:
    def __init__(self):
        self.spotify_token = refresh()
        self.tracks = []
        self.header = get_auth_header(self.spotify_token)

    

    def delete_songs(self):

        print("Finding songs in SOTD...")
        #print(self.spotify_token)
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
        print("Deleting songs in SOTD...")

        #self.new_playlist_id = self.create_playlist()
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            sotd_id)

        response = requests.delete(query, headers=self.header,data=json.dumps(self.tracks))

        print(response.json)

a = SaveSongs()
a.find_songs()
