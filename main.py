import json, urllib.parse, datetime, logging
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

GENRES = ("rap francais", "rap marseille", "french hip hop", "pop urbaine", "rap calme", "rap francais nouvelle vague", "swiss hip hop", "rap inde")

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
logging.basicConfig(level=logging.INFO)

releases = spotify.search("tag:new", type="album", limit=50, market="FR")

logging.info(f"number of results {releases['albums']['total']}")

today_date = datetime.date.today()
today_date = str(today_date)
logging.info(f"Today's date is {today_date}")

def is_wanted_genre(genres):
    return True if genres in GENRES else False

def get_genres(album):
    genres = []
    for artist in album['artists']:
            artist_info = spotify.artist(artist['id'])
            genres.extend(artist_info["genres"])
    return(genres)

while releases is not None:
    for album in releases['albums']['items']:
        album_date = album['release_date']

        album_genres = get_genres(album)
        filtered_genres = list(filter(is_wanted_genre, album_genres))

        if filtered_genres != [] and "2022-07-01" == album_date: 
        #if filtered_genres != []: 
            print(album['album_type'], album['name'], album['artists'][0]['name'], album_genres, album['release_date'], sep=' - ')

    releases = spotify.next(releases['albums'])
