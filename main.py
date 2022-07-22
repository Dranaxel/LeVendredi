import json, urllib.parse, datetime, logging
import spotipy

from spotipy.oauth2 import SpotifyClientCredentials
from jinja2 import Environment, PackageLoader


logging.basicConfig(level=logging.INFO)
GENRES = {"rap francais", "rap marseille", "french hip hop", "pop urbaine", "rap calme", "rap francais nouvelle vague", "swiss hip hop", "rap inde"}
results = dict()

class releases():
    def __init__(self, country):
        logging.info(f"Logging to Spotify")
        try:
            self.spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        except BaseException:
            logging.error('There have been a problem')
        logging.info(f"Successfully logged in Spotify")
        self.releases = self.spotify.new_releases(country, limit=50)

    def __get_genres(self, album):
        spotify = self.spotify
        genres = set()
        for artist in album['artists']:
                artist_info = spotify.artist(artist['id'])
                for i in artist_info["genres"]:
                    genres.add(i)
        return(genres)

    def get_albums(self):
        albums = []
        releases = self.releases
        while releases is not None:
            for album in releases['albums']['items']:
                album_date = album['release_date']
                album_genres = self.__get_genres(album)
                artists = [x['name'] for x in album['artists']]
                albums.append(
                    {
                            "name": album['name'],
                            "artists": artists,
                            "date": album['release_date'],
                            "genres": album_genres,
                            "type": album['album_type'],
                            "images": album['images']
                    }
                )
            releases = self.next()
        return albums

    def get_page(self):
        return self.releases

    def next(self):
        self.releases = self.spotify.next(self.releases['albums'])
        return  self.releases

def get_today_date():
    today_date = datetime.date.today()
    today_date = str(today_date)
    logging.info(f"Today's date is {today_date}")
    return(today_date)


if __name__ == '__main__':
    jinja = Environment(
            loader=PackageLoader("main")
    )
    results = []
    today_date = get_today_date()
    releases = releases("FR")
    releases = releases.get_albums()

    for i in releases:
        if i["genres"].intersection(GENRES):
           results.append(i) 

    template = jinja.get_template("main.jinja")
    rendered = template.render(albums=results)

    with open("web-src/main.html", "w") as f:
        f.write(rendered)

