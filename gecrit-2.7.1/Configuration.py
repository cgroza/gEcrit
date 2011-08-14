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
import os
from SyntaxHighlight import *


class Configuration:
    """
    ConfigNanny

    Manages the application configuration manipulation.

    """

    def __init__(self):
        """
        __init__

        Creates a default configuration dictionary and reads the
        configuration file.
        """
        self.__default_cfg_dict = {
            "Autosave": False,
            "Autosave Interval": 200,
            "StatusBar": True,
            "ActLog": True,
            "LineNumbers": False,
            "Font": "Arial",
            "FontSize": "12",
            "SyntaxHighlight": True,
            "IndentSize": 4,
            "Whitespace": False,
            "IndetationGuides": False,
            "Autoindentation": True,
            "BackSpaceUnindent": False,
            "UseTabs": False,
            "CarretWidth": 7,
            "FoldMarks": False,
            "TabWidth": 8,
            "EdgeLine": False,
            "EdgeColumn": 80,
            "RecentFiles":[],
            "BraceComp":False,
            "StripTrails":False,
            "Session" : True,
            "ActivePlugins": ["Task Keeper","Class Hierarchy Tree",
                              "HTML Converter", "Python Syntax Doctor",
                              "Pastebin.com Uploader","PyTidy","Notes",
                              "Terminator"]
            }

        self.update_funct = {
            "Autosave Interval":self.UpdateAutoSaveInterval,
            "StatusBar":        self.UpdateStatusBar,
            "LineNumbers":      self.UpdateLineNumbers,
            "SyntaxHighlight":  self.UpdateSyntaxHighlight,
            "IndentSize":       self.UpdateIndentSize,
            "Whitespace":       self.UpdateWhitespace,
            "IndetationGuides": self.UpdateIndentationGuides,
            "BackSpaceUnindent":self.UpdateBackSpaceUnindent,
            "UseTabs":          self.UpdateUseTabs,
            "CarretWidth":      self.UpdateCarretWidth,
            "FoldMarks":        self.UpdateFoldMarks,
            "TabWidth":         self.UpdateTabWidth,
            "EdgeLine":         self.UpdateEdgeLine,
            "EdgeColumn":       self.UpdateEdgeColumn
        }

        self.HOMEDIR = os.path.expanduser('~')
        self.cfg_path = os.path.join(self.HOMEDIR, ".gEcrit","gEcrit.conf")
        self.cfg_dir = os.path.join(self.HOMEDIR, ".gEcrit")
        self.__cfg_dict = {}

        self.ReadConfig()

    def GetOption(self, option):
        """
        GetOption

        Return the status of the requested option from the
        configuration dictionary.
        If something goes wrong, returns from default.
        """
        return (self.__cfg_dict)[option]

    def ChangeOption(self, option, val, id_range=0):
        """
        ChangeOption

        Modifies the status of the requested option  to the provided
        value.

        Updates the configuration dictionary and writes it to file.
        """
        self.__cfg_dict[option] = val

        with open(self.cfg_path, "w") as new_cfg:
            new_cfg.write(str(self.__cfg_dict))


        if option in self.update_funct:
            self.update_funct[option](val,id_range)

    def ReadConfig(self):
        """
        ReadConfig

        Reads the configuration file and generates a configuration
        dictionary.

        If something goes wrong, returns from default.
        """
        try:
            cfg_file = open(self.cfg_path, "r")
            self.__cfg_dict = eval(cfg_file.read())
            return self.__cfg_dict
        except:
            if not os.path.exists(self.cfg_path): # create the config dir if it is inexistent
                if not os.path.exists(self.cfg_dir):
                    os.mkdir(self.cfg_dir)
            self.__cfg_dict = self.__default_cfg_dict
            cfg_file = open(cfg_path, "w") # write default cfg file
            cfg_file.write(str(self.__default_cfg_dict))
            cfg_file.close()
            return self.__cfg_dict


    def UpdateIndentSize(self, val, id_range):
        for id in id_range:
            item = wx.FindWindowById(id)
            item.SetIndent(val)

    def UpdateIndentationGuides(self, val, id_range):
        for id in id_range:
            item = wx.FindWindowById(id)
            item.SetIndentationGuides(val)

    def UpdateBackSpaceUnindent(self, val, id_range):
        for id in id_range:
            item = wx.FindWindowById(id)
            item.SetBackSpaceUnIndents(val)

    def UpdateWhitespace(self, val, id_range):
        for id in id_range:
            item = wx.FindWindowById(id)
            item.SetViewWhiteSpace(val)

    def UpdateUseTabs(self, val, id_range):
        for id in id_range:
            item = wx.FindWindowById(id)
            item.SetUseTabs(val)

    def UpdateCarretWidth(self, val, id_range):
        for id in id_range:
            item = wx.FindWindowById(id)
            item.SetCaretWidth(val)


    def UpdateLineNumbers(self, val, id_range):

        for id in id_range:
            item = wx.FindWindowById(id)
            if val == True:

                item.SetMarginWidth(1, 45)
            else:
                item.SetMarginWidth(1, 1)

    def UpdateFoldMarks(self, val, id_range):
        for id in id_range:
            item = wx.FindWindowById(id)
            if val == True:
                item.SetMarginType(2, wx.stc.STC_MARGIN_SYMBOL)
                item.SetMarginMask(2, wx.stc.STC_MASK_FOLDERS)
                item.SetMarginSensitive(2, True)
                item.SetMarginWidth(2, 12)
            elif val == False:
                item.SetMarginWidth(2, 1)

    def UpdateSyntaxHighlight(self, val, id_range):

        if val == False:
            for id in id_range:
                item = wx.FindWindowById(id)
                item.StyleClearAll()
        elif val == True:
            for id in id_range:
                item = wx.FindWindowById(id)
                item.ActivateSyntaxHighLight()

    def UpdateStatusBar(self, val=True, id_range=0):

        item = wx.FindWindowById(999)
        if val == True:
            item.Show(True)
        else:
            item.Hide()

    def UpdateTabWidth(self, val, id_range):

        for id in id_range:
            item = wx.FindWindowById(id)
            item.SetTabWidth(val)

    def UpdateEdgeLine(self, val, id_range):
        if val == False:
            for id in id_range:
                item = wx.FindWindowById(id)
                item.SetEdgeMode(wx.stc.STC_EDGE_NONE)
        else:
            for id in id_range:
                item = wx.FindWindowById(id)
                item.SetEdgeMode(wx.stc.STC_EDGE_LINE)

    def UpdateEdgeColumn(self, val, id_range):
        for id in id_range:
            item = wx.FindWindowById(id)
            item.SetEdgeColumn(val)

    def UpdateAutoSaveInterval(self, val, id_range):
        for id in id_range:
            item = wx.FindWindowById(id)
            item.autosave_interval = val

    def GetTab(self, tab_name, notebook):
        """
        GetTab

        Retrieves a AUI NOTEBOOK tab index from a given name.
        """
        end = notebook.GetPageCount()
        selectedtabText = ""

        for i in range(end):
            selectedtabText = notebook.GetPageText(i)

            if tab_name == selectedtabText:
                return i
                None

        return -1
        None


Config = Configuration()
