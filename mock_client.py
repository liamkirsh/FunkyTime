#THIS FILE IS PSEUDOCODE. DO NOT RUN.
from sys import argv
import time

def get_metadata_from_server(QUERY):
    #get spotify info from server
    pass
def init_download_on_server(QUERY):
    #tell server to download the query
    pass
def poll_server(QUERY):
    pass




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
