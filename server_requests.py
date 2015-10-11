import requests
import subprocess
import json
from pydub import AudioSegment

server_name = "http://162.243.156.22"

def get_metadata_from_server(query):
    #get spotify info from server
    payload = { 'q' : query }
    #print query
    r = requests.get(server_name + '/lookup', params=payload)
    print r.content
    return r.content

def init_download_on_server(JSON):
    #tell server to download the query
    payload = json.loads(JSON)
    r = requests.post(server_name + '/initiate', json=payload)
    #print r.text
    #return r.text
    return

def poll_server(QUERY):
    pass #TODO

#init_download_on_server('{"album": "Good Girl Gone Bad: Reloaded", "thumb": "https://i.scdn.co/image/b1244db3be7cb3c1fd05555c2e53dc5d2b94176d", "title": "Umbrella", "artist": "Rihanna"}')

"""
#get query from user
QUERY = argv[1]
#get metadata from server
metadata = get_metadata_from_server(QUERY)
#ask user if this is acceptable
OK = argv[2]
if OK:
    init_download_on_server(QUERY)
else:
    quit()
here_yet = False
while not here_yet:
    here_yet, audio = poll_server(QUERY)
    time.sleep(1)
#enjoy the music
play(audio)
"""

if __name__ == '__main__':
    init_download_on_server('{"album": "Good Girl Gone Bad: Reloaded", "thumb": "https://i.scdn.co/image/b1244db3be7cb3c1fd05555c2e53dc5d2b94176d", "title": "Umbrella", "artist": "Rihanna"}')
