import requests
#import urllib2
import libtorrent as lt
import time
import sys
import os

ses = lt.session()
ses.listen_on(6881, 6891)

# First, accept URL to torrent file as a param and grab it
if not os.path.exists('torrents'):
    os.makedirs('torrents')
if not os.path.exists('downloads'):
    os.makedirs('downloads')
#print sys.argv[1]
#sys.exit(100)
headers = {'user-agent': 'Wget/1.15 (linux-gnu)'}
r = requests.get(sys.argv[1], headers=headers)
#f = urllib2.urlopen(sys.argv[1])
tFile = sys.argv[1].split('/')[-1]
filename = os.path.join('torrents', tFile)
with open(filename, 'wb') as fd:
	fd.write(r.content)

#filename=sys.argv[1]
info = lt.torrent_info(filename)
REQUIRED = sys.argv[2]
#selection
admitted = []
i=0
for f in info.files():
    if REQUIRED in f.path:
        admitted.append(i)
        print f.path
    i += 1
MAX_I = i
#####This section maintains a list of permitted filenames to download


h = ses.add_torrent({'ti': info, 'save_path': './downloads/'})


#prioritization
for fileIndex in range(MAX_I):
    if fileIndex in admitted:
        h.file_priority(fileIndex, 7)
    else:
        h.file_priority(fileIndex, 0)
#####This section sets the priority of the allowed names to 7 and unallowed names to 0


ses.start_dht()
ses.start_lsd()
ses.start_natpmp()
ses.start_upnp()
print 'starting', h.name()
print ses.is_dht_running()
while (not h.is_seed()):
	s = h.status()

	state_str = ['queued', 'checking', 'downloading metadata', \
		'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']
	print '\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
		(s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
		s.num_peers, state_str[s.state]),
	sys.stdout.flush()
        if s.progress >= 1:
            break
	time.sleep(1)

print h.name(), 'complete'
