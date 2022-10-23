import json, urllib.parse, datetime, logging, os
import spotipy

from spotipy.oauth2 import SpotifyClientCredentials
from jinja2 import Environment, PackageLoader


logging.basicConfig(level=logging.INFO)
GENRES = {"rap francais", "rap marseille", "french hip hop", "pop urbaine", "rap calme", "rap francais nouvelle vague", "swiss hip hop", "rap inde"}
GENRES = {"rap francais"}
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
    artists_list = []
    logging.info(f'Gathering artists for genre {genre}')
    payload = f'genre: "{genre}"'
    spotify_artists = spotify.search(q=payload, type="artist", limit=50)
    while spotify_artists is not None:
        artists = spotify_artists['artists']['items']
        artists_list.extend(artists)
        spotify_artists = spotify.next(spotify_artists['artists'])
    logging.info(f'Gathered {len(artists_list)} artists')
    return artists_list

def search_for_albums(artist, spotify):
    logging.info(artist)
    logging.info(f'Gathering albums from artist {artist["name"]}')
    spotify_albums = spotify.artist_albums(artist['id'], album_type="album", limit=50)
    albums = spotify_albums["items"]
    logging.info(f'Gathered {len(albums)} albums from artist {artist["name"]}')
    return albums

def get_album_info(album, spotify):
    album = spotify.album(album['id'])
    logging.info(f'Gathered {album["name"]} released at {album["release_date"]}')
    return album

def get_today_date():
    today_date = datetime.date.today()
    today_date = str(today_date)
    logging.info(f"Today's date is {today_date}")
    return(today_date)

if __name__ == "__main__":
    ls_artists = []
    today_date = get_today_date()
    today_date = "2022-10-21"
    spotify = spotify_connector()

    for _ in GENRES:
        artists = get_artists(_, spotify)
        ls_artists.extend(artists)

    released_albums = []
    for i in ls_artists:
        albums = search_for_albums(i, spotify)
        for _ in albums:
            album = get_album_info(_, spotify)
            if album["release_date"] == today_date:
                logging.info(f'Added album {album["name"]}')
                released_albums.append(album)

    print(released_albums)

        



