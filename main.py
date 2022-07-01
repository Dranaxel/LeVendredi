import json, urllib.parse, datetime
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

GENRES = ["hip hop", "rap francais", "rap marseille", "french hip hop", "francoton", "pop urbaine", "rap calme", "rap francais nouvelle vague", "swiss hip hop", "rap inde"]

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

releases = spotify.new_releases(country="FR", limit=50)

today_date = datetime.date.today()
today_date = str(today_date)


def is_wanted_genre(genres):
    return True if genres in GENRES else False

while releases is not None:
    print(releases)
    for albums in releases['albums']['items']:
        album_date = albums['release_date']
        artists_genres = []

        for artist in albums['artists']:
            artist_info = spotify.artist(artist['id'])
            genres = artist_info["genres"]
            artists_genres += genres

        filtered_genres = list(filter(is_wanted_genre, artists_genres))

        if filtered_genres != [] and today_date == album_date: 
            print(albums['name'], albums['artists'][0]['name'], genres, albums['release_date'], sep=' - ')


        #    if GENRES in genres:
        #        print(albums['name'], albums['artists'][0]['name'], genres, sep=' - ')
    releases = spotify.next(releases['albums'])
    print("next")
