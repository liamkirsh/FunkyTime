import subprocess
import urllib2

def ping(host):
    ping_response = subprocess.Popen(["/bin/ping", "-c1", "-w100", host], stdout=subprocess.PIPE).stdout.read()
    return ping_response

def query_server(query):
    while True:
        responce = urllib2.urlopen(query)
        print(responce)
        if responce:
            return responce

def conferm_query():
    pass
