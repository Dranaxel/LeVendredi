import json, urllib.parse, datetime, logging, os
import spotipy

from spotipy.oauth2 import SpotifyClientCredentials
from jinja2 import Environment, PackageLoader


logging.basicConfig(level=logging.INFO)
GENRES = {"rap francais", "rap marseille", "french hip hop", "pop urbaine", "rap calme", "rap francais nouvelle vague", "swiss hip hop", "rap inde"}
results = dict()
COUNTRY = os.getenv("COUNTRY", "FR")

def spotify_connector():
    logging.info(f"Logging to Spotify")
    try:
        spotify_instance = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    except BaseException:
        logging.error('There have been a problem')
    logging.info(f"Successfully logged in Spotify")
    return spotify_instance

def get_artists(genre, spotify):
    artists_list = set()
    payload = f'genre: "{genre}"'
    spotify_artists = spotify.search(q=payload, type="artist", limit=50)
    while spotify_artists is not None:
        artists = spotify_artists['artists']['items']
        artists = [ x["id"] for x in artists]
        artists_list.update(artists)
        spotify_artists = spotify.next(spotify_artists['artists'])
    return artists_list

def search_for_albums(artist_id, spotify):
    spotify_albums = spotify.artist_albums(artist_id, album_type="album", limit=50)
    albums = spotify_albums["items"]
    print(albums)

ls_artists = set()
spotify = spotify_connector()
for _ in GENRES:
    print(_)
    artists = get_artists(_, spotify)
    ls_artists.update(artists)

print(len(ls_artists))
for i in ls_artists:
    print(i)
    search_for_albums(i, spotify)

def get_today_date():
    today_date = datetime.date.today()
    today_date = str(today_date)
    logging.info(f"Today's date is {today_date}")
    return(today_date)



