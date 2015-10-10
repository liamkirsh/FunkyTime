import sqlite3
import pdb

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('local.db')

        if not self.exists():
            self.create()

    def close(self):
        self.conn.close()

    def exists(self):
        result = self.conn.cursor().execute("SELECT * FROM sqlite_master WHERE type = 'table' and name='Playlist';").fetchone()
        return result is not None

    def empty(self):
        if self.exists():
            self.conn.cursor().execute("DROP TABLE Playlist;")

    def create(self):
        self.conn.cursor().execute('CREATE TABLE Playlist (song_name varchar(500), album_name varchar(500), file_path varchar(500));')

    def loadDemo(self):
        if self.exists():
            for i in range(1, 5):
                self.add_song('Beet 5.' + str(i), 'Beet Symp', './beet_5_1.wav')

    def addSong(self, song_name, album_name, file_path):
        if self.exists():
            c = self.conn.cursor()
            c.execute('INSERT INTO Playlist (song_name, album_name, file_path) VALUES (?, ?, ?);', (song_name, album_name, file_path))
            self.conn.commit()

    def getPlaylist(self):
        if self.exists():
            return list(self.conn.cursor().execute('SELECT * FROM Playlist;'))
        return None
