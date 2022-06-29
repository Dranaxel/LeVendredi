import spotipy
import json, urllib.parse
from spotipy.oauth2 import SpotifyClientCredentials

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

releases = spotify.search(
        q="",
        limit=50,
        type='album',
        market='FR')

#releases = json.load(releases)

print(type(releases))
print(releases)
