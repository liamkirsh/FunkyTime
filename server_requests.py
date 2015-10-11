import requests
import subprocess

server_name = "http://162.243.156.22"

def ping(host):
    ping_response = subprocess.Popen(["/bin/ping", "-c1", "-w100", server_name + '/lookup?q=' + host], stdout=subprocess.PIPE).stdout.read()
    return ping_response

def get_metadata_from_server(QUERY):
    #get spotify info from server
    payload = { 'q' : QUERY }
    print(QUERY)
    r = requests.get(server_name + '/lookup?q=', params=payload)
    print(r.json())
    return r.json()

def init_download_on_server(JSON):
    #tell server to download the query
    payload = JSON
    r = requests.post(server_name + '/initiate', params=payload)
    return r.text

def poll_server(QUERY):
    pass #TODO



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
