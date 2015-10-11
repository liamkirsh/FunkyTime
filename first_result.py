import sys
import json
from KickassAPI import Search, Latest, User, CATEGORY, ORDER

j = json.loads(sys.argv[1])
q = Search(j["artist"] + " " + j["album"], category=CATEGORY.MUSIC, order=ORDER.SEED).list()
if len(q) == 0:
	q = Search(j["artist"] + " " + j["title"], category=CATEGORY.MUSIC, order=ORDER.SEED).list()
# If still can't find any results
if len(q) == 0:
	print
	sys.stdout.flush()
	sys.exit(0)
# Given that results are found:
for t in q:
	print 'http://' + t.download_link[2:]
	sys.stdout.flush()
	sys.exit(0)

