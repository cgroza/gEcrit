import wx
from data.plugins.categories import General
import yapsy.IPlugin

class TreeFileBrowser(wx.GenericDirCtrl):
    def __init__(self, parent):
        self.parent = parent
        wx.GenericDirCtrl.__init__(self, self.parent, -1,
                filter ="""Python files (.py)|*.py|
PythonW files (.pyw)|*.pyw|
Ruby files (.rb) |*.rb|
Text files (.txt) |*.txt|
All files (*.*)|*.*
""", style =wx.DIRCTRL_SHOW_FILTERS)



    def OnItemActivated(self, event):
        file_path = self.GetFilePath()
        if file_path != "":
            self.parent.parent.OpenFile(file_path)
        event.Skip()

class TreeFilePanel(wx.Panel, General, yapsy.IPlugin.IPlugin):
    def __init__(self):
        self.name = "Tree File Browser"

    def Init(self, parent):
        self.parent = parent
        wx.Panel.__init__(self, self.parent.GetSidePanel())
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.file_browser = TreeFileBrowser(self)
        self.file_browser.Bind(wx.EVT_TREE_ITEM_ACTIVATED,
                                      self.file_browser.OnItemActivated)

        self.main_sizer.Add(self.file_browser, 1, wx.EXPAND)

        self.SetSizer(self.main_sizer)
        self.Fit()
        self.Layout()
        self.parent.AddToSidePanel(self,"File Browser")

    def NotifyTabChanged(self):
        self.file_browser.ExpandPath(self.parent.GetCurrentDocument().GetFilePath())

    def Stop(self):
        self.parent.DeleteSidePage("File Browser")
