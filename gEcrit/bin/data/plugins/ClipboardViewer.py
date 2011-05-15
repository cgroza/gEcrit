
from data.plugins.categories import Passive
import yapsy.IPlugin
import wx

class ClipboardViewer(wx.Frame, Passive, yapsy.IPlugin.IPlugin):
    def __init__(self):
        self.name = "Clipboard Viewer"

    def Init(self, parent):
        self.parent = parent
        wx.Frame.__init__(self, self.parent)

        self.main_panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.clip_view_descr = wx.StaticText(self.main_panel, -1,
                                 "Clipboard Contents:", size = (-1, -1))
        
        self.clip_view = wx.TextCtrl(self.main_panel, -1, 
                                                style = wx.TE_MULTILINE)

        self.update_clp = wx.Button(self.main_panel, -1, "Update Clipboard")
        self.refresh_view = wx.Button(self.main_panel, -1, "Refresh")

        self.update_clp.Bind(wx.EVT_BUTTON, self.OnUpdate)
        self.refresh_view.Bind(wx.EVT_BUTTON, self.OnRefresh)

        self.plugins_menu = wx.Menu()
        show_entry = self.plugins_menu.Append(-1,"Show Clipboard")

        self.menu_item = self.parent.AddToMenuBar("Clipboard Viewer",
                                                      self.plugins_menu)
        self.parent.BindMenubarEvent(show_entry, self.ShowMe)

        self.button_sizer.Add(self.update_clp)
        self.button_sizer.AddSpacer(5)
        self.button_sizer.Add(self.refresh_view)

        self.main_sizer.Add(self.clip_view_descr)
        self.main_sizer.AddSpacer(10)
        self.main_sizer.Add(self.clip_view, 1, wx.EXPAND)
        self.main_sizer.Add(self.button_sizer)

        self.main_panel.SetSizerAndFit(self.main_sizer)

        self.Bind(wx.EVT_CLOSE, self.HideMe)
        self.Hide()

    def ReadClipboard(self):
        #opening the clipboard
        if not wx.TheClipboard.IsOpened():
            wx.TheClipboard.Open()

        #reading the clipboard
        txt = wx.TextDataObject()
        success = wx.TheClipboard.GetData(txt)
        #loading the text to the clip_view
        if success:
            self.clip_view.SetValue( txt.GetText() )

    def OnRefresh(self, event):
        self.ReadClipboard()

    def OnUpdate(self, event):
        #creating the data object
        data = wx.TextDataObject()
        #settinc the data object value
        data.SetText(self.clip_view.GetValue())
        
        #writing the data object to clipboard
        if not wx.TheClipboard.IsOpened():        
            wx.TheClipboard.Open()
        wx.TheClipboard.SetData(data)
        wx.TheClipboard.Close()

    def HideMe(self, event):
        self.Hide()

    def ShowMe(self, event):
        self.ReadClipboard()
        self.Show()
