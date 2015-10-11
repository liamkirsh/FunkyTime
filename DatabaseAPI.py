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
            self.addSong('German March', 'EdGuy Advantasia', '/Users/isak/Projects/FunkyTime/song.wav')
            self.addSong('Bass Wave', 'EdGuy Advantasia', '/Users/isak/Projects/FunkyTime/bass.wav')
        else:
            raise no_table_ex

    def addSong(self, song_name, album_name, file_path):
        if self.exists():
            c = self.conn.cursor()
            self.deleteSong(file_path)
            c.execute('INSERT INTO Playlist (song_name, album_name, file_path) VALUES (?, ?, ?);', (song_name, album_name, file_path))
            self.conn.commit()
        else:
            raise no_table_ex

    def deleteSong(self, file_path):
        if self.exists():
            c = self.conn.cursor()
            c.execute("DELETE FROM Playlist WHERE file_path = ?;", (file_path,))
            self.conn.commit()
        else:
            raise no_table_ex

    def getPlaylist(self):
        if self.exists():
            return list(self.conn.cursor().execute('SELECT * FROM Playlist;'))
        raise no_table_ex

db = Database()
