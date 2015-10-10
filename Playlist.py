import wx
import DatabaseAPI

APP_EXIT = 1

class Playlist:
    def __init__(self):
        self.db = DatabaseAPI.Database()
        self.playlist = []

    def findSongAlbum(self, song_name):
        return "Generic Album Name"

    def downloadFile(self, song_name, album_name):
        return None

    def addSongWithAlbum(self, song):
        self.db.addSongToPlaylist(song, 'default')
        self.playlist.append(song)

    def getListCtrl(self,panel,w,h):
        return wx.ListCtrl(panel, id=-1, size=(w,h), style=wx.LC_REPORT)

    def getCurrentSong(self):
        return './Music/beet_5_1.wav'

    def getNextSong(self):
        return './Music/beet_5_1.wav'

