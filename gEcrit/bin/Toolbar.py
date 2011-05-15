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


        self.NewTabImage = wx.Image('icons/newtab.bmp', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.OpenImage = wx.Image('icons/open.bmp', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.SaveImage = wx.Image('icons/save.bmp', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.SaveAsImage = wx.Image('icons/saveas.bmp', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        ConfigImage = wx.Image('icons/config.bmp', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.QuitImage = wx.Image('icons/quit.bmp', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.PrintImage = wx.Image("icons/printer.bmp", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.RunImage = wx.Image("icons/run.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        self.AddSimpleTool(600, self.NewTabImage, self._('New'),
                                    self._('Open a new tab.'))
        self.AddSimpleTool(601, self.OpenImage, self._('Open'),
                        self._('Open a new document.'))
        self.AddSimpleTool(602, self.SaveImage, self._('Save'),
                        self._('Save the current document.'))
        self.AddSimpleTool(603, self.SaveAsImage, self._('Save As'),
             self._('Save the current document under a differend name.'))
        self.AddSimpleTool(604, ConfigImage, self._('Settings'),
                    self._('Open the configuration window.'))
        self.AddSeparator()
        self.AddSimpleTool(605, self.QuitImage, self._('Quit'), self._('Quit gEcrit'))

        self.AddSeparator()
        self.AddSimpleTool(609, self.PrintImage, self._("Print"),
                         self._("Print the current document."))
        self.AddSimpleTool(610, self.RunImage, "Run",
                  self._("Run the current file.(Python only)"))
        self.Realize()
