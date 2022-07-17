import json, urllib.parse, datetime, logging
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

logging.basicConfig(level=logging.INFO)
GENRES = ("rap francais", "rap marseille", "french hip hop", "pop urbaine", "rap calme", "rap francais nouvelle vague", "swiss hip hop", "rap inde")
results = dict()

def get_today_date():
    today_date = datetime.date.today()
    today_date = str(today_date)
    logging.info(f"Today's date is {today_date}")
    return(today_date)

def is_wanted_genre(genres):
    return True if genres in GENRES else False

def get_genres(album):
    genres = []
    for artist in album['artists']:
            artist_info = spotify.artist(artist['id'])
            genres.extend(artist_info["genres"])
    return(genres)

if __name__ == '__main__':
    today_date = get_today_date()

    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    releases = spotify.new_releases(country="FR", limit=50)

    while releases is not None:
        for album in releases['albums']['items']:
            album_date = album['release_date']

            album_genres = get_genres(album)
            filtered_albums = list(filter(is_wanted_genre, album_genres))

            #if filtered_genres != [] and "2022-07-15" == album_date: 
            if filtered_albums != []: 
                results.update(
                        {
                            album['name']: 
                            {
                                "artist": album['artists'][0]['name'],
                                "date": album['release_date'],
                                "genres": album_genres,
                                "type": album['album_type']
                            }
                        }
                    )
                print(album['album_type'], album['name'], album['artists'][0]['name'], album_genres, album['release_date'], sep=' - ')
        releases = spotify.next(releases['albums'])
    print(results)
