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

#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx, os
import yapsy.IPlugin
from data.plugins.categories import General


class StampIt(wx.Frame, yapsy.IPlugin.IPlugin, General):

    """
    DefaultColderFr

    Creates a window and all the control necessary to
    change the contents of the text added upon a new tab.

    """

    def __init__(self):
        self.name = "StampIt"


    def Init(self, parent):
        """
        __init__


        Creates the frame and all the controls. Binds their events to
        the neccesary functions.
        """
        self.parent = parent

        self.__text_file = self.parent.HOMEDIR + "/.gEcrit/StampIt.txt"
        wx.Frame.__init__(self, self.parent, -1, 'StampIt', size=(500, 410))

        panel = wx.Panel(self)

        descr = wx.StaticText(panel, -1,
                              'The folowing text will be added automatically when creating a new tab:'
                              , pos=(10, 10), size=(-1, -1))

        self.text_ctrl = wx.TextCtrl(
            panel,
            -1,
            '',
            size=(300, 350),
            pos=(10, 300),
            style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER 
            )

        save_btn = wx.Button(panel, -1, 'Save', size=(-1, -1),
                             pos=(600, 460))
        close_btn = wx.Button(panel, -1, 'Close', size=(-1, -1),
                              pos=(600, 460))

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(save_btn, 0, wx.EXPAND)
        btn_sizer.Add(close_btn, 0, wx.EXPAND)

        self.Bind(wx.EVT_CLOSE, self.HideMe)
        close_btn.Bind(wx.EVT_BUTTON, self.HideMe)
        save_btn.Bind(wx.EVT_BUTTON, self.Save)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(descr, 0, wx.EXPAND)
        main_sizer.AddSpacer(10)
        main_sizer.Add(self.text_ctrl, 0, wx.EXPAND)
        main_sizer.Add(btn_sizer, 0, wx.EXPAND)
        panel.SetSizer(main_sizer)
        panel.Fit()

        self.plugins_menu = wx.Menu()
        show_entry = self.plugins_menu.Append(-1,"Edit Stamp Text")

        self.menu_item = self.parent.AddToMenuBar("StampIt",
                                                      self.plugins_menu)
        self.parent.BindMenubarEvent(show_entry, self.ShowMe)

        self.ReadTextFile()
        self.Bind(wx.EVT_CLOSE, self.HideMe)
        self.Centre()
        self.Hide()

    def Save(self, event):
        """
        OnSave

        Saves the contents of the TextCtrl to the text file.
        """
        self.text_ctrl.SaveFile(self.__text_file)
        event.Skip()


    def ReadTextFile(self):
        """
        ReadTextFile

        Reads the plugin's text file and sets the text to the wx.TextCtrl.
        """
        if not os.path.exists(self.__text_file):
            source = open(self.__text_file, "w")
            source.write("")
            source.close()
            return
        self.text_ctrl.LoadFile(self.__text_file)

    def NotifyNewTabOpened(self):
        doc = self.parent.GetCurrentDocument()
        doc.AddText(self.text_ctrl.GetValue())


    def ShowMe(self, event):
        """
        ShowMe

        Makes window visible.
        """

        self.Show()

    def HideMe(self, event):
        """
        Hides the window.
        """

        self.Hide()



