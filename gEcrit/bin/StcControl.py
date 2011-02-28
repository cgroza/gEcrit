
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

#StcControl.py

import wx,os,time
import wx.lib.inspection
from configClass import *
from logClass import *
try:
    import enchant
    from SpellChecker import *
    NO_SPELL_CHECK = False
except: print "module enhant not found."; NO_SPELL_CHECK = True
class StcTextCtrl(wx.stc.StyledTextCtrl):
    
    def __init__(self,parent,id,src_br,file_path="New Document"):
        wx.stc.StyledTextCtrl.__init__(self, parent, id, pos = (0,0), size=(1,1))
        self.CharCount  = 0
        self.SaveTarget = file_path

        if file_path != "New Document" and file_path != "":
            self.LoadFile(file_path) 

        else: self.SaveTarget = ""

        self.SaveRecord = self.GetText()

        self.HOMEDIR =  os.path.expanduser('~')

        self.nb = wx.FindWindowById(900)

        self.StatusBar = wx.FindWindowById(999)
        self.InitSrcBr = src_br
        self.text_id = id
        if not NO_SPELL_CHECK:
            self.Bind(wx.stc.EVT_STC_CHARADDED, self.OnSpellCheck)
            self.Bind(wx.EVT_KEY_DOWN,self.OnCheckSpace)

        self.last_word = ""
        self.spell_error = False


        if Config.GetOption("Autosave") == True:
            self.Bind(wx.stc.EVT_STC_CHARADDED, lambda event : self.Autosave(event,Config.GetOption("Autosave Interval")))


    def SaveAs(self,event):
        SaveFileAs = wx.FileDialog(None, style = wx.SAVE)
        SaveFileAs.SetDirectory(self.HOMEDIR)
        if SaveFileAs.ShowModal() == wx.ID_OK:
            SaveAsFileName = SaveFileAs.GetFilename()
            SaveAsPath = SaveFileAs.GetDirectory()+"/"+ SaveAsFileName

            self.SaveFile(SaveAsPath) 

            SaveContent = self.GetText()

            self.SaveTarget = SaveAsPath

            if Config.GetOption("StatusBar"):
                self.StatusBar.SetStatusText("Saved as"+ SaveAsPath)

            self.nb.SetPageText(self.nb.GetSelection(), SaveAsFileName)
            self.InitSrcBr.RefreshTree(self.text_id, SaveAsPath)

            self.SaveRecord = SaveContent
            SaveFileAs.Destroy()
            return True
        else:
            SaveFileAs.Destroy()
            return False



    def Save(self,event):
        if self.SaveTarget == "" or self.SaveTarget == "New Document" :
            self.SaveAs(0)
            return

        try:
            

            self.SaveFile(self.SaveTarget) 

            if Config.GetOption("StatusBar"):
                self.StatusBar.SetStatusText("Saved")

            SaveContent = self.GetText()
            Log.AddLogEntry(time.ctime() + ": Saved file "+self.SaveTarget)
            self.InitSrcBr.RefreshTree(self.text_id, self.SaveTarget)
            self.SaveRecord = SaveContent
        except:
            self.SaveAs(0)


    def OnSpellCheck(self,event):
        if Config.GetOption("SpellCheck"):
            st = self.WordStartPosition(self.GetCurrentPos(),False)
            end = self.WordEndPosition(self.GetCurrentPos(),False)
            word = self.GetTextRange(st,end)
            self.last_word = word
            spelled_ok = WordSpeller.CheckWord(word)

            if not spelled_ok:
                self.StartStyling(st,wx.stc.STC_INDIC2_MASK)
                self.SetStyling(end-st,wx.stc.STC_INDIC2_MASK)
                self.spell_error = True
            else:
                self.StartStyling(st, wx.stc.STC_INDIC2_MASK)
                self.SetStyling(end-st, 0)
                self.spell_error = False

            return end

    def OnCheckSpace(self,event):
        key = event.GetKeyCode()
        if key == 32:
            if self.spell_error:
                if Config.GetOption("SpellSuggestions"):
                    self.CallTipShow(self.GetCurrentPos(),"\n".join(WordSpeller.GetSuggestion\
                    (self.last_word)))
        event.Skip()


    def Autosave(self,event,interval):
        if self.CharCount == interval:
            self.Save(0)
            self.CharCount = 0

        else:
            self.CharCount += 1
        event.Skip()


    def OnDedent(self,event):
        self.BackTab()

    def OnIndent(self,event):
        sel_end =  self.LineFromPosition(self.GetSelectionEnd())
        sel_start =  self.LineFromPosition(self.GetSelectionStart())

        for line in xrange(sel_start,sel_end+1):
            self.SetLineIndentation(line ,self.GetLineIndentation(line) + self.GetIndent())



    def OnZoomIn(self,event):
        self.ZoomIn()
        event.Skip()

    def OnZoomOut(self,event):
        self.ZoomOut()
        event.Skip()

    def OnResetZoom(self, event):
        self.SetZoom(0)
        event.Skip()

    def OnRedo(self,event):
        if self.CanRedo(): self.Redo()
        event.Skip()


    def OnUndo(self,event):
        if self.CanUndo(): self.Undo()
        event.Skip()


    def OnCut(self,event):
        self.Cut()
        event.Skip()

    
    def OnCopy(self,event):
        self.Copy()
        event.Skip()


    def OnSelectAll(self,event):
        self.SelectAll()
        event.Skip()


    def OnPaste(self,event):
        self.Paste()
        event.Skip()


    def OnInsertDate(self,event):
        self.AddText(str(time.ctime()))
        event.Skip()
