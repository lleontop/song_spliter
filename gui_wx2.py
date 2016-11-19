import wx
import os
from pydub import AudioSegment

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.dirname=''
        self.sound = None

        # A "-1" in the size parameter instructs wxWidgets to use the default size.
        # In this case, we select 200px width and the default height.
        wx.Frame.__init__(self, parent, title=title, size=(200,-1))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar() # A Statusbar in the bottom of the window

        self.setup_menu()        
        
        self.file_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.audio_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.audio_sizer.Add(wx.StaticText(self, label="Audio: "), 0)
        self.audio_sizer.Add(wx.StaticText(self, label="Select audio file...",style=wx.SIMPLE_BORDER), 1, wx.EXPAND)
        self.audio_sizer.Add(wx.Button(self, -1, "Select"), 0)
        
        self.time_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.time_sizer.Add(wx.StaticText(self, label="Times: "), 0)
        self.time_sizer.Add(wx.StaticText(self, label="Select time file...",style=wx.SIMPLE_BORDER), 1, wx.EXPAND)
        self.time_sizer.Add(wx.Button(self, -1, "Select"), 0)
        
        self.file_sizer.Add(self.audio_sizer, 1, wx.EXPAND)
        self.file_sizer.Add(self.time_sizer, 1, wx.EXPAND)
        
#         self.buttons = []
#         for i in range(0, 6):
#             self.buttons.append(wx.Button(self, -1, "Button &"+str(i)))
#             self.file_sizer.Add(self.buttons[i], 1, wx.EXPAND)

        # Use some sizers to see layout options
        self.sizer = wx.BoxSizer(wx.VERTICAL)        
        self.sizer.Add(self.file_sizer, 0, wx.EXPAND)
        self.sizer.Add(self.control, 1, wx.EXPAND)
        #Layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
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
            #self.control.SetValue(f.read())
            #f.close()
        dlg.Destroy()
        
        dialog = wx.ProgressDialog("A progress box", "Time remaining", 100, style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_APP_MODAL)
        self.sound = AudioSegment.from_file(filename)
        dialog.Pulse()
        dialog.Destroy()

app = wx.App(False)
frame = MainWindow(None, "Sample editor")
app.MainLoop()