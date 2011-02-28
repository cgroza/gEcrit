
#   Distributed under the terms of the GPL (GNU Public License)
#
#   gEcrit is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


#configClass.py


import wx, os
from TinyFeatures import *
from SyntaxHighlight import *


class ConfigNanny:
    def __init__(self):
        self.DefaultConfigDict = {"Autosave" : False, "Autosave Interval": 200, "StatusBar": True\
        ,"ActLog":True, "LineNumbers": False, "Font":"Arial","FontSize":"12","SyntaxHighlight":True,\
        "IndentSize":4,"Whitespace":False,"IndetationGuides":False, "Autoindentation":True,\
        "BackSpaceUnindent":False, "UseTabs":False, "CarretWidth": 7,"FoldMarks":False,"SourceBrowser":False\
        , "TabWidth":8, "EdgeLine":False, "EdgeColumn":80,"BashShell":False,"PythonShell":False\
        ,"OSPath":"/bin/bash","PyPath":"/usr/bin/python","SpellCheck":False,"SpellSuggestions":False\
        ,"FileTree":False}
        self.HOMEDIR= os.path.expanduser('~')

        self.ReadConfig()


    def GetOption(self,option):
        try:
            return self.ConfigDict[option]

        except:
            return self.DefaultConfigDict[option]


    def ChangeOption(self,option, val,IdRange):
            TempConfigDict = self.ConfigDict
        #~ try:
            self.DefaultConfigDict[option]
            TempConfigDict[option] = val

            NewConfig = open(self.HOMEDIR+"/.gEcrit.conf","w")
            NewConfig.write(str(TempConfigDict))
            NewConfig.close()
            self.ToggleFeature(0,option, val,IdRange)
            self.ReadConfig()
        #~ except:
            #~ ConfigDict = self.DefaultConfigDict
            #~ ConfigFile = open(self.HOMEDIR+"/.gEcrit.conf","w")
            #~ ConfigFile.write(str(self.DefaultConfigDict))
            #~ ConfigFile.close()
            #~ self.ReadConfig()


    def ReadConfig(self):
        try:
            ConfigFile = open(self.HOMEDIR+"/.gEcrit.conf","r")
            self.ConfigDict = eval(ConfigFile.read())
            return self.ConfigDict

        except:
            self.ConfigDict = self.DefaultConfigDict
            ConfigFile = open(self.HOMEDIR+"/.gEcrit.conf","w")
            ConfigFile.write(str(self.DefaultConfigDict))
            ConfigFile.close()
            return  self.ConfigDict


    def ToggleFeature(self,event,feature, val, IdRange):
        if feature == "IndentSize":
            for id in IdRange:
                item =wx.FindWindowById(id)
                item.SetIndent(val)
        elif feature == "IndetationGuides":
            for id in IdRange:
                item =wx.FindWindowById(id)
                item.SetIndentationGuides(val)

        elif feature == "BackSpaceUnindent":
            for id in IdRange:
                item = wx.FindWindowById(id)
                item.SetBackSpaceUnIndents(val)

        elif feature == "Whitespace":
            for id in IdRange:
                item = wx.FindWindowById(id)
                item.SetViewWhiteSpace(val)

        elif feature == "UseTabs":
            for id in IdRange:
                item = wx.FindWindowById(id)
                item.SetUseTabs(val)

        elif feature == "CarretWidth":
            for id in IdRange:
                item=wx.FindWindowById(id)
                item.SetCaretWidth(val)

        elif feature == "IndentSize":
            for id in IdRange:
                item=wx.FindWindowById(id)
                item.SetTabWidth(val)

        elif feature == "LineNumbers":
            for id in IdRange:
                item = wx.FindWindowById(id)
                if val == True:
            #        item.SetMarginType(0,wx.stc.STC_MARGIN_NUMBER)
                    item.SetMarginWidth(1,45)
                else:
                    item.SetMarginWidth(1,1)

        elif feature == "FoldMarks":
            for id in IdRange:
                item = wx.FindWindowById(id)
                if val == True:
                    item.SetMarginType(2, wx.stc.STC_MARGIN_SYMBOL)
                    item.SetMarginMask(2, wx.stc.STC_MASK_FOLDERS)
                    item.SetMarginSensitive(2, True)
                    item.SetMarginWidth(2, 12)
                elif val == False:
                    item.SetMarginWidth(2,1)

        elif feature == "SyntaxHighlight":
            if val == False:
                for id in IdRange:
                    item = wx.FindWindowById(id)
                    item.StyleClearAll()
            elif val == True:
                for id in IdRange:
                    SyntCol.ActivateSyntaxHighLight(id)

        elif feature == "StatusBar":
            item = wx.FindWindowById(999)
            if val == True:
                item.Show(True)
            else:
                item.Hide()

        elif feature == "TabWidth":
            for id in IdRange:
                item = wx.FindWindowById(id)
                item.SetTabWidth(val)

        elif feature == "EdgeLine":
            if val == False:
                for id in IdRange:
                    item = wx.FindWindowById(id)
                    item.SetEdgeMode(wx.stc.STC_EDGE_NONE)
            else:
                for id in IdRange:
                    item = wx.FindWindowById(id)
                    item.SetEdgeMode(wx.stc.STC_EDGE_LINE)

        elif feature == "EdgeColumn":
            for id in IdRange:
                item = wx.FindWindowById(id)
                item.SetEdgeColumn(val)


        elif feature == "SourceBrowser":
            counter=0
            if val == True:
                for id in IdRange:
                    item = wx.FindWindowById(2000+id)
                    nb = wx.FindWindowById(4003+id)
                    if self.GetOption("SourceBrowser") and not self.GetOption("FileTree"):
                        item.parent.GetParent().GetParent().GetParent().SplitVertically(item.GetParent().GetParent().GetParent(), wx.FindWindowById(1001+id))
                    nb.AddPage(item.GetParent(),"Source Browser")
                    counter +=1

            else:
                for id in IdRange:
                    item = wx.FindWindowById(2000+id)
                    nb = wx.FindWindowById(4003+id)
                    if not self.GetOption("SourceBrowser") and not self.GetOption("FileTree"):
                        item.parent.GetParent().GetParent().GetParent().Unsplit(item.GetParent().GetParent().GetParent())
                    nb.RemovePage(self.GetTab("Source Browser",nb))
                    counter +=1


        elif feature == "FileTree":
            counter=0
            if val == True:
                for id in IdRange:
                    item = wx.FindWindowById(5000+id)
                    nb = wx.FindWindowById(4003+id)
                    if self.GetOption("FileTree") and not self.GetOption("SourceBrowser"):
                        item.parent.GetParent().GetParent().GetParent().SplitVertically(item.GetParent().GetParent().GetParent(), wx.FindWindowById(1001+id))
                    nb.AddPage(item.GetParent(),"File Browser")
                    counter +=1

            else:
                for id in IdRange:
                    item = wx.FindWindowById(5000+id)
                    nb = wx.FindWindowById(4003+id)
                    if not self.GetOption("FileTree") and not self.GetOption("SourceBrowser"):
                        item.parent.GetParent().GetParent().GetParent().Unsplit(item.GetParent().GetParent().GetParent())
                    nb.RemovePage(self.GetTab("File Browser",nb))
                    counter +=1


        elif feature in ["PythonShell","BashShell"]:
            item = wx.FindWindowById(4002)
            OSShell = wx.FindWindowById(4000)
            PyShell = wx.FindWindowById(4001)
            Nb_Panel = wx.FindWindowById(998)
            if  not self.GetOption("PythonShell"):
                try:
                    PyShell.OnClose(0)
                    item.RemovePage(self.GetTab("Python",item))
                except:pass
            if not self.GetOption("BashShell") and feature == "BashShell":
 #               try:
                    OSShell.OnClose(0)
                    item.RemovePage(self.GetTab("OS Shell",item))
#                except: pass

            if not self.GetOption("PythonShell") and not self.GetOption("BashShell"):
                #item.Hide()
                item.GetParent().GetParent().Unsplit(item.GetParent())

            else:
                if self.GetOption("PythonShell") and  feature == "PythonShell":
                    PyShell.OnRun(0,self.GetOption("PyPath"))
                    item.AddPage(PyShell.parent, "Python")
                    PyShell.GetParent().Fit()

                if self.GetOption("BashShell") and feature == "BashShell":
                    OSShell.OnRun(0,self.GetOption("OSPath"))
                    item.AddPage(OSShell.parent,"OS Shell")
                    OSShell.GetParent().Fit()

                item.GetParent().GetParent().SplitHorizontally(Nb_Panel,item.GetParent())
                item.GetParent().GetParent().Refresh()

        elif feature == "EdgeLine":
            if val:
                for id in IdRange:
                    wx.FindWindowById(id).SetEdgeMode(wx.stc.STC_EDGE_LINE)
            else:
                for id in IdRange:
                    wx.FindWindowById(id).SetEdgeMode(wx.stc.STC_EDGE_NONE)

    def GetTab(self,tab_name, notebook):
          end = notebook.GetPageCount()
          selectedtabText = ""

          for i in range(end):
            selectedtabText = notebook.GetPageText(i)

            if tab_name == selectedtabText:
                return i;

          return -1;



    def ApplyIDEConfig(self,text_id, file_ext):
        cur_doc = wx.FindWindowById(text_id)

        if self.GetOption("SyntaxHighlight") and file_ext =="py":
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
            cur_doc.SetMarginWidth(1,45)
        else:
            cur_doc.SetMarginWidth(1,1)

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
