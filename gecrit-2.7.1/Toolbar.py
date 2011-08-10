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

import wx, gettext
from Fonts import *




class MainToolbar(wx.ToolBar):
    """
    MainToolbar

    Creates the application toolbar object.

    """
    def __init__(self, parent, id=wx.ID_ANY):

        """
         __init__

         Builds the ToolBar object and adds elemensts to it.
         Takes the icons from the icons/ folder.
        """


        wx.ToolBar.__init__(self, parent, id, style=wx.TB_HORIZONTAL |
                            wx.NO_BORDER)

        #self.presLan_ro = gettext.translation("gEcrit", "./locale")

        self._ = parent._

        #self.presLan_ro.install()


        self.new_tab_img = wx.Image('icons/newtab.bmp', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.open_img = wx.Image('icons/open.bmp', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.save_img = wx.Image('icons/save.bmp', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.saveas_image = wx.Image('icons/saveas.bmp', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        ConfigImage = wx.Image('icons/config.bmp', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.quit_img = wx.Image('icons/quit.bmp', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.print_img = wx.Image("icons/printer.bmp", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.run_img = wx.Image("icons/run.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        self.AddSimpleTool(600, self.new_tab_img, self._('New'),
                                    self._('Open a new tab.'))
        self.AddSimpleTool(601, self.open_img, self._('Open'),
                        self._('Open a new document.'))
        self.AddSimpleTool(602, self.save_img, self._('Save'),
                        self._('Save the current document.'))
        self.AddSimpleTool(603, self.saveas_image, self._('Save As'),
             self._('Save the current document under a differend name.'))
        self.AddSimpleTool(604, ConfigImage, self._('Settings'),
                    self._('Open the configuration window.'))
        self.AddSeparator()
        self.AddSimpleTool(605, self.quit_img, self._('Quit'), self._('Quit gEcrit'))

        self.AddSeparator()
        self.AddSimpleTool(609, self.print_img, self._("Print"),
                         self._("Print the current document."))
        self.AddSimpleTool(610, self.run_img, "Run",
                  self._("Run the current file.(Python only)"))
        self.Realize()
