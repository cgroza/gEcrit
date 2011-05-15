#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import os
from SyntaxHighlight import *


class ConfigNanny:
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
        self.DefaultConfigDict = {
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
            "BashShell": False,
            "PythonShell": False,
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

        self.ReadConfig()

    def GetOption(self, option):
        """
        GetOption

        Return the status of the requested option from the
        configuration dictionary.
        If something goes wrong, returns from default.
        """
        try:
            return (self.ConfigDict)[option]
        except:

            return (self.DefaultConfigDict)[option]

    def ChangeOption(self, option, val, IdRange=0):
        """
        ChangeOption

        Modifies the status of the requested option  to the provided
        value.

        Updates the configuration dictionary and writes it to file.
        """
        TempConfigDict = self.ConfigDict

        (self.DefaultConfigDict)[option]
        TempConfigDict[option] = val

        NewConfig = open(self.HOMEDIR + "/.gEcrit/gEcrit.conf", "w")
        NewConfig.write(str(TempConfigDict))
        NewConfig.close()
        if option in ["PythonShell","BashShell"]:
            self.UpdateShells(option)

        if option in self.update_funct:
            self.update_funct[option](val,IdRange)

        self.ReadConfig()

    def ReadConfig(self):
        """
        ReadConfig

        Reads the configuration file and generates a configuration
        dictionary.

        If something goes wrong, returns from default.
        """
        try:
            ConfigFile = open(self.HOMEDIR + "/.gEcrit/gEcrit.conf", "r")
            self.ConfigDict = eval(ConfigFile.read())
            return self.ConfigDict
        except:
            if not os.path.exists(self.HOMEDIR + "/.gEcrit/gEcrit.conf"):
                if not os.path.exists(self.HOMEDIR + "/.gEcrit"):
                    os.mkdir(self.HOMEDIR + "/.gEcrit/")
            self.ConfigDict = self.DefaultConfigDict
            ConfigFile = open(self.HOMEDIR + "/.gEcrit/gEcrit.conf", "w")
            ConfigFile.write(str(self.DefaultConfigDict))
            ConfigFile.close()
            return self.ConfigDict


    def UpdateIndentSize(self, val, IdRange):
        for id in IdRange:
            item = wx.FindWindowById(id)
            item.SetIndent(val)

    def UpdateIndentationGuides(self, val, IdRange):
        for id in IdRange:
            item = wx.FindWindowById(id)
            item.SetIndentationGuides(val)

    def UpdateBackSpaceUnindent(self, val, IdRange):
        for id in IdRange:
            item = wx.FindWindowById(id)
            item.SetBackSpaceUnIndents(val)

    def UpdateWhitespace(self, val, IdRange):
        for id in IdRange:
            item = wx.FindWindowById(id)
            item.SetViewWhiteSpace(val)

    def UpdateUseTabs(self, val, IdRange):
        for id in IdRange:
            item = wx.FindWindowById(id)
            item.SetUseTabs(val)

    def UpdateCarretWidth(self, val, IdRange):
        for id in IdRange:
            item = wx.FindWindowById(id)
            item.SetCaretWidth(val)


    def UpdateLineNumbers(self, val, IdRange):

        for id in IdRange:
            item = wx.FindWindowById(id)
            if val == True:

                item.SetMarginWidth(1, 45)
            else:
                item.SetMarginWidth(1, 1)

    def UpdateFoldMarks(self, val, IdRange):
        for id in IdRange:
            item = wx.FindWindowById(id)
            if val == True:
                item.SetMarginType(2, wx.stc.STC_MARGIN_SYMBOL)
                item.SetMarginMask(2, wx.stc.STC_MASK_FOLDERS)
                item.SetMarginSensitive(2, True)
                item.SetMarginWidth(2, 12)
            elif val == False:
                item.SetMarginWidth(2, 1)

    def UpdateSyntaxHighlight(self, val, IdRange):

        if val == False:
            for id in IdRange:
                item = wx.FindWindowById(id)
                item.StyleClearAll()
        elif val == True:
            for id in IdRange:
                SyntCol.ActivateSyntaxHighLight(id)

    def UpdateStatusBar(self, val=True, IdRange=0):

        item = wx.FindWindowById(999)
        if val == True:
            item.Show(True)
        else:
            item.Hide()

    def UpdateTabWidth(self, val, IdRange):

        for id in IdRange:
            item = wx.FindWindowById(id)
            item.SetTabWidth(val)

    def UpdateEdgeLine(self, val, IdRange):
        if val == False:
            for id in IdRange:
                item = wx.FindWindowById(id)
                item.SetEdgeMode(wx.stc.STC_EDGE_NONE)
        else:
            for id in IdRange:
                item = wx.FindWindowById(id)
                item.SetEdgeMode(wx.stc.STC_EDGE_LINE)

    def UpdateEdgeColumn(self, val, IdRange):
        for id in IdRange:
            item = wx.FindWindowById(id)
            item.SetEdgeColumn(val)


    def UpdateShells(self, feature):
        item = wx.FindWindowById(4002)
        OSShell = wx.FindWindowById(4000)
        PyShell = wx.FindWindowById(4001)
        Nb_Panel = wx.FindWindowById(998)

        if not self.GetOption("PythonShell"):
            try:
                PyShell.OnClose(0)
                item.RemovePage(self.GetTab("Python", item))
            except:
                pass
        if not self.GetOption("BashShell") and feature == \
            "BashShell":

            OSShell.OnClose(0)
            item.RemovePage(self.GetTab("OS Shell", item))

        if self.GetOption("PythonShell") and feature == \
            "PythonShell":
            PyShell.OnRun(0, self.GetOption("PyPath"))
            item.AddPage(PyShell.parent, "Python")
            PyShell.GetParent().Fit()


        if self.GetOption("BashShell") and feature == \
            "BashShell":
            OSShell.OnRun(0, self.GetOption("OSPath"))
            item.AddPage(OSShell.parent, "OS Shell")
            OSShell.GetParent().Fit()

        if item.GetPageCount() == 0:

            item.GetParent().GetParent().Unsplit(item.GetParent())



    def UpdateAutoSaveInterval(self, val, IdRange):
        for id in IdRange:
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

    def ApplyIDEConfig(self, text_id, file_ext):
        """
        ApplyIDEConfig

        Sets the IDE related features at application startup time.
        """
        cur_doc = wx.FindWindowById(text_id)

        SyntCol.ActivateSyntaxHighLight(text_id)

        if self.GetOption("Autoindentation"):
            cur_doc.SetIndent(self.GetOption("IndentSize"))

        cur_doc.SetIndentationGuides(self.GetOption("IndetationGuides"))
        cur_doc.SetBackSpaceUnIndents(self.GetOption("BackSpaceUnindent"))

        cur_doc.SetViewWhiteSpace(self.GetOption("Whitespace"))
        cur_doc.SetUseTabs(self.GetOption("UseTabs"))

        cur_doc.SetCaretWidth(self.GetOption("CarretWidth"))
        cur_doc.SetTabWidth(self.GetOption("IndentSize"))

        cur_doc.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        if self.GetOption("LineNumbers"):
            cur_doc.SetMarginWidth(1, 45)
            cur_doc.SetMarginSensitive(1, True)
        else:
            cur_doc.SetMarginWidth(1, 1)
            cur_doc.SetMarginSensitive(1, False)

        if self.GetOption("FoldMarks"):
            cur_doc.SetMarginType(2, wx.stc.STC_MARGIN_SYMBOL)
            cur_doc.SetMarginMask(2, wx.stc.STC_MASK_FOLDERS)
            cur_doc.SetMarginSensitive(2, True)
            cur_doc.SetMarginWidth(2, 12)


        cur_doc.SetTabWidth(self.GetOption("TabWidth"))
        if self.GetOption("EdgeLine"):
            cur_doc.SetEdgeColumn(self.GetOption("EdgeColumn"))
            cur_doc.SetEdgeMode(wx.stc.STC_EDGE_LINE)
            cur_doc.SetEdgeColour(SyntCol.ReadColorFile("EdgeLine"))


Config = ConfigNanny()
