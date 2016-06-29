# FunkyTime 

## Popcorn Time for Music -- Cal Hacks 2.0 Project

http://devpost.com/software/funkytime

### Contributors
* Liam
* Omer
* Long
* Kevin
* Isak
* John Cena

### Dank Memes
* 4.0
* EECS Masterrace

### How to use
#### Server
Set up a web server with Node.js and Python 2.7 installed. Install the following Node modules:
* body-parser
* express
* http

Open incoming ports 22 and 80 and outgoing ports 6881 and 6891.

Set up the directory structure this way:  

/FunkyTime/FunkyTime.js  
/FunkyTime/scripts/bittorrent.py  
/FunkyTime/scripts/KAT.py  
/FunkyTime/scripts/KickassAPI.py  
/FunkyTime/scripts/Spotify.py  

Run sudo node FunkyTime.js. You should see the message "Express server listening on port 80." You can run app/server_requests.py from the commandline to test your server -- just pass a single string as a parameter containing the track name and artist.
#### Client
Run python FunkyTime.py in the app directory. You will need Python 2.7 and the wxPython and pydub modules installed. You may also need ffmpeg installed on your system to use the pydub module.
