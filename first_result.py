import sys
from KickassAPI import Search, Latest, User, CATEGORY, ORDER

for t in Search(sys.argv[1], category=CATEGORY.MUSIC, order=ORDER.SEED):
    print "TITLE:"
    print t.name
    print "LINK"
    print t.download_link
    break

