import os
import requests
from requests_oauthlib import OAuth1
from requests_oauthlib import OAuth1Session
from xmltodict import parse as xtd

client_key = os.environ['CLIENT_KEY']
client_secret = os.environ['CLIENT_SECRET']
resource_owner_key = os.environ['RESOURCE_OWNER_KEY']
resource_owner_secret = os.environ['RESOURCE_OWNER_SECRET']
page = 0
URL = f'http://api.music-story.com/release/search?creation_date=2021-07-08&genres=rap-francais&pageCount=100&format=album&page={page}'
TOKEN_URL = 'http://api.music-story.com/oauth/request_token/json'

oauth = OAuth1(client_key, client_secret)
r = requests.get(url=TOKEN_URL, auth=oauth)
token = xtd(r.text)["root"]["data"]["token"]
secret = xtd(r.text)["root"]["data"]["token_secret"]

while True:

    print(URL)
    oauth = OAuth1Session(client_key, client_secret, resource_owner_key=token, resource_owner_secret=secret, signature_type='query')
    query = oauth.post(URL)
    for i in xtd(query.text)["root"]["data"]["item"]:
        print(i['title'])

    page += 1
    URL = f'http://api.music-story.com/release/search?creation_date=2021-07-08&genres=rap-francais&pageCount=100&format=album&page={page}'
