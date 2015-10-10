import sys
from KickassAPI import Search, Latest, User, CATEGORY, ORDER

for t in Search(sys.argv[1], category=CATEGORY.MUSIC, order=ORDER.SEED):
    #print "TITLE:"
    #print t.name
    #print "LINK"
    print 'http://' + t.download_link[2:]
    sys.stdout.flush()
    sys.exit(0)

