import sqlite3, requests, json
import spotipy
import spotipy.oauth2
from config import CONFIG
from secrets import secrets

class Converter():

    def convert(self,cookie, query):
        playlistID = query["playlist_ID"][0]
        playlistName = query["playlist_name"][0]
        authToken = CONFIG["account"].get_spotifyID(cookie)
        results = self.make_playlist_request(playlistID,authToken)
        song_uris = self.get_uri_of_new_tracks(results,authToken)
        self.make_new_playlist(playlistName+"Parallel",authToken,song_uris)

    def get_user_id(self, token):
        url = "https://api.spotify.com/v1/me"
        headers = {
            "Authorization": "Bearer "+token
        }
        response = requests.get(url,headers= headers)
        id = response.json()["id"]
        return id

    def make_new_playlist(self,name,token,uris):
        id = self.get_user_id(token)
        url = "https://api.spotify.com/v1/users/"+id+"/playlists"
        data = "{\"name\":\""+name+"\",\"description\":\"New parallel playlist\",\"public\":true}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer "+token
        }
        response = requests.post(url,headers= headers,data=data).json()
        playlist_id = response["id"]
        playlist_url = response["owner"]["external_urls"]["spotify"]
        self.add(playlist_url)
        url = "https://api.spotify.com/v1/playlists/"+playlist_id+"/tracks"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer "+token,
        }
        for uri in uris:
            new_url = url+"?uris="+uri
            response= requests.post(new_url,headers=headers)
            print(response.text)


    def make_playlist_request(self,playlist, token):
        url = "https://api.spotify.com/v1/playlists/"+playlist+"/tracks?fields=items(track(name%2Chref%2Cartists%2Cid))&limit=100"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer "+token
        }
        response = requests.get(url,headers= headers)
        reponse =  response.json()
        print (response)
        return response

    def get_uri_of_new_tracks(self,tracks,token):
        song_uris =[]
        for item in tracks["items"]:
            artist_id = item["track"]["artists"][0]["id"]
            song_uris.append(self.get_artist_song(artist_id,token))
        return song_uris

    def get_artist_song(self,id,token):
        url = "https://api.spotify.com/v1/artists/"+id+"/top-tracks?country=US"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer "+token
        }
        response = requests.get(url, headers=headers)
        iterable = response.json()
        return iterable["tracks"][0]["uri"]

    def add(self,url):
        self.cursor.execute('''INSERT OR REPLACE INTO Conversions VALUES(?)''',(url,))
        self.conn.commit()

    def get_all(self):
        self.cursor.execute('''Select playlist from Conversions''')
        return self.cursor.fetchall()

    def __init__(self):
        self.credentials = spotipy.oauth2.SpotifyClientCredentials(client_id = secrets["spotify_client_id"], client_secret = secrets["spotify_client_secret"])
        self.conn = sqlite3.connect("./Data/app_info.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Conversions (playlist TEXT, Primary Key (playlist))''')
        self.conn.commit()
