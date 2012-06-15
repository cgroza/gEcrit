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



import wx, os
import yapsy.IPlugin
from data.plugins.categories import Passive

class Notes(wx.Panel, Passive,yapsy.IPlugin.IPlugin):
    def __init__(self):
        self.name = "Notes"

    def Init(self, parent):
        self.parent = parent
        self.save_point = parent.HOMEDIR + "/.gEcrit/Notes.plugin.conf"

        wx.Panel.__init__(self, self.parent.GetBottomPanel())
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.txt_input = wx.TextCtrl(self, -1, style = wx.TE_MULTILINE |
                                                   wx.TE_PROCESS_ENTER)
        self.txt_input.Bind(wx.EVT_TEXT_ENTER, self.Save)
        self.ReadTxtFile()

        self.sizer.Add(self.txt_input, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()

        self.parent.AddToBottomPanel(self, "Notes")

    def ReadTxtFile(self):
        if not os.path.exists(self.save_point):
            source = open(self.save_point, "w")
            source.write("")
            source.close()
            return
        self.txt_input.LoadFile(self.save_point)

    def Save(self, event):
        self.txt_input.SaveFile(self.save_point)
        event.Skip()

    def Stop(self):
        self.txt_input.SaveFile(self.save_point)
        self.parent.DeleteBottomPage(self.name)
