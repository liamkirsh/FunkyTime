import requests
import sys
from urllib import quote

script, query = sys.argv
#print 'https://api.spotify.com/v1/search?q=' + quote(query)
#sys.exit(0)
r = requests.get('https://api.spotify.com/v1/search?q=' + quote(query) + '&type=track')
json = r.json()

print json["tracks"]["items"][0]["album"]["name"]
sys.stdout.flush()
sys.exit(0)
