import requests
import subprocess
import json

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
    return r.text #server returns the hash of the json. keep it safe

def poll_server(the_hash):
    payload = { 'hash' : the_hash }
    r = requests.get(server_name + '/poll', params=payload)
    data = r.content
    ok = data[0]
    if not ok:
        return None
    else:
        return data[1:]  #this will return None if no response, and a bitstream if yes response

if __name__ == '__main__':
    init_download_on_server('{"album": "Good Girl Gone Bad: Reloaded", "thumb": "https://i.scdn.co/image/b1244db3be7cb3c1fd05555c2e53dc5d2b94176d", "title": "Umbrella", "artist": "Rihanna"}')
