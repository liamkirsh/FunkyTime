import requests
import json
import time
from sys import argv
import sys

server_name = "http://162.243.156.22"

def get_metadata_from_server(query):
    #get spotify info from server
    payload = { 'q' : query }
    #print query
    r = requests.get(server_name + '/lookup', params=payload)
    print r.content
    if (r.content == "Not found"):
        sys.exit(100)
    return r.content

def init_download_on_server(JSON):
    #tell server to download the query
    payload = json.loads(JSON)
    r = requests.post(server_name + '/initiate', data=payload)
    #print r.text
    return r.text #server returns the hash of the json. keep it safe

def poll_server(the_hash):
    payload = { 'hash' : the_hash }
    r = requests.get(server_name + '/ready', params=payload)
    ctype = r.headers['content-type']
    data = r.content
    print 'ctype', ctype
    if 'text/html' in ctype:
        return None
    else:
        return data, ctype

if __name__ == '__main__':
    '''#init_download_on_server('{"album": "Good Girl Gone Bad: Reloaded", "thumb": "https://i.scdn.co/image/b1244db3be7cb3c1fd05555c2e53dc5d2b94176d", "title": "Umbrella", "artist": "Rihanna"}')'''
    metadata = get_metadata_from_server(argv[1])
    hash = init_download_on_server(metadata)
    dataNtype = poll_server(hash)
    while dataNtype is None:
        time.sleep(2)
        dataNtype = poll_server(hash)
    with open('file', "wb") as f:
        f.write(dataNtype[0])

    '''dataNtype = poll_server("670b7d929218f7e36622e202eebb3fd1")
    while dataNtype is None:
        dataNtype = poll_server("670b7d929218f7e36622e202eebb3fd1")
    print dataNtype[1]
    '''
