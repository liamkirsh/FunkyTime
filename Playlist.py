import wx
#from wx.lib.agw import ultimatelistctrl as ulc
from wx.lib.mixins import listctrl as lc
import DatabaseAPI
import pdb

DEMO = False

### TODO
### ADD BOOLEAN CHECK MARK FOR "SAVE" OR "DELETE"
### Self.media files, media folder, hashed right now
### If boolean is checked, move it over to self.media_files
### convert to mp3 if possible

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
        del_list = []
        while self.ctrl.GetFirstSelected() != -1:
            s = self.ctrl.GetFirstSelected()
            hg_path = self.ctrl.GetItem(itemId=s, col=3).GetText()
            del_list.append(hg_path)

            self.db.deleteSong(hg_path)
            self.ctrl.DeleteItem(s)
            
            self.size -= 1
            self.selectSong(self.selected)

        print 'Deleted list:', del_list
        return del_list

    def addSong(self, song):
        name = song['name']
        artist = song['artist']
        album = song['album']
        thumb = song['thumb']
        path = song['path']

        self.db.addSong(name, artist, album, thumb, path)

        self.ctrl.InsertStringItem(self.size, name)
        self.ctrl.SetStringItem(self.size, 1, artist)
        self.ctrl.SetStringItem(self.size, 2, album)
        self.ctrl.SetStringItem(self.size, 3, path)
        self.size += 1

    def onSelectItem(self, evt):
        #print 'Item selected', evt.Item.Id
        self.highlighted = evt.GetIndex()

    def onDoubleClick(self, evt):
        #print 'DOUBLE CLICK:', evt
        self.onSelectItem(evt)
        self.selectSong(self.highlighted)
        self.callback(self.getCurrentSong())
    
    def getListCtrl(self,panel,w,h, callback):
        #ctrl = wx.ListCtrl(panel, id=-1, size=(w,h), style=wx.LC_REPORT)
        ctrl = StarredListCtrl(panel, (w,h), callback)
        #ctrl = ulc.UltimateListCtrl(panel, size=(w,h), agwStyle=wx.LC_REPORT)
        ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onDoubleClick)
        ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onSelectItem)

        ctrl.InsertColumn(0, 'Song')
        ctrl.InsertColumn(1, 'Artist')
        ctrl.InsertColumn(2, 'Album')
        ctrl.InsertColumn(3, 'File Path')

        ctrl.SetColumnWidth(0, 100)
        ctrl.SetColumnWidth(1, 100)
        ctrl.SetColumnWidth(2, 100)
        ctrl.SetColumnWidth(3, 300)

        pl = self.db.getPlaylist()
        if pl:
            self.size = len(pl)
            for i, song in enumerate(pl):
                ctrl.InsertStringItem(i, song[1])
                ctrl.SetStringItem(i, 1, song[2])
                ctrl.SetStringItem(i, 2, song[3])
                ctrl.SetStringItem(i, 2, song[3])
                ctrl.SetStringItem(i, 3, song[4])
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
        #result = self.ctrl.GetItem(itemId=self.selected, col=3).GetText()
        result = self.ctrl.GetItem(self.selected, 3).GetText()
        return result

    def getNextSong(self):
        self.selectSong(self.selected + 1)
        return self.getCurrentSong()

    def getPrevSong(self):
        self.selectSong(self.selected - 1)
        return self.getCurrentSong()

class StarredListCtrl(wx.ListCtrl, lc.CheckListCtrlMixin):

    def __init__(self, parent, size, callback):
        wx.ListCtrl.__init__(self, parent, -1, size=size, style=wx.LC_REPORT)

        saved = wx.Bitmap('img/yellowstar.png', type=wx.BITMAP_TYPE_PNG)
        notsaved = wx.Bitmap('img/blackstar.png', type=wx.BITMAP_TYPE_PNG)

        lc.CheckListCtrlMixin.__init__(self, check_image=saved, uncheck_image=notsaved, imgsz=(16,16))

        self.callback = callback

    def OnCheckItem(self, index, flag):
        self.callback(index, flag, self.GetItem(index,3).GetText())
