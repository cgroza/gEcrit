#  Copyright (C) 2011  Groza Cristian
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
from data.plugins.categories import General
import yapsy.IPlugin

class TreeFileBrowser(wx.GenericDirCtrl):
    def __init__(self, parent):
        file_filter ="Python files (.py)|*.py|PythonW files (.pyw)|*.pyw|Ruby files (.rb) |*.rb|Text files (.txt) |*.txt|All files (*.*)|*.*"
        

        self.parent = parent
        wx.GenericDirCtrl.__init__(self, self.parent, -1, filter =file_filter,
            style =wx.DIRCTRL_SHOW_FILTERS)

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
