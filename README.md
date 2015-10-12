# PopcornTimeForMusic

## 2015 Cal Hacks Project

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
Set up a web server with Node.js and Python 2.7 installed. Install the following Node modules:
* body-parser
* express
* http

Open ports 22 and 80.

Set up the directory structure this way:
/MusicTime/MusicTime.js
/MusicTime/scripts/bittorrent.py <-- selective_client.py in this repo
/MusicTime/scripts/KAT.py <-- first_result.py in this repo
/MusicTime/scripts/KickassAPI.py
/Musictime/scripts/Spotify.py

Run sudo node MusicTime.js. You should see the message "Express server listening on port 80."
