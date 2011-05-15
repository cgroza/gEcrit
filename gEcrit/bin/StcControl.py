#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx, gettext
import os
import wx.lib.inspection
from configClass import *
from logClass import *
from SyntaxHighlight import *
from logClass import *
import AutoCompletition

class StcTextCtrl(wx.stc.StyledTextCtrl):
    """
    StcTextCtrl

    Provides the editing facilities and function.
    Creates the editor object and its environment.
    Stores its file path.
    """
    file_exts = {
                "py"   : ".py Python",
                "pyw"  : ".pyw Python",
                "cpp"  : ".cpp C++",
                "h"    : ".h C/C++",
                "txt"  : ".txt Text",
                "sh"   : ".sh Bash",
                "bat"  : ".bat Batch",
                "conf" : ".conf Config",
                "php"  : ".php PHP",
                "html" : ".html HTML",
                "xhtml": ".xhtml XHTML",
                "tcl"  : ".tcl Tcl",
                "pl"   : ".pl Perl",
                "c"    : ".c C",
                "rb"   : ".rb Ruby",
                "js"   : ".js Javascript",
                "java" : ".java Java",
                "lua"  : ".lua LUA",
                "pm"   : ".pm Perl Module",
                "vbs"  : ".vbs Visual Basic",
                "asm"  : ".asm Assembly"
                }

    lexers = {
              "py": wx.stc.STC_LEX_PYTHON,
              "pyw": wx.stc.STC_LEX_PYTHON,
              "rb": wx.stc.STC_LEX_RUBY,
              "cpp" : wx.stc.STC_LEX_CPP,
              "c" : wx.stc.STC_LEX_CPP,
              "java": wx.stc.STC_LEX_CPP
    }

    brace_dict={
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
        self.SaveTarget = file_path
        self.parent = parent

        self.main_window = self.parent.GetParent()
        self._ = self.main_window._

        self.file_size = False
        if file_path != "New Document" and file_path != "":
            self.LoadFile(file_path)
            self.file_size = os.path.getsize(file_path)

        else:
            self.SaveTarget = ""

        self.SaveRecord = self.GetText()

        self.HOMEDIR = os.path.expanduser('~')

        self.nb = wx.FindWindowById(900)

        self.StatusBar = wx.FindWindowById(999)
        self.text_id = id

        self.autosave_interval = Config.GetOption("Autosave Interval")
        if Config.GetOption("Autosave") == True:
            self.Bind(wx.stc.EVT_STC_CHARADDED, self.Autosave)


        self.show_check_dlg = True

        self.check_count = 0

        self.Bind(wx.stc.EVT_STC_CHARADDED, self.OnCompBrace)
        try:
            self.ext = StcTextCtrl.file_exts[self.SaveTarget.split(".")[-1].lower()]
            self.SetStatusFileExt()
        except:
            self.ext = self._("Unknown format ") + self.SaveTarget.split(".")[-1].lower()
            self.SetStatusFileExt()

        self.Bind(wx.stc.EVT_STC_UPDATEUI, self.UpdateCords)

        self.Bind(wx.stc.EVT_STC_UPDATEUI,  self.OnUpdateUI)
        self.Bind(wx.stc.EVT_STC_MARGINCLICK,
                     self.OnMarginClick)

        self.Bind(wx.EVT_KEY_UP,  self.AutoIndent)
        self.Bind(wx.EVT_KEY_UP, self.OnCheckFile)

        self.Bind(wx.stc.EVT_STC_CHARADDED, lambda event: AutoCompletition.AutoComp.OnKeyPressed(event,
                     self.text_id))


        #marker definitions (fold nodes, line numbers...
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

        ext = self.GetFileExtension()
        if ext in StcTextCtrl.lexers:
            self.SetLexer(StcTextCtrl.lexers[ext])
        elif ext != "txt":
                self.SetLexer(StcTextCtrl.lexers["cpp"])



    def OnReload(self,event):
        """
        OnReload

        Loads the current file from the hard disk once again.
        Checks for its existence first. If it does not exists,
        prompts the user.
        """
        if self.SaveTarget != "":
            if os.path.exists(self.SaveTarget):
                self.LoadFile(self.SaveTarget)
                Log.AddLogEntry("Reloaded "+self.SaveTarget)

            else:
                fl_not_exists = wx.MessageDialog(self,self._("The file ")+self.SaveTarget+self._(" does\
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
                self.AddText(StcTextCtrl.brace_dict[key])
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
        SaveFileAs = wx.FileDialog(None, style=wx.SAVE)
        if self.main_window.menubar.last_recent != "":
            SaveFileAs.SetDirectory(os.path.split(self.main_window.menubar.last_recent)[0])
        else:
            SaveFileAs.SetDirectory(self.HOMEDIR)
        if SaveFileAs.ShowModal() == wx.ID_OK:
            SaveAsFileName = SaveFileAs.GetFilename()
            SaveAsPath = SaveFileAs.GetDirectory() + "/" + \
                SaveAsFileName

            if Config.GetOption("StripTrails"):
                self.OnRemoveTrails(0)

            self.SaveFile(SaveAsPath)

            SaveContent = self.GetText()

            self.SaveTarget = SaveAsPath
            self.file_size = os.path.getsize(self.SaveTarget)
            self.show_check_dlg = True
            if Config.GetOption("StatusBar"):
                self.StatusBar.SetStatusText(self._("Saved as") + SaveAsPath)

            self.nb.SetPageText(self.nb.GetSelection(), SaveAsFileName)


            self.SaveRecord = SaveContent

            if self.GetFileExtension() in StcTextCtrl.lexers:
                self.SetLexer(StcTextCtrl.lexers[self.GetFileExtension()])
                SyntCol.ActivateSyntaxHighLight(self.text_id)


            #notify general plugins
            for t in self.main_window.general_plugins:
                try: #insulate from possible plugin errors
                    self.main_window.general_plugins[t].NotifyDocumentSaved()
                except: pass

            #update the ctags files with the new content
            AutoCompletition.AutoComp.UpdateCTagsFiles(self.main_window.IdRange)

            del SaveFileAs
            return True
        else:
            del SaveFileAs
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
        if self.SaveTarget == "" or self.SaveTarget == "New Document":
            self.SaveAs(0)
            return

        try:
            if Config.GetOption("StripTrails"):
                self.OnRemoveTrails(0)

            self.SaveFile(self.SaveTarget)
            self.file_size = os.path.getsize(self.SaveTarget)
            self.show_check_dlg = True
            if Config.GetOption("StatusBar"):
                self.StatusBar.SetStatusText("Saved")

            SaveContent = self.GetText()
            Log.AddLogEntry(self._("Saved file ") + self.SaveTarget)
            self.SaveRecord = SaveContent

            #notify text generalt plugins
            for t in self.main_window.general_plugins:
                try: #insulate from possible plugin errors
                    self.main_window.general_plugins[t].NotifyDocumentSaved()
                except: pass
            #update the ctags files with the new content
            AutoCompletition.AutoComp.UpdateCTagsFiles(self.main_window.IdRange)
        except:
            self.SaveAs(0)


    def Autosave(self, event):
        """
        AutoSave

        Count the numbers of characters entered. If they reach a
        value, calls Save.

        Adds a log entry.

        """
        if self.CharCount == self.autosave_interval:
            self.Save(0)
            Log.AddLogEntry(self._("Autosaved ")+self.SaveTarget)
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

        for line in xrange(sel_start, sel_end + 1):
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

        Appends a '#' at the beggining of the selected lines.
        """
        sel_end = self.LineFromPosition(self.GetSelectionEnd())
        sel_start = self.LineFromPosition(self.GetSelectionStart())
        for line in range(sel_start, sel_end+1):
            line_text = "# "+self.GetLine(line)
            ln_length = self.LineLength(line)
            st = self.GetLineEndPosition(line) - ln_length
            end = self.GetLineEndPosition(line)
            self.SetTargetStart(st+1)
            self.SetTargetEnd(end+1)
            self.ReplaceTarget(line_text)


    def OnUnComment(self,event):
        """
        OnUnComment

        Removes the '#' at teh beggining of the selected lines.
        """
        sel_end = self.LineFromPosition(self.GetSelectionEnd())
        sel_start = self.LineFromPosition(self.GetSelectionStart())
        for line in range(sel_start, sel_end+1):
            line_text = self.GetLine(line)
            #Remove Comment:
            comment = line_text.find('#')
            if comment > -1:
                line_text = line_text[comment+1:]
                ln_length = self.LineLength(line)
                st = self.GetLineEndPosition(line) - ln_length
                end = self.GetLineEndPosition(line)
                self.SetTargetStart(st+1)
                self.SetTargetEnd(end+1)
                self.ReplaceTarget(line_text)

    def SetStatusFileExt(self):
        self.StatusBar.SetStatusText(self.ext+" file.",2)


    def UpdateCords(self, event):
        """
        UpdateCords

        Updates the x,y coordinates of the cursor.
        """

        self.StatusBar.SetStatusText(self._("line: ") + str(self.GetCurrentLine()) +
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
            if Config.GetOption("Autoindentation") == True:
                try:  #to silence a useless error message

                        line = self.GetCurrentLine().rstrip()
                        if self.GetLine(line - 1)[-2] == ":":
                            self.SetLineIndentation(line, self.GetLineIndentation(line -
                                    1) + self.GetIndent())
                            self.LineEnd()
                        else:
                            self.SetLineIndentation(line, self.GetLineIndentation(line -
                                    1))
                            self.LineEnd()
                except: event.Skip()
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
        up_line = self.GetCurrentLine()
        down_line = up_line
        indent = self.GetLineIndentation(up_line)

        while True:
            if self.GetLineIndentation(up_line) >= indent:
                up_line -= 1
            elif self.GetLineIndentation(up_line) < indent:
                if self.GetLine(up_line).isspace():
                    up_line -= 1
                else: break


        while True:
            if self.GetLineIndentation(down_line) >= indent:
                down_line += 1
            elif self.GetLineIndentation(down_line) < indent:
                if self.GetLine(down_line).isspace():
                    down_line += 1
                else: break

        self.SetSelection(self.GetLineEndPosition(up_line),
                        self.GetLineEndPosition(down_line-1))


    def OnCheckFile(self,event):
        self.check_count += 1
        if self.SaveTarget != "" and self.show_check_dlg and self.check_count == 5:
            if not os.path.exists(self.SaveTarget):
                self.OnReload(0)
            else:
                if os.path.getsize(self.SaveTarget) != self.file_size:
                    check_file_ask = wx.MessageDialog(self,self._("The file ")+self.SaveTarget+self._(" has\
 been modified and the loaded buffer is out of date. Do you wish to reload it?"),self._("File Modified"),style = wx.YES | wx.NO)
                    if self.check_file_ask.ShowModal() == 5103:
                        self.OnReload(0)
                        self.check_count = 0
                    else:
                        self.check_count = 0
                        self.show_check_dlg = False
                    del self.check_file_ask
        event.Skip()

    ####################################################################
    #                        PLUGIN INTERFACE                          #
    ####################################################################
    def GetFilePath(self):
        """
        GetFilePath

        Returns the file from which the buffer is loaded.

        """
        return self.SaveTarget

    def GetFileName(self):
        """
        GetFileName

        Returns the filename of the current buffer.

        """
        return os.path.split(self.SaveTarget)[-1]

    def GetFileExtension(self):
        """
        GetFileExtension

        Returns the file extension of the current buffer.
        """
        return os.path.split(self.SaveTarget)[-1].split(".")[-1]
