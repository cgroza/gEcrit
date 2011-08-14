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
import os
import wx.lib.inspection
from Configuration import *
from Logger import *
from SyntaxHighlight import *
from Logger import *
import AutoComplet
from StcMode import *
from StcLangModes import *

class StcTextCtrl(wx.stc.StyledTextCtrl):
    """
    StcTextCtrl

    Provides the editing facilities and function.
    Creates the editor object and its environment.
    Stores its file path.
    """

    lang_modes = [StcPythonMode, StcRubyMode, StcCppMode, StcPerlMode, StcJavaMode]

    __brace_dict={              # for barce completion
        40:")",
        91:"]",
        123:"}",
        39:"'",
        34:'"'
        }

    def __init__(self, parent, id,  file_path="New Document"):
        """
        __init__

        Initializes the StyledTextCtrl object and sets up its
        environment.
        Binds the proper events to their functions and sets up the
        spell checker object.
        """
        wx.stc.StyledTextCtrl.__init__(self, parent, id, pos=(0, 0),
                                       size=(1, 1))

        self.CharCount = 0
        self.__save_path = file_path
        self.parent = parent

        self.__main_window = self.parent.GetParent()
        self._ = self.__main_window._

        self.__file_size = False
        if file_path != "New Document" and file_path != "":
            self.LoadFile(file_path)
            self.__file_size = os.path.getsize(file_path)

        else:
            self.__save_path = ""

        self.__macro_register = [] # stores the macro event sequence

        self.save_record = self.GetText()

        self.__HOMEDIR = os.path.expanduser('~')

        self.nb = wx.FindWindowById(900)

        self.__status_bar = wx.FindWindowById(999)
        self.text_id = id

        self.__autosave_interval = Config.GetOption("Autosave Interval")
        if Config.GetOption("Autosave") == True:
            self.Bind(wx.stc.EVT_STC_CHARADDED, self.Autosave)

        self.__show_check_dlg = True

        self.__check_count = 0
        self.lang_mode = None   # will point to a StcMode object, will be set by UpdateLangMode()

        self.Bind(wx.stc.EVT_STC_CHARADDED, self.OnCompBrace)

        self.Bind(wx.stc.EVT_STC_UPDATEUI, self.UpdateCords)

        self.Bind(wx.stc.EVT_STC_UPDATEUI,  self.OnUpdateUI)
        self.Bind(wx.stc.EVT_STC_MARGINCLICK,
                  self.OnMarginClick)

        self.Bind(wx.EVT_KEY_UP,  self.AutoIndent)
        self.Bind(wx.EVT_KEY_UP, self.OnCheckFile)

        self.Bind(wx.stc.EVT_STC_CHARADDED, lambda event: AutoComplet.AutoComp.OnKeyPressed(event,
                                                                                                 self.text_id))

        self.Bind(wx.stc.EVT_STC_MACRORECORD, self.OnMacroRecord)

        self._DefineMarkers()
        self.UpdateLangMode()   # apply the language mode
        self.ApplyIDEConfig()   # apply the IDE configurations        

    def UpdateLangMode(self):
        ext = self.GetFileExtension()
        self.lang_mode = StcFundamentalMode(self) # default mode, it will be changed if a specialized one exists
        for mode in StcTextCtrl.lang_modes:
            if ext in mode.file_extensions:
                self.lang_mode = mode(self)
                self.SetLexer(mode.lexer)
                break
        if Config.GetOption("SyntaxHighlight"):
            self.ActivateSyntaxHighLight() # Refreshes the control to use the current mode

    def OnReload(self,event):
        """
        OnReload

        Loads the current file from the hard disk once again.
        Checks for it's existence first. If it does not exists,
        prompts the user.
        """
        if self.__save_path:
            if os.path.exists(self.__save_path):
                self.LoadFile(self.__save_path)
                Log.AddLogEntry("Reloaded "+self.__save_path)
            else:
                fl_not_exists = wx.MessageDialog(self,self._("The file ")+self.__save_path+self._(" does\
 not exists. Do you wish to save it?"), self._("Missing File"),style = wx.YES | wx.NO)
                if fl_not_exists.ShowModal() == 5103:
                    self.Save(0)
                del fl_not_exists
        else:
            message = wx.MessageDialog(self, self._("The file seems unsaved, it does not exists\
 on the disk. Do you wish to save it?"), self._("File Not Saved"),
                                       style = wx.YES | wx.NO)
            if message.ShowModal() == 5103:
                self.Save(0)
                del message
        self.event()

    def OnCompBrace(self,event):
        """
        OnCompBrace

        If the feature is enabled, it adds a closing brace
        at the current cursor position.
        """
        key = event.GetKey()
        if key in [40,91,123,39,34]:
            if Config.GetOption("BraceComp"):
                self.AddText(StcTextCtrl.__brace_dict[key])
                self.CharLeft()
        event.Skip()

    def SaveAs(self, event):
        """
        SaveAs

        Ask the user for a path via a file dialog and the uses
        the StyledTextCtrl's function to write the date to file.
        Returns False if the user did not complete the process.
        Checks if there is a lexer for the file type and enables
        it if the option is active.
        Adds a log entry.
        """
        savefileas_dlg = wx.FileDialog(None, style=wx.SAVE)
        if self.__main_window.menubar.last_recent != "":
            savefileas_dlg.SetDirectory(os.path.split(self.__main_window.menubar.last_recent)[0])
        else:
            savefileas_dlg.SetDirectory(self.__HOMEDIR)
        if savefileas_dlg.ShowModal() == wx.ID_OK:
            filename = savefileas_dlg.GetFilename()
            saveas_path = os.path.join(savefileas_dlg.GetDirectory(), filename)

            if Config.GetOption("StripTrails"):
                self.OnRemoveTrails(0)

            self.SaveFile(saveas_path)

            self.save_record = self.GetText()

            self.__save_path = saveas_path
            self.__file_size = os.path.getsize(self.__save_path)
            self.__show_check_dlg = True
            if Config.GetOption("StatusBar"):
                self.__status_bar.SetStatusText(self._("Saved as") + saveas_path)

            self.nb.SetPageText(self.nb.GetSelection(), filename)

            # update the lang mode
            if self.GetFileExtension not in self.lang_mode.__class__.file_extensions:
                self.UpdateLangMode()
                self.SetStatusFileMode()

            #notify general plugins
            for t in self.__main_window.general_plugins:
                try: #insulate from possible plugin errors
                    self.__main_window.general_plugins[t].NotifyDocumentSaved()
                except: pass

            #update the ctags files with the new content
            AutoComplet.AutoComp.UpdateCTagsFiles(self.__main_window.id_range)

            del savefileas_dlg
            return True
        else:
            del savefileas_dlg
            return False

    def Save(self, event):
        """
        Save

        Checks if the objects file path is valid and saves to it.
        If not, it calls the SaveAs function to.
        Checks if there is a lexer for the file type and enables
        it if the option is active.
        Adds a log entry.
        """
        if self.__save_path == "" or self.__save_path == "New Document":
            self.SaveAs(0)
            return

        try:
            if Config.GetOption("StripTrails"):
                self.OnRemoveTrails(0)

            self.SaveFile(self.__save_path)
            self.__file_size = os.path.getsize(self.__save_path)
            self.__show_check_dlg = True
            if Config.GetOption("StatusBar"):
                self.__status_bar.SetStatusText("Saved")
            
            self.save_record = self.GetText()
            Log.AddLogEntry(self._("Saved file ") + self.__save_path)
            
            #notify text generalt plugins
            for t in self.__main_window.general_plugins:
                try: #insulate from possible plugin errors
                    self.__main_window.general_plugins[t].NotifyDocumentSaved()
                except: pass
            #update the ctags files with the new content
            AutoComplet.AutoComp.UpdateCTagsFiles(self.__main_window.id_range)
        except:
            print "An exception was thrown during save, falling back to default behavior"
            self.SaveAs(0)


    def Autosave(self, event):
        """
        AutoSave

        Count the numbers of characters entered. If they reach a
        value, calls Save.

        Adds a log entry.

        """
        if self.CharCount == self.__autosave_interval:
            self.Save(0)
            Log.AddLogEntry(self._("Autosaved ")+self.__save_path)
            self.CharCount = 0
        else:

            self.CharCount += 1
        event.Skip()

    def OnDedent(self, event):
        """
        OnDedent

        Dedents the selected lines.
        """
        self.BackTab()

    def OnIndent(self, event):
        """
        OnIndent

        Indents the selected lines.
        """
        sel_end = self.LineFromPosition(self.GetSelectionEnd())
        sel_start = self.LineFromPosition(self.GetSelectionStart())

        for line in range(sel_start, sel_end + 1):
            self.SetLineIndentation(line, self.GetLineIndentation(line) +
                                    self.GetIndent())

    def OnZoomIn(self, event):
        """
        OnZoomIn

        Zooms in the editor.
        """
        self.ZoomIn()
        event.Skip()

    def OnZoomOut(self, event):
        """
        OnZoomOut

        Zooms out the editor.
        """
        self.ZoomOut()
        event.Skip()

    def OnResetZoom(self, event):
        """
        OnResetZoom

        Resets the zoom at the normal state.
        """
        self.SetZoom(0)
        event.Skip()

    def OnRedo(self, event):
        """
        OnRedo

        Redos the editor one step.
        """
        if self.CanRedo():
            self.Redo()
        event.Skip()

    def OnUndo(self, event):
        """
        OnUndo

        Undos the editor one step.
        """
        if self.CanUndo():
            self.Undo()
        event.Skip()

    def OnCut(self, event):
        """
        OnCut

        Cuts the selected text and copies it to clipboard.
        """
        self.Cut()
        event.Skip()

    def OnCopy(self, event):
        """
        OnCopy

        Copies the selected text to clipboard.
        """
        self.Copy()
        event.Skip()

    def OnSelectAll(self, event):
        """
        OnSelectAll

        Selects all the text in the editor.
        """
        self.SelectAll()
        event.Skip()

    def OnPaste(self, event):
        """
        OnPaste

        Pastes from clipboard.
        """
        self.Paste()
        event.Skip()

    def OnInsertDate(self, event):
        """
        OnInsertDate

        Find the date and inserts it in the current postion.
        """
        self.AddText(str(time.ctime()))
        event.Skip()

    def OnRemoveTrails(self,event):
        """
        OnRemoveTrails

        Removes the trailing whitespace in the current document.

        """
        c = self.GetCurrentPos()
        line_nr = self.GetLineCount()
        ln = 1
        while ln <= line_nr:
            ln += 1
            length = self.LineLength(ln)
            if " " not in self.GetLine(ln): continue
            st = self.GetLineEndPosition(ln) - length
            end = self.GetLineEndPosition(ln)
            txt = self.GetTextRange(st,end)
            self.SetTargetStart(st)
            self.SetTargetEnd(end)
            self.ReplaceTarget(txt.rstrip(" ").rstrip("\t"))
        self.SetCurrentPos(c)
        self.SetSelection(c,c)  

    def Tabify(self, event):
        st = 0
        tab_size = self.GetTabWidth()
        end = self.GetTextLength()
        temp_doc = self.GetText()
        temp_doc = temp_doc.replace(" "*tab_size,"\t")
        self.SetText(temp_doc)

    def OnStartRecordMacro(self, event):
        self.__status_bar.SetStatusText(self._("Recording macro..."), 0)
        self.__macro_register = [] # delete old macro
        self.StartRecord()
        event.Skip()

    def OnStopRecordMacro(self, event):
        self.__status_bar.SetStatusText(self._("Stopped recording macro..."), 0)
        self.StopRecord()
        event.Skip()


    def OnMacroRecord(self, event):
        "Records keystrokes and events for macro recording."
        this_event = (event.GetMessage(), event.GetWParam(), event.GetLParam())
        self.__macro_register.append(this_event)
        event.Skip()


    def OnMacroPlayback(self, event):
        "Plays the recorded macro."
        for m in self.__macro_register:
            self.SendMsg(m[0], m[1], m[2])
        event.Skip()
    
    def UnTabify(self, event):
        st = 0
        tab_size = self.GetTabWidth()
        end = self.GetTextLength()
        temp_doc = self.GetText()
        temp_doc = temp_doc.replace("\t"," "*tab_size)
        self.SetText(temp_doc)

    def OnComment(self,event):
        """
        OnComment

        """
        self.lang_mode.OnComment(event)

    def OnUnComment(self,event):
        """
        OnUnComment

        """
        self.lang_mode.OnUnComment(event)

    def SetStatusFileMode(self):
        self.__status_bar.SetStatusText(self.lang_mode.__class__.lang_name+" file.",2)


    def UpdateCords(self, event):
        """
        UpdateCords

        Updates the x,y coordinates of the cursor.
        """

        self.__status_bar.SetStatusText(self._("line: ") + str(self.GetCurrentLine()) +
                                        "    col: " + str(self.GetColumn(self.GetCurrentPos())),
                                        1)
        event.Skip()

    def AutoIndent(self, event):
        """
        AutoIndent

        Responsible for the autoindentation feature.

        """
        key = event.GetKeyCode()
        if key == wx.WXK_NUMPAD_ENTER or key == wx.WXK_RETURN:
            if Config.GetOption("Autoindentation"):
                self.lang_mode.AutoIndent(event)
        event.Skip()


    def OnUpdateUI(self ,evt):
        """
        OnUpdateUI

        Responsible for the bad brace check feature.
        """


        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        caretPos = self.GetCurrentPos()

        if caretPos > 0:
            charBefore = self.GetCharAt(caretPos - 1)
            styleBefore = self.GetStyleAt(caretPos - 1)

        if charBefore and chr(charBefore) in "[]{}()" and styleBefore == wx.stc.STC_P_OPERATOR:
            braceAtCaret = caretPos - 1

        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            styleAfter = self.GetStyleAt(caretPos)

            if charAfter and chr(charAfter) in "[]{}()" and styleAfter == wx.stc.STC_P_OPERATOR:
                braceAtCaret = caretPos

        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)

        if braceAtCaret != -1 and braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)

        evt.Skip()


    def OnMarginClick(self, evt):
        """
        OnMarginClick

        Responsible for the interaction of the user with
        code folding.
        """

        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.FoldAll()
            else:
                lineClicked = self.LineFromPosition(evt.GetPosition())

                if self.GetFoldLevel(lineClicked) & wx.stc.STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldExpanded(lineClicked, True)
                        self.Expand(lineClicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldExpanded(lineClicked):
                            self.SetFoldExpanded(lineClicked, False)
                            self.Expand(lineClicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(lineClicked, True)
                            self.Expand(lineClicked, True, True, 100)
                    else:
                        self.ToggleFold(lineClicked)


        elif evt.GetMargin() == 1:
            ln = self.LineFromPosition(evt.GetPosition())
            marker = self.MarkerGet(ln)
            if marker == 0:
                self.MarkerAdd( ln , 3)
            elif marker == 8:
                self.MarkerDelete( ln , 3)

                
        evt.Skip()


    def FoldAll(self):
        """
        FoldAll

        Folds all the code when given the command.

        """

        lineCount = self.GetLineCount()
        expanding = True

        for lineNum in range(lineCount):
            if self.GetFoldLevel(lineNum) & wx.stc.STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldExpanded(lineNum)
                break

        lineNum = 0

        while lineNum < lineCount:
            level = self.GetFoldLevel(lineNum)
            if level & wx.stc.STC_FOLDLEVELHEADERFLAG and level & wx.stc.STC_FOLDLEVELNUMBERMASK == \
                    wx.stc.STC_FOLDLEVELBASE:

                if expanding:
                    self.SetFoldExpanded(lineNum, True)
                    lineNum = self.Expand(lineNum, True)
                    lineNum = lineNum - 1
                else:
                    lastChild = self.GetLastChild(lineNum, -1)
                    self.SetFoldExpanded(lineNum, False)

                    if lastChild > lineNum:
                        self.HideLines(lineNum + 1, lastChild)

            lineNum = lineNum + 1


    def Expand(self, line, doExpand, force=False, visLevels=0, level=-1):
        """
        Expand

        Expands the provided line in argument line.
        """

        lastChild = self.GetLastChild(line, level)
        line = line + 1

        while line <= lastChild:
            if force:
                if visLevels > 0:
                    self.ShowLines(line, line)
                else:
                    self.HideLines(line, line)
            else:
                if doExpand:
                    self.ShowLines(line, line)

            if level == -1:
                level = self.GetFoldLevel(line)

            if level & wx.stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if visLevels > 1:
                        self.SetFoldExpanded(line, True)
                    else:
                        self.SetFoldExpanded(line, False)

                    line = Expand(text_id, line, doExpand, force, visLevels -
                                  1)
                else:

                    if doExpand and self.GetFoldExpanded(line):
                        line = Expand(text_id, line, True, force, visLevels -
                                      1)
                    else:
                        line = Expand(text_id, line, False, force, visLevels -
                                      1)
            else:
                line = line + 1

        return line


    def OnSelectCodeBlock(self,event):
        self.lang_mode.OnSelectCodeBlock(event)

    def OnCheckFile(self,event):
        self.__check_count += 1
        if self.__save_path != "" and self.__show_check_dlg and self.__check_count == 5:
            if not os.path.exists(self.__save_path):
                self.OnReload(0)
            else:
                if os.path.getsize(self.__save_path) != self.__file_size:
                    check_file_ask = wx.MessageDialog(self,self._("The file ")+self.__save_path+self._(" has\
 been modified and the loaded buffer is out of date. Do you wish to reload it?"),self._("File Modified"),style = wx.YES | wx.NO)
                    if self.check_file_ask.ShowModal() == 5103:
                        self.OnReload(0)
                        self.__check_count = 0
                    else:
                        self.__check_count = 0
                        self.__show_check_dlg = False
                    del self.check_file_ask
        event.Skip()

    def _DefineMarkers(self):
        #marker definitions (fold nodes, line numbers...)
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPEN, wx.stc.STC_MARK_BOXMINUS,
                          "white", "#808080")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDER, wx.stc.STC_MARK_BOXPLUS,
                          "white", "#808080")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERSUB, wx.stc.STC_MARK_VLINE,
                          "white", "#808080")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERTAIL, wx.stc.STC_MARK_LCORNER,
                          "white", "#808080")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEREND, wx.stc.STC_MARK_BOXPLUSCONNECTED,
                          "white", "#808080")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.stc.STC_MARK_BOXMINUSCONNECTED,
                          "white", "#808080")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERMIDTAIL, wx.stc.STC_MARK_TCORNER,
                          "white", "#808080")
    	self.MarkerDefine(3, wx.stc.STC_MARK_CIRCLE, "#0000FF", "#FF0000")

        
    def GetEndOfLineCharacter(self):
        emode = self.GetEOLMode()
        if emode == wx.stc.STC_EOL_CR:
            return '\r'
        elif emode == wx.stc.STC_EOL_CRLF:
            return '\r\n'
        return '\n'


    ####################################################################
    #                        PLUGIN INTERFACE                          #
    ####################################################################
    def GetFilePath(self):
        """
        GetFilePath

        Returns the file from which the buffer is loaded.

        """
        return self.__save_path

    def GetFileName(self):
        """
        GetFileName

        Returns the filename of the current buffer.

        """
        return os.path.split(self.__save_path)[-1]

    def GetFileExtension(self):
        """
        GetFileExtension
     
        Returns the file extension of the current buffer.
        """
        return os.path.split(self.__save_path)[-1].split(".")[-1]

    def ApplyIDEConfig(self):
        """
        ApplyIDEConfig

        Configures the StcTextCtrl with the user settings
        """

        
        if Config.GetOption("SyntaxHighlight"):
            self.ActivateSyntaxHighLight()

        if Config.GetOption("Autoindentation"):
            self.SetIndent(Config.GetOption("IndentSize"))

        self.SetIndentationGuides(Config.GetOption("IndetationGuides"))
        self.SetBackSpaceUnIndents(Config.GetOption("BackSpaceUnindent"))

        self.SetViewWhiteSpace(Config.GetOption("Whitespace"))
        self.SetUseTabs(Config.GetOption("UseTabs"))

        self.SetCaretWidth(Config.GetOption("CarretWidth"))
        self.SetTabWidth(Config.GetOption("IndentSize"))

        self.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        if Config.GetOption("LineNumbers"):
            self.SetMarginWidth(1, 45)
            self.SetMarginSensitive(1, True)
        else:
            self.SetMarginWidth(1, 1)
            self.SetMarginSensitive(1, False)

        if Config.GetOption("FoldMarks"):
            self.SetMarginType(2, wx.stc.STC_MARGIN_SYMBOL)
            self.SetMarginMask(2, wx.stc.STC_MASK_FOLDERS)
            self.SetMarginSensitive(2, True)
            self.SetMarginWidth(2, 12)


        self.SetTabWidth(Config.GetOption("TabWidth"))
        if Config.GetOption("EdgeLine"):
            self.SetEdgeColumn(Config.GetOption("EdgeColumn"))
            self.SetEdgeMode(wx.stc.STC_EDGE_LINE)
            self.SetEdgeColour(SyntCol.GetColor("EdgeLine"))

    def ActivateSyntaxHighLight(self):
        """
        ActivateSyntaxHighLight

        Initializes the lexer and sets the color styles.

        """

        keywords = self.lang_mode.__class__.keywords
        self.SetKeyWords(0, (" ").join(keywords))
        self.SetProperty("fold", "1")
        self.StyleSetSpec(wx.stc.STC_P_DEFAULT, "fore:#000000")
        self.StyleSetSpec(wx.stc.STC_P_COMMENTLINE, "fore:" + SyntCol.GetColor("Comments").GetAsString(wx.C2S_HTML_SYNTAX))
        self.StyleSetSpec(wx.stc.STC_P_NUMBER, "fore:" + SyntCol.GetColor("Integers").GetAsString(wx.C2S_HTML_SYNTAX))
        self.StyleSetSpec(wx.stc.STC_P_STRING, "fore:" + SyntCol.GetColor("Strings").GetAsString(wx.C2S_HTML_SYNTAX))
        self.StyleSetSpec(wx.stc.STC_P_CHARACTER, "fore:" + SyntCol.GetColor("Strings").GetAsString(wx.C2S_HTML_SYNTAX))
        self.StyleSetSpec(wx.stc.STC_P_WORD, "fore:" + SyntCol.GetColor("Keywords").GetAsString(wx.C2S_HTML_SYNTAX))
        self.StyleSetSpec(wx.stc.STC_P_TRIPLE, "fore:" + SyntCol.GetColor("TripleQuotes").GetAsString(wx.C2S_HTML_SYNTAX))
        self.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, "fore:" + SyntCol.GetColor("TripleQuotes").GetAsString(wx.C2S_HTML_SYNTAX))
        self.StyleSetSpec(wx.stc.STC_P_CLASSNAME, "fore:" + SyntCol.GetColor("MethodNames").GetAsString(wx.C2S_HTML_SYNTAX) +
                             ",bold,underline")
        self.StyleSetSpec(wx.stc.STC_P_DEFNAME, "fore:" + SyntCol.GetColor("MethodNames").GetAsString(wx.C2S_HTML_SYNTAX) +
                             ",bold,underline")
        self.StyleSetSpec(wx.stc.STC_P_OPERATOR, "fore:" + SyntCol.GetColor("Operators").GetAsString(wx.C2S_HTML_SYNTAX))
        self.StyleSetSpec(wx.stc.STC_P_IDENTIFIER, "fore:" + SyntCol.GetColor("Identifiers").GetAsString(wx.C2S_HTML_SYNTAX))
        self.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK, "fore:" + SyntCol.GetColor("Comments").GetAsString(wx.C2S_HTML_SYNTAX))
        self.StyleSetSpec(wx.stc.STC_P_STRINGEOL,
                             "fore:#000000,face:%s,back:" + SyntCol.GetColor("BadEOL").GetAsString(wx.C2S_HTML_SYNTAX) +
                             "eol")
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT, "back:" + SyntCol.GetColor("Brackets").GetAsString(wx.C2S_HTML_SYNTAX))
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD,
                             "fore:#000000,back:#FF0000,bold")
        self.SetCaretForeground("BLUE")
        self.SetEdgeColour(SyntCol.GetColor("EdgeLine"))


