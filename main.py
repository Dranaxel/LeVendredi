import json, urllib.parse, datetime, logging, os
import spotipy

from spotipy.oauth2 import SpotifyClientCredentials
from jinja2 import Environment, PackageLoader


logging.basicConfig(level=logging.INFO)
GENRES = {"rap francais", "rap marseille", "french hip hop", "pop urbaine", "rap calme", "rap francais nouvelle vague", "swiss hip hop", "rap inde"}
results = dict()
COUNTRY = os.getenv("COUNTRY", "FR")

logging.info(f"Logging to Spotify")
try:
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
except BaseException:
    logging.error('There have been a problem')
logging.info(f"Successfully logged in Spotify")


ls_artists = set()
for _ in GENRES:
    payload = f'genre:"{_}"'
    spotify_artists = spotify.search(q=payload, type="artist", limit=50)
    print(spotify_artists['artists']["total"])
    while spotify.next(spotify_artists['artists']):
        artists = spotify_artists['artists']['items']
        artists = [ x["name"] for x in artists]
        ls_artists.update(artists)
        spotify_artists = spotify.next(spotify_artists['artists'])

print(ls_artists)
print(len(ls_artists))
def get_today_date():
    today_date = datetime.date.today()
    today_date = str(today_date)
    logging.info(f"Today's date is {today_date}")
    return(today_date)



