import wx
import wx.media
import Playlist as pl
import server_requests as sr
from functools import reduce
import requests
import sys
import pdb

class Funky_GUI(wx.Frame):

    def __init__(self):
        """Constructor"""
        dw, dh = wx.DisplaySize()
        r1=dw/1210.
        r2=dw/640.
        self.GUI_RESOLUTION=min(r1,r2,1.3)
        wx.Frame.__init__(self, None, title="Funky Time", size=(700*self.GUI_RESOLUTION,450*self.GUI_RESOLUTION))
        self.Bind(wx.EVT_CLOSE, self.close_app)
        self.panel = wx.Panel(self,-1,size=(700*self.GUI_RESOLUTION,450*self.GUI_RESOLUTION))
        self.init_UI()

    def init_UI(self):
        """ """
        self.CreateMenuBar()
        self.playlist = pl.Playlist()
        self.CreateUI()

    def CreateMenuBar(self):
        """ """
        self.menubar = wx.MenuBar()

        menu_file = wx.Menu()

        m_exit = menu_file.Append(-1, "&Exit\tctrl-q", "")
        self.Bind(wx.EVT_MENU, self.close_app, m_exit)

        self.menubar.Append(menu_file, "&File")


##############
        menu_setting = wx.Menu()
        m_setting = menu_setting.Append(-1, "&Setting", "")
        self.Bind(wx.EVT_MENU, self.open_settings_menu, m_setting)

        self.menubar.Append(menu_setting, "&Setting")
###############

        self.SetMenuBar(self.menubar)

    def CreateUI(self):
        """ """
#        self.toolbar0 = wx.ToolBar(self.panel, id=-1)

####################

        try:
            self.mediaPlayer = wx.media.MediaCtrl(self.panel, id=-1, style=wx.SIMPLE_BORDER)
        except NotImplementedError:
            self.Destroy()
            raise

        self.search_bar = wx.SearchCtrl(self.panel, id=-1, value='enter song or band name', size = (256*self.GUI_RESOLUTION,32), style=wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER, self.search_torrents, self.search_bar)

        self.img_play = wx.Bitmap('img/play_button.jpg',type=wx.BITMAP_TYPE_JPEG)
        self.img_pause = wx.Bitmap('img/pause_button.jpg',type=wx.BITMAP_TYPE_JPEG)
        img_next = wx.Bitmap('img/next_button.jpg', type=wx.BITMAP_TYPE_JPEG)
        img_prev = wx.Bitmap('img/prev_button.jpg', type=wx.BITMAP_TYPE_JPEG)
        img_stop = wx.Bitmap('img/stop_button.jpg', type=wx.BITMAP_TYPE_JPEG)
        img_repeat = wx.Bitmap('img/repeat_button.jpg', type=wx.BITMAP_TYPE_JPEG)

        self.isplaying=False
        self.playOrPauseButton = wx.BitmapButton(self.panel, id=-1, bitmap=self.img_play, size=(32,32))
        self.Bind(wx.EVT_BUTTON, self.on_play_button, self.playOrPauseButton)

        self.prevButton = wx.BitmapButton(self.panel, id=-1, bitmap=img_prev, size=(32,32))
        self.Bind(wx.EVT_BUTTON, self.on_prev_button, self.prevButton)

        self.nextButton = wx.BitmapButton(self.panel, id=-1, bitmap=img_next, size=(32,32))
        self.Bind(wx.EVT_BUTTON, self.on_next_button, self.nextButton)

        self.stopButton = wx.BitmapButton(self.panel, id=-1, bitmap=img_stop, size=(32,32))
        self.Bind(wx.EVT_BUTTON, self.on_stop_button, self.stopButton)

        self.repeatButton = wx.BitmapButton(self.panel, id=-1, bitmap=img_repeat, size=(32,32))
        self.Bind(wx.EVT_BUTTON, self.on_repeat_button, self.repeatButton)

        self.listctrl = self.playlist.getListCtrl(self.panel,32*5+256*self.GUI_RESOLUTION+5*10,256*self.GUI_RESOLUTION)

        self.sliderctrl = wx.Slider(self.panel, id=-1, minValue=0, maxValue=60, size=(32*5+256*self.GUI_RESOLUTION+5*10,40*self.GUI_RESOLUTION), style=wx.SL_HORIZONTAL | wx.SL_LABELS )
        self.slidertime = wx.StaticText(self.panel)
        self.Bind(wx.EVT_SLIDER, self.onSeek, self.sliderctrl)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer)
        self.timer.Start(100)

        ######################SIZERS AND STUFF#######################
#        for var in ('playOrPauseButton','prevButton','nextButton','stopButton','repeatButton','search_bar'):
#            COMMAND = 'self.toolbar0.AddControl(self.%s); self.toolbar0.AddSeparator()'%var
#            exec COMMAND

        self.search_sizer = wx.StaticBoxSizer(wx.StaticBox(self.panel, wx.ID_ANY, ""), wx.HORIZONTAL)
        self.button_sizer = wx.StaticBoxSizer(wx.StaticBox(self.panel, wx.ID_ANY, ""), wx.HORIZONTAL)

        self.button_sizer.Add(self.prevButton, 0, wx.LEFT, 5)
        self.button_sizer.Add(self.playOrPauseButton, 0, wx.LEFT, 5)
        self.button_sizer.Add(self.nextButton, 0, wx.LEFT, 5)
        self.button_sizer.Add(self.stopButton, 0, wx.LEFT, 5)
        self.button_sizer.Add(self.repeatButton, 0, wx.LEFT, 5)
        self.search_sizer.Add(self.search_bar, 0, wx.LEFT, 5)

        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        hbox0.Add(self.button_sizer, flag=wx.ALIGN_LEFT, border=8)
        hbox0.Add(self.search_sizer, flag=wx.ALIGN_RIGHT, border=8)

        vbox0 = wx.BoxSizer(wx.VERTICAL)
        vbox0.Add(hbox0)
        vbox0.Add(self.listctrl)
        vbox0.Add(self.sliderctrl)

        self.panel.SetSizer(vbox0)
        vbox0.Fit(self)

#######################
# SLIDER STUFF
#######################
    def onSeek(self, evt):
        offset = self.sliderctrl.GetValue()
        self.mediaPlayer.Seek(offset)

    def onTimer(self, evt):
        offset = self.mediaPlayer.Tell()
        self.sliderctrl.SetValue(offset)

#######################

    def search_torrents(self,event):
        query=self.search_bar.GetValue()
        try:
            TEXT = sr.get_metadata_from_server(query)
        except(requests.exceptions.RequestException):
            print "server not up"
            return
        dlg1 = wx.MessageDialog(None,caption="Confirm Download:", message=str(TEXT) ,style=wx.OK|wx.CANCEL|wx.ICON_EXCLAMATION)
        if dlg1.ShowModal() == wx.ID_OK:
            print('you hit okay')
            dlg1.Destroy()

    def close_app(self,event):
        self.Destroy()


##########################
    def open_settings_menu(self,event):
        print('to be cont')

    def on_play_button(self,event):
        current_song = self.playlist.getCurrentSong()
        if current_song == None: return
        if self.isplaying:
            self.playOrPauseButton.SetBitmapLabel(self.img_play)
            self.isplaying=False
            self.mediaPlayer.Pause()
        else:
            self.playOrPauseButton.SetBitmapLabel(self.img_pause)
            self.isplaying=True
            self.playSong(current_song)

    def on_next_button(self,event):
        self.playSong(self.playlist.getNextSong()) ##
        return 

    def on_prev_button(self,event):
        self.AudioSegment.from_file(self.playlist.getPrevSong(), format= sndhdr.what(pl.getPrevSong())[0]) ##
        return 

    def on_stop_button(self,event):
        return

    def on_repeat_button(self,event):
        return

    def button_download(self,event):
        return #xxx

#    def onBrowse(self, event):
#        """
#        Opens file dialog to browse for music
#        """
#        wildcard = "MP3 (*.mp3)|*.mp3|"     \
#                   "WAV (*.wav)|*.wav"
#        dlg = wx.FileDialog(
#            self, message="Choose a file",
#            defaultDir=self.currentFolder, 
#            defaultFile="",
#            wildcard=wildcard,
#            style=wx.OPEN | wx.CHANGE_DIR
#            )
#        if dlg.ShowModal() == wx.ID_OK:
#            path = dlg.GetPath()
#            self.currentFolder = os.path.dirname(path)
#            self.loadMusic(path)
#        dlg.Destroy()

    def playSong(self,current_song):
        try:
            if self.mediaPlayer.Play():
                wx.MessageBox("Unable to Play media : Unsupported format?",
                              "ERROR",
                              wx.ICON_ERROR | wx.OK)
            else:
                self.mediaPlayer.SetInitialSize()
                self.GetSizer().Layout()
                self.sliderctrl.SetRange(0, self.mediaPlayer.Length())
        except:
            if not self.mediaPlayer.Load(current_song):
                wx.MessageBox("Unable to load %s: Unsupported format?" % current_song,
                              "ERROR",
                              wx.ICON_ERROR | wx.OK)
            else:
                self.mediaPlayer.SetInitialSize()
                self.GetSizer().Layout()
                self.sliderctrl.SetRange(0, self.mediaPlayer.Length())

###########################

def __main__():
    app = wx.App()
    app.frame = Funky_GUI()
    app.frame.Center()
    app.frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    __main__()
