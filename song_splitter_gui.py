import wx
import os
import song_splitter

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.dirname=''
        self.sound = None

        # A "-1" in the size parameter instructs wxWidgets to use the default size.
        # In this case, we select 200px width and the default height.
        wx.Frame.__init__(self, parent, title=title, size=(700,700))        
        self.CreateStatusBar() # A Statusbar in the bottom of the window

        self.setup_menu()
        self.set_main_layout()        
        
        self.Show()

    def setup_menu(self):
        
        # Setting up the file menu.
        file_menu= wx.Menu()
        file_menu_open = file_menu.Append(wx.ID_OPEN, "&Open"," Open the file to split")
        self.Bind(wx.EVT_MENU, self.OnOpen, file_menu_open)
         
        file_menu_about= file_menu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, file_menu_about)
        
        file_menu_exit = file_menu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        self.Bind(wx.EVT_MENU, self.OnExit, file_menu_exit)

        about_menu = wx.Menu()
        about_menu_about = about_menu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, about_menu_about)
 
        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(file_menu,"&File") # Adding the "file_menu" to the MenuBar
        menuBar.Append(about_menu,"&Help") # Adding the "file_menu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
       
    
    def set_main_layout(self):
        
        self.create_audio_file_selector()
        self.create_time_file_selector()
        self.create_processing_button()
        
        self.select_files_sizer = wx.BoxSizer(wx.VERTICAL)
        self.select_files_sizer.Add(self.audio_row, 1, wx.EXPAND)
        self.select_files_sizer.Add(self.time_sizer, 1, wx.EXPAND)
        
        self.files_row = wx.BoxSizer(wx.HORIZONTAL)
        self.files_row.Add(self.select_files_sizer, 1, wx.EXPAND)
        self.files_row.Add(self.start_processing_button, 0, wx.EXPAND)
        
        
        self.text_times = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        
        # Use some sizers to see layout options
        self.sizer = wx.BoxSizer(wx.VERTICAL)        
        self.sizer.Add(self.files_row, 0, wx.EXPAND)
        self.sizer.Add(self.text_times, 1, wx.EXPAND)
        #Layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        # self.sizer.Fit(self)
        self.SetBackgroundColour(wx.WHITE)
     
    def create_audio_file_selector(self):
                
        def on_audio_select(e):
            """ Open a file"""
            dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "MP3 files (*.mp3)|*.mp3|M4A files (*.m4a)|*.m4a|All files (*.*)|*.*", wx.OPEN)
            if dlg.ShowModal() == wx.ID_OK:
                self.filename = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                self.audio_filename = os.path.join(self.dirname, self.filename)
                self.audio_path_label.SetLabel(self.audio_filename)
            dlg.Destroy()
        
        self.audio_label = wx.StaticText(self, label="Audio: ")
        self.audio_path_label = wx.StaticText(self, label="Select audio file...",style=wx.SIMPLE_BORDER|wx.ST_ELLIPSIZE_MIDDLE)
        self.audio_button = wx.Button(self, -1, "Select")
        
        self.Bind(wx.EVT_BUTTON, on_audio_select, self.audio_button)
        
        self.audio_row = wx.BoxSizer(wx.HORIZONTAL)
        self.audio_row.Add(self.audio_label, 0)
        self.audio_row.Add(self.audio_path_label, 1, wx.EXPAND)
        self.audio_row.Add(self.audio_button, 0)
    
    def create_time_file_selector(self):
        
        def on_time_select(e):
            """ Open a file"""
            dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "TXT files (*.txt)|*.txt|All files (*.*)|*.*", wx.OPEN)
            if dlg.ShowModal() == wx.ID_OK:
                self.filename = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                self.time_filename = os.path.join(self.dirname, self.filename)
                self.time_path_label.SetLabel(self.time_filename)
            dlg.Destroy()
        
        self.time_label = wx.StaticText(self, label="Times: ")
        self.time_path_label = wx.StaticText(self, label="Select time file...",style=wx.SIMPLE_BORDER|wx.ST_ELLIPSIZE_MIDDLE)
        self.time_button = wx.Button(self, -1, "Select")
        
        self.Bind(wx.EVT_BUTTON, on_time_select, self.time_button)
        
        self.time_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.time_sizer.Add(self.time_label, 0)
        self.time_sizer.Add(self.time_path_label, 1, wx.EXPAND)
        self.time_sizer.Add(self.time_button, 0)
 
    def create_processing_button(self):
        def on_start_processing(e):
            song_splitter.main(self.audio_filename, self.time_filename)
        self.start_processing_button = wx.Button(self, -1, "Start processing")        
        self.Bind(wx.EVT_BUTTON, on_start_processing, self.start_processing_button)
                    
    def OnAbout(self,e):
        # Create a message dialog box
        dlg = wx.MessageDialog(self, " A sample editor \n in wxPython", "About Sample Editor", wx.OK)
        dlg.ShowModal() # Shows it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.
    
    def OnOpen(self,e):
        """ Open a file"""
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "MP3 files (*.mp3)|*.mp3|M4A files (*.m4a)|*.m4a|All files (*.*)|*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            filename = os.path.join(self.dirname, self.filename)
            self.control.SetValue(filename)
            #self.control.SetValue(f.read())
            #f.close()
        dlg.Destroy()
        
#         dialog = wx.ProgressDialog("A progress box", "Time remaining", 100, style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_APP_MODAL)
#         self.sound = AudioSegment.from_file(filename)
#         dialog.Pulse()
#         dialog.Destroy()

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

if __name__ == '__main__':    
    app = wx.App(False)
    frame = MainWindow(None, "Song Splitter")
    app.MainLoop()