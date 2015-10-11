import wx
import DatabaseAPI
import pdb

DEMO = True

class Playlist:
    def __init__(self, hbg = 'LIGHT BLUE', nbg = 'WHITE'): 
        self.db = DatabaseAPI.Database()
        self.size = -1
        self.selected = -1
        self.hbg = hbg
        self.nbg = nbg

        if DEMO:
            self.db.empty()
            self.db.create()
            self.db.loadDemo()

    def addSong(self, song):
        name = song['name']
        album = song['album']
        path = song['path']

        self.db.addSong(name, album, path)

        self.ctrl.InsertStringItem(self.size, name)
        self.ctrl.SetStringItem(self.size, 1, album)
        self.ctrl.SetStringItem(self.size, 2, path)
        self.size += 1
    
    def getListCtrl(self,panel,w,h):
        ctrl = wx.ListCtrl(panel, id=-1, size=(w,h), style=wx.LC_REPORT)

        ctrl.InsertColumn(0, 'Song')
        ctrl.InsertColumn(1, 'Album')
        ctrl.InsertColumn(2, 'File Path')
        
        pl = self.db.getPlaylist()
        if pl:
            self.size = len(pl)
            for i, song in enumerate(pl):
                ctrl.InsertStringItem(i, song[0])
                ctrl.SetStringItem(i, 1, song[1])
                ctrl.SetStringItem(i, 2, song[2])

        self.ctrl = ctrl

        if self.size > 0:
            self.selectSong(0)

        return ctrl

    def selectSong(self, index):
        if 0 <= index and index < self.size:

            if self.selected >= 0:
                self.ctrl.SetItemBackgroundColour(self.selected, self.nbg)

            self.ctrl.SetItemBackgroundColour(index, self.hbg)

            self.selected = index
        else:
            raise Exception('Out of bounds.')

    def getCurrentSong(self):
        return './FUCK.mp3' ##xxx 

    def getNextSong(self):
        return './Music/beet_5_1.wav'

    def getPrevSong(self):
        return './Music/beet_5_1.wav'

