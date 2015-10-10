import requests as r

server_name = "http://162.243.156.22"

def get_metadata_from_server(QUERY):
    #get spotify info from server
    response = r.get(server_name, q = QUERY);
    return response.json()
def init_download_on_server(QUERY):
    #tell server to download the query
    pass #TODO
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
