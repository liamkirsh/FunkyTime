import wx
import DatabaseAPI
import pdb

DEMO = False

class Playlist:
    def __init__(self, hbg = 'LIGHT BLUE', nbg = 'WHITE'): 
        self.db = DatabaseAPI.Database()
        self.size = -1
        self.selected = -1
        self.highlighted = -1
        self.hbg = hbg
        self.nbg = nbg
        self.callback = None

        if DEMO:
            self.db.empty()
            self.db.create()
            self.db.loadDemo()

    def removeSelected(self):
        name = self.ctrl.GetItemString(self.selected)
        album = self.ctrl.GetItemString(self.selected, 1)
        path = self.ctrl.GetItemString(self.selected, 2)
        print 'Attempting to remove', name, album, path
        self.selectSong(self.selected)

    def addSong(self, song):
        name = song['name']
        album = song['album']
        path = song['path']

        self.db.addSong(name, album, path)

        self.ctrl.InsertStringItem(self.size, name)
        self.ctrl.SetStringItem(self.size, 1, album)
        self.ctrl.SetStringItem(self.size, 2, path)
        self.size += 1

    def onSelectItem(self, evt):
        #print 'Item selected', evt.Item.Id
        self.highlighted = evt.Item.Id

    def onDoubleClick(self, evt):
        #print 'DOUBLE CLICK:', evt
        self.selectSong(self.highlighted)
        self.callback()
    
    def getListCtrl(self,panel,w,h):
        ctrl = wx.ListCtrl(panel, id=-1, size=(w,h), style=wx.LC_REPORT)
        ctrl.Bind(wx.EVT_LEFT_DCLICK, self.onDoubleClick)
        ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onSelectItem)

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

        self.getCurrentSong()

        return ctrl

    def selectSong(self, index):
        if self.size <= 0:
            self.size = -1
            self.selected = -1
            return

        if index < 0:
            index = self.size - 1
        if index >= self.size:
            index = 0

        if self.selected >= 0:
            self.ctrl.SetItemBackgroundColour(self.selected, self.nbg)

        self.selected = index

        if self.selected >= 0:
            self.ctrl.SetItemBackgroundColour(index, self.hbg)


    def getCurrentSong(self):
        if self.selected < 0:
            return None
        result = self.ctrl.GetItem(itemId=self.selected, col=2).GetText()
        print 'returning', result
        return result

    def getNextSong(self):
        self.selectSong(self.selected + 1)
        return self.getCurrentSong()

    def getPrevSong(self):
        self.selectSong(self.selected - 1)
        return self.getCurrentSong()

