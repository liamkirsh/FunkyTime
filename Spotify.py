import requests
import sys
from urllib import quote
import json

script, query = sys.argv
r = requests.get('https://api.spotify.com/v1/search?q=' + quote(query) + '&type=track')
spot = r.json()
if spot["tracks"]["total"] == 0:
    print
    sys.stdout.flush()
    sys.exit(0)
result = {"album": spot["tracks"]["items"][0]["album"]["name"], "artist": spot["tracks"]["items"][0]["artists"][0]["name"], "name": spot["tracks"]["items"][0]["name"], "thumb": spot["tracks"]["items"][0]["album"]["images"][1]["url"]}

print json.dumps(result)
sys.stdout.flush()
sys.exit(0)
