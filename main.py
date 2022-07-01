import spotipy
import json, urllib.parse
from spotipy.oauth2 import SpotifyClientCredentials

GENRES = ["rap francais", "rap marseille"]

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

releases = spotify.new_releases(country="FR")

def is_wanted_genre(genres):
    return True if genres in GENRES else False

while releases['albums']['next']:
    for albums in releases['albums']['items']:
        artists_genres = []

        for artist in albums['artists']:
            artist_info = spotify.artist(artist['id'])
            genres = artist_info["genres"]
            artists_genres += genres

        filtered_genres = list(filter(is_wanted_genre, artists_genres))

        if filtered_genres != []:
            print(albums['name'], albums['artists'][0]['name'], genres, sep=' - ')


        #    if GENRES in genres:
        #        print(albums['name'], albums['artists'][0]['name'], genres, sep=' - ')
    releases = spotify.next(releases['albums'])
