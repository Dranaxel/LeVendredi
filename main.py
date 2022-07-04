import json, urllib.parse, datetime, logging
import spotipy
from jinja2 import Environment, PackageLoader
from spotipy.oauth2 import SpotifyClientCredentials

GENRES = ("rap francais", "rap marseille", "french hip hop", "pop urbaine", "rap calme", "rap francais nouvelle vague", "swiss hip hop", "rap inde")

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
jinja = Environment(
        loader=PackageLoader("main")
        )
logging.basicConfig(level=logging.INFO)

releases = spotify.search("tag:new", type="album", limit=50, market="FR")

logging.info(f"number of results {releases['albums']['total']}")

today_date = datetime.date.today()
#today_date = str(today_date)
today_date = "2022-07-01"
logging.info(f"Today's date is {today_date}")

albums = []
singles = []

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

        if filtered_genres != [] and today_date == album_date: 
            if album['album_type'] == 'album' and album not in albums:
                albums.append(album)
            if album['album_type'] == 'single' and album not in singles:
                singles.append(album)
            print(album['album_type'], album['name'], album['artists'][0]['name'], album_genres, album['release_date'], sep=' - ')

    try:
        releases = spotify.next(releases['albums'])
    except:
        releases = None

template = jinja.get_template("main.jinja")
print(template.render(albums=albums))

