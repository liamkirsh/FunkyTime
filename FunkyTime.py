import wx
import wx.media, wx.animate
import Playlist as pl
import server_requests as sr
from functools import reduce
from glob import glob
import AudioConversion as ac
import requests
import time
import sys,os
import json
import pdb

STOP = -1
PAUSE = 0
PLAY = 1

class Funky_GUI(wx.Frame):

    def __init__(self):
        """Constructor"""
        dw, dh = wx.DisplaySize()
        r1=dw/1210.
        r2=dw/640.
        self.GUI_RESOLUTION=min(r1,r2,1.3)
        self.mediaFolder = os.getcwd()
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

        m_add = menu_file.Append(-1, "&Add File\tctrl-o", "")
        self.Bind(wx.EVT_MENU, self.add_file, m_add)

        m_save = menu_file.Append(-1, "&Save File\tctrl-s", "")
        self.Bind(wx.EVT_MENU, self.save_file, m_save)

        m_delete = menu_file.Append(-1, "&Delete File\tctrl-d", "")
        self.Bind(wx.EVT_MENU, self.delete_file, m_delete)

        m_set_directory = menu_file.Append(-1, "&Set Media Directory\tctrl-f", "")
        self.Bind(wx.EVT_MENU, self.onBrowse, m_set_directory)

        m_exit = menu_file.Append(-1, "&Exit\tctrl-q", "")
        self.Bind(wx.EVT_MENU, self.close_app, m_exit)

#############
        menu_edit = wx.Menu()

        m_play_pause = menu_edit.Append(-1, "&Play/Pause\tctrl-p", "")
        self.Bind(wx.EVT_MENU, self.on_play_button, m_play_pause)

        m_prev = menu_edit.Append(-1, "&Previous Track\tctrl-left", "")
        self.Bind(wx.EVT_MENU, self.on_prev_button, m_prev)

        m_next = menu_edit.Append(-1, "&Next Track\tctrl-right", "")
        self.Bind(wx.EVT_MENU, self.on_next_button, m_next)

        m_volUp = menu_edit.Append(-1, "&Increase Volume\tctrl-up", "")
        self.Bind(wx.EVT_MENU, self.IncreaseVol, m_volUp)

        m_volDown = menu_edit.Append(-1, "&Decrease Volume\tctrl-down", "")
        self.Bind(wx.EVT_MENU, self.DecreaseVol, m_volDown)

#        m_shuffle = menu_edit.Append(-1, "&Shuffle\tctrl-h", "")
#        self.Bind(wx.EVT_MENU, self.shuffle, m_shuffle)


##############
        menu_setting = wx.Menu()

        m_setting = menu_setting.Append(-1, "&Setting", "")
        self.Bind(wx.EVT_MENU, self.open_settings_menu, m_setting)

###############
        self.menubar.Append(menu_file, "&File")
        self.menubar.Append(menu_edit, "&Edit")
        self.menubar.Append(menu_setting, "&Setting")

        self.SetMenuBar(self.menubar)

    def CreateUI(self):
        """ """
        self.toolbar0 = wx.ToolBar(self.panel, id=-1)

####################

        if sys.platform == 'linux2':
            self.backend = wx.media.MEDIABACKEND_GSTREAMER
        elif sys.platform == 'darwin':
            self.backend = wx.media.MEDIABACKEND_QUICKTIME
        else:
            self.backend = wx.media.MEDIABACKEND_WMP10

        try:
            self.mediaPlayer = wx.media.PreMediaCtrl()
            ok = self.mediaPlayer.Create(self.panel, szBackend=self.backend)
            if not ok:
                raise NotImplementedError
            self.mediaPlayer.PostCreate(self.mediaPlayer)
            self.Bind(wx.media.EVT_MEDIA_LOADED, self.onMediaLoad)
        except NotImplementedError:
            self.Destroy()
            raise

        self.search_bar = wx.TextCtrl(self.panel, id=-1, value='enter song or band name', size = (256*self.GUI_RESOLUTION,32), style=wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER, self.search_torrents, self.search_bar)

        self.img_play = wx.Bitmap('img/play_button.jpg',type=wx.BITMAP_TYPE_JPEG)
        self.img_pause = wx.Bitmap('img/pause_button.jpg',type=wx.BITMAP_TYPE_JPEG)
        img_next = wx.Bitmap('img/next_button.jpg', type=wx.BITMAP_TYPE_JPEG)
        img_prev = wx.Bitmap('img/prev_button.jpg', type=wx.BITMAP_TYPE_JPEG)
        img_stop = wx.Bitmap('img/stop_button.jpg', type=wx.BITMAP_TYPE_JPEG)
        img_repeat = wx.Bitmap('img/repeat_button.jpg', type=wx.BITMAP_TYPE_JPEG)

        self.isplaying=STOP
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

        self.listctrl = self.playlist.getListCtrl(self.panel,32*5+256*self.GUI_RESOLUTION+5*10,256*self.GUI_RESOLUTION, self.on_check_song)
        self.playlist.callback = self.on_double_click

        self.sliderctrl = wx.Slider(self.panel, id=-1, minValue=0, maxValue=60, size=(32*5+256*self.GUI_RESOLUTION+5*10,40*self.GUI_RESOLUTION), style=wx.SL_HORIZONTAL | wx.SL_LABELS )
        self.slidertime = wx.StaticText(self.panel)
        self.Bind(wx.EVT_SLIDER, self.onSeek, self.sliderctrl)

        self.mediaPlayer.SetVolume(.5)
        self.volumectrl = wx.Slider(self.panel, size=(40*self.GUI_RESOLUTION,40*self.GUI_RESOLUTION), style=wx.SL_VERTICAL | wx.SL_INVERSE | wx.SL_LABELS)
        self.volumectrl.SetRange(0, 100)
        self.volumectrl.SetValue(50)
        self.Bind(wx.EVT_SLIDER, self.onSetVolume, self.volumectrl)

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
        self.search_sizer.Add(self.search_bar, wx.LEFT, 5)

        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        hbox0.Add(self.button_sizer, flag=wx.ALIGN_LEFT, border=8)
        hbox0.Add(self.search_sizer, flag=wx.ALIGN_RIGHT, border=8)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(self.sliderctrl)
        hbox1.Add(self.volumectrl)

        vbox0 = wx.BoxSizer(wx.VERTICAL)
        vbox0.Add(hbox0)
        vbox0.Add(self.listctrl, flag=wx.ALL, border=8)
        vbox0.Add(hbox1)
        vbox0.Add(self.mediaPlayer)

        self.panel.SetSizer(vbox0)
        vbox0.Fit(self)

#######################
# SLIDER STUFF
#######################
    def onSeek(self, evt):
        offset = self.sliderctrl.GetValue()
        self.mediaPlayer.Seek(offset * 1000)

    def onTimer(self, evt):
        offset = self.mediaPlayer.Tell()
        self.sliderctrl.SetValue(offset // 1000 )

#######################

    def search_torrents(self,event):
        query=self.search_bar.GetValue()
        if self.search_media_for_file(query): return
        try:
            meta_data = sr.get_metadata_from_server(query)
            if meta_data==None:
                Text="No Torrent Found"
                dlg1 = wx.MessageDialog(None,caption="Confirm Download:", message=str(Text) ,style=wx.OK|wx.ICON_EXCLAMATION)
                if dlg1.ShowModal() == wx.ID_OK:
                    dlg1.Destroy()
                    return
            open_meta_data = json.loads(meta_data)
        except(requests.exceptions.RequestException):
            print "server not up"
            return
        Text = "Was this the file you were looking for?\nSong: " + open_meta_data['title'] + "\nAlbum: " + open_meta_data['album'] + "\nArtist: " + open_meta_data['artist']
        dlg1 = wx.messageDialog(None,caption="Confirm Download:", message=str(Text) ,style=wx.OK|wx.CANCEL|wx.ICON_EXCLAMATION)
        if dlg1.ShowModal() == wx.ID_OK:
            download_hash = sr.init_download_on_server(meta_data)
            dlg1.Destroy()
            download_hash = sr.init_download_on_server(meta_data)
        else: return
        data = None
        while data is None:
            data,ctype = sr.poll_server(download_hash)
            time.sleep(2)
        if ctype == 'audio/mpeg':
            filepath = 'music/'+open_meta_data['title']+'.mp3'
            fileout = open(filepath, 'wb')
            fileout.write(data)
            finalpath = ac.convert_to_wav(filepath,outputpath=os.getcwd()+'/music/'+str(hash(filepath))+'.wav')
            open_meta_data['path'] = finalpath
            open_meta_data['name'] = open_meta_data['title']
            os.remove(filepath)
            self.playlist.addSong(open_meta_data)
        if ctype == 'audio/m4a':
            filepath = 'music/'+open_meta_data['title']+'.m4a'
            fileout = open(filepath, 'wb')
            fileout.write(data)
            finalpath = ac.convert_to_wav(filepath,outputpath=os.getcwd()+'/music/'+str(hash(filepath))+'.wav')
            open_meta_data['path'] = finalpath
            open_meta_data['name'] = open_meta_data['title']
            os.remove(filepath)
            self.playlist.addSong(open_meta_data)
        if ctype == 'audio/x-flac':
            filepath='music/'+open_meta_data['title']+'.flac'
            fileout = open(filepath, 'wb')
            fileout.write(data)
            finalpath = ac.convert_to_wav(filepath,outputpath=os.getcwd()+'/music/'+str(hash(filepath))+'.wav')
            open_meta_data['path'] = finalpath
            open_meta_data['name'] = open_meta_data['title']
            os.remove(filepath)
            self.playlist.addSong(open_meta_data)
        if ctype == 'audio/x-wav':
            filepath = 'music/'+open_meta_data['title']+'.wav'
            fileout = open(filepath, 'wb')
            fileout.write(data)
            open_meta_data['path'] = filepath
            open_meta_data['name'] = open_meta_data['title']
            self.playlist.addSong(open_meta_data)

    def onBrowse(self, event):
        """git 
        Opens file dialog to browse for music
        """
        wildcard = "/"
        dlg = wx.DirDialog(self.panel, "choose media directory:", defaultPath=self.mediaFolder ,style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if not path.endswith('/'): path += '/'
            self.mediaFolder = path
        dlg.Destroy()

    def save_file(self, event):
        pass

    def delete_file(self, event):
        files_deleted = self.playlist.removeSelected()
        for dfile in files_deleted:
            if dfile.split('/')[-2] != 'music': continue
            os.remove(dfile)

    def add_file(self, event):
        """
        Opens file dialog to browse for music
        """
        wildcard = """MP3 (*.mp3)|*.mp3| WAV (*.wav)|*.wav| FLAC (*.flac)|*.flac| ALL (*)|*"""
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.mediaFolder,
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if path.split('.')[-1] != 'wav':
                final_path = ac.convert_to_wav(path,outputpath=os.getcwd()+'/music/'+str(hash(path))+'.wav')
            else: final_path = path
            name = path.split('/')[-1].split('.')[0]
            album = path.split('/')[-2]
            self.playlist.addSong({'path':final_path,'name':name,'album':album, 'artist':'None','thumb':'None'})
        dlg.Destroy()

##########################Menu Files##############################

    def close_app(self,event):
        self.Destroy()

    def IncreaseVol(self,event):
        vi = int(self.volumectrl.GetValue())
        if vi+1 <= 100: self.volumectrl.SetValue(vi+1)
        else: self.volumectrl.SetValue(vi)
        self.onSetVolume(event)


    def DecreaseVol(self,event):
        vi = int(self.volumectrl.GetValue())
        if vi-1 >= 0: self.volumectrl.SetValue(vi-1)
        else: self.volumectrl.SetValue(vi)
        self.onSetVolume(event)

##########################
    def open_settings_menu(self,event):
        print('to be cont')

    def on_double_click(self, song):
        self.isplaying=PLAY
        self.playOrPauseButton.SetBitmapLabel(self.img_pause)
        self.playSong(song)

    def on_check_song(self, index, flag, file_path):
        print 'Check', index, ',', flag, ',', file_path

    def on_play_button(self,event):
        current_song = self.playlist.getCurrentSong()
        if current_song == None: return
        if self.isplaying == PLAY:
            self.playOrPauseButton.SetBitmapLabel(self.img_play)
            self.isplaying=PAUSE
            self.mediaPlayer.Pause()
        elif self.isplaying == PAUSE:
            self.playOrPauseButton.SetBitmapLabel(self.img_pause)
            self.isplaying=PLAY
            self.mediaPlayer.Play()
        else:
            self.playOrPauseButton.SetBitmapLabel(self.img_pause)
            self.isplaying=PLAY
            self.playSong(current_song)


    def on_next_button(self,event):
        next_song = self.playlist.getNextSong()
        if next_song:
            self.playSong(next_song)

    def on_prev_button(self,event):
        prev_song = self.playlist.getPrevSong()
        if prev_song:
            self.playSong(prev_song)

    def on_stop_button(self,event):
        self.isplaying=STOP
        self.playOrPauseButton.SetBitmapLabel(self.img_play)
        self.mediaPlayer.Stop()

    def on_repeat_button(self,event):
        return

    def button_download(self,event):
        return #xxx

    def onMediaLoad(self, evt):
        self.mediaPlayer.Play()

    def playSong(self, current_song):
        if not self.mediaPlayer.Load(current_song):
            wx.MessageBox("Unable to load %s: Unsupported format?" % current_song,
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        self.sliderctrl.SetRange(0, self.mediaPlayer.Length() // 1000)

    def search_media_for_file(self, query):
        """return bool of wather or not file is found, if file is found pass it to playlist"""
        print(self.mediaFolder)
        for tup in os.walk(self.mediaFolder):
            for mfile in tup[2]:
                if mfile.endswith('/'): continue
                song = mfile.split('.')[0]
                if query not in song: continue
                print("sucess")
                album = tup[0].split('/')[-2]
                TEXT = "Is this the song you where searching for?\nSong: " + song + "\nAlbum: " + album
                dlg1 = wx.MessageDialog(None,caption="Confirm Download:", message=str(TEXT) ,style=wx.OK|wx.CANCEL|wx.ICON_EXCLAMATION)
                if dlg1.ShowModal() == wx.ID_OK:
                    directory = tup[0]
                    if not directory.endswith('/'): directory += '/'
                    path = directory+mfile
                    final_path = ac.convert_to_wav(path,outputpath=os.getcwd()+'/music/'+str(hash(path))+'.wav')
                    self.playlist.addSong({'path':final_path,'name':song,'album':album, 'artist':'None','thumb':'None'})
                    dlg1.Destroy()
                    return True
        return False

    def onSetVolume(self, event):
        self.mediaPlayer.SetVolume(float(self.volumectrl.GetValue())/100.)

#    def shuffle(self, event):
#        shuffle(self.playlist.db.getPlaylist)





###########################

def __main__():
    app = wx.App()
    app.frame = Funky_GUI()
    app.frame.Center()
    app.frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    __main__()
