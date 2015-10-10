import sqlite3

no_table_ex = Exception('Playlist Table does not exist.')
yes_table_ex = Exception('Playlist Table does exist.')

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
        else:
            raise no_table_ex

    def create(self):
        if not self.exists():
            self.conn.cursor().execute('CREATE TABLE Playlist (song_name varchar(500), album_name varchar(500), file_path varchar(500));')
        else:
            raise yes_table_ex

    def loadDemo(self):
        if self.exists():
            for i in range(1, 5):
                self.addSong('Beet 5.' + str(i), 'Beet Symp', './beet_5_1.wav')
        else:
            raise no_table_ex

    def addSong(self, song_name, album_name, file_path):
        if self.exists():
            c = self.conn.cursor()
            c.execute('INSERT INTO Playlist (song_name, album_name, file_path) VALUES (?, ?, ?);', (song_name, album_name, file_path))
            self.conn.commit()
        else:
            raise no_table_ex

    def getPlaylist(self):
        if self.exists():
            return list(self.conn.cursor().execute('SELECT * FROM Playlist;'))
        raise no_table_ex
