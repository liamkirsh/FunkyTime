import requests
#import urllib2
import libtorrent as lt
import time
import sys
import os
import shutil
import re

ses = lt.session()
ses.listen_on(6881, 6891)

def audio_match(title, f):
	extension = f.split(".")[-1]
	if extension in ["mp3", "flac", "m4a", "wav", "wma"]:
		f = f[:-1]
	title = re.sub(r"\W+", "", title)
	f = re.sub(r"\W+", "", f)
	return (title.lower() in f.lower()) or (f.lower() in title.lower())

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
the_hash = sys.argv[3]
#selection
admitted = []
admitted_fnames = []
i=0
done_with_it = False
for f in info.files():
    if audio_match(REQUIRED, f.path):
	if not done_with_it:
        	admitted.append(i)
        	admitted_fnames.append(f.path)
        	print f.path
        i += 1
        done_with_it = True
    else:
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

if not os.path.exists('outbox'):
    os.makedirs('outbox')
dump_dir = os.path.join('downloads', the_hash)
if not os.path.exists(dump_dir):
    os.makedirs(dump_dir)
for fname in admitted_fnames:
    shutil.move(os.path.join('downloads',fname), dump_dir)
shutil.move(dump_dir, 'outbox')
