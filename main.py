import spotipy
import json, urllib.parse
from spotipy.oauth2 import SpotifyClientCredentials

GENRES = "rap francais"

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

releases = spotify.new_releases(country="FR")

#releases = json.load(releases)

while releases['albums']['next']:
    for albums in releases['albums']['items']:
        for artist in albums['artists']:
            artist_info = spotify.artist(artist['id'])
            genres = artist_info["genres"]
            
            if GENRES in genres:
                print(albums['name'], albums['artists'][0]['name'], genres, sep=' - ')
    releases = spotify.next(releases['albums'])
