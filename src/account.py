import uuid, sqlite3
from datetime import datetime, timedelta
from dateutil.parser import parse
from config import CONFIG
import spotipy
import spotipy.oauth2
from secrets import secrets

class Account():

    #after authentication, add that spotify ID permanently to this account
    def add_spotifyID(self,cookie, spotifyID):
        self.cursor.execute('''UPDATE Accounts SET spotify_token = ? WHERE
                    handle =?''',(spotifyID, cookie))
        self.conn.commit()

    def get_spotifyID(self, cookie):
        self.cursor.execute('''SELECT spotify_token from Accounts where handle =
                            ?''',(cookie,))
        token = self.cursor.fetchone()[0]
        return token

    def handle_R(self, cookie):
        spotify_handle = self.get_spotifyID(cookie)
        if spotify_handle == None:
            raise NotEnoughAuthentication
        #get the playlists from SPOTIFY
        sp = spotipy.client.Spotify(auth = spotify_handle, client_credentials_manager = self.credentials )
        try:
            results = sp.current_user_playlists(limit = 15)
            (links,names,id) = self.handle_playlist_results(results)
            return (links,names,id)
        except spotipy.client.SpotifyException:
            raise SpotifyTokenExpired

    def handle_playlist_results(self,results):
        playlists = results["items"]
        length = len(playlists)
        links=[None]*length
        names=[None]*length
        ids = [None]*length
        pictures = [None]*length
        counter = 0
        for item in playlists:
            links[counter] =item["external_urls"]["spotify"]
            ids[counter] =item["id"]
            names[counter] =item["name"]
            counter = counter+1
        return (links,names,ids)

    def handle_CU(self,body):
        try:
            assert "username" in body and "password" in body
        except AssertionError:
            raise NotEnoughInfoError

        #deal with creating new account
        if "email" in body:
            handle = self.create(body["username"][0],body["password"][0],\
                                body["email"][0])
        #deal with a sign in
        else:
            handle = self.retrieve(body["username"][0],body["password"][0])
        return handle


    def create(self,username,password,email):
        handle = str(uuid.uuid4())
        handle_expiration = datetime.now()+timedelta(hours=4)

        try:
            self.cursor.execute(''' INSERT INTO Accounts
            (username,password,email,handle,handle_expiration) VALUES(?,?,?,?,?)''',
                                (username,password,email,handle,handle_expiration))
            self.conn.commit()
            return handle
        except sqlite3.IntegrityError:
            #email or password is already in use
            raise BadAccountIdentifiersError

    def retrieve(self,username,password):
        self.cursor.execute('''SELECT handle,handle_expiration FROM Accounts
                            WHERE username = ?and password = ?'''\
                            ,(username,password))
        list = self.cursor.fetchone()
        self.conn.commit()
        if list == None:
            raise BadSignInError
        handle = list[0]
        expiration = parse(list[1])
        if datetime.now()>expiration: #handle expired
            handle = str(uuid.uuid4())
            expiration = datetime.now()+timedelta(hours=4)
            self.cursor.execute('''UPDATE Accounts SET handle=?,handle_expiration
                                =? WHERE username = ?and password = ? ''',\
                                (handle,expiration,username,password))
            self.conn.commit()
        return handle

    def handle_D_token(self,cookie):
        self.cursor.execute('''UPDATE Accounts SET spotify_token = NULL where
            handle = ?''',(cookie,))
        self.conn.commit()

    def __init__(self):
        self.credentials = spotipy.oauth2.SpotifyClientCredentials(client_id = secrets["spotify_client_id"], client_secret = secrets["spotify_client_secret"])
        self.conn = sqlite3.connect("./Data/app_info.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Accounts ( username
                            VARCHAR(100) NOT NULL,password VARCHAR(100) NOT NULL,
                            email VARCHAR(100) NOT NULL,
                            handle TEXT, handle_expiration TIMESTAMP,
                            spotify_token TEXT,
                            PRIMARY KEY(username,email))''')
        self.conn.commit()

class BadSignInError(Exception):
    pass

class BadAccountIdentifiersError(Exception):
    pass

class NotEnoughInfoError(Exception):
    pass

class NotEnoughAuthentication(Exception):
    pass

class SpotifyTokenExpired(Exception):
    pass
