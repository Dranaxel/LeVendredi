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

def get_albums_info(albums, spotify):
    albums_name = [ _["name"] for _ in albums]
    albums_id = [ _["id"] for _ in albums]
    logging.info(f'Gathering {albums_name} with ids {albums_id}')

    if len(albums) == 0:
        logging.info(f'No album to gather, passing')
        pass
    elif len(albums) > 20:
        logging.info('More than 20 albums, breaking it in chunks')
        albums_buffer = []
        chunks = [ albums_id[x:x+20] for x in range(0, len(albums_id), 20)]
        logging.info(f'Processing chunks: {chunks}')
        for i in chunks:
            i = spotify.albums(i)
            albums_buffer.append(i)
        return albums_buffer
    else:
        albums = spotify.albums(albums_id)
        logging.info(f'Gathered {albums_name}')
        return albums

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
        print(albums)
        albums = get_albums_info(albums, spotify)
        released_albums.append(albums)
            #if album["release_date"] == today_date:
            #    logging.info(f'Added album {album["name"]}')
            #    released_albums.append(album)
    logging.info(f'Gathered {len(released_albums)} albums')
    for _ in released_albums:
        print(_)
        if _['release_date'] == today_date:
            print(_)

