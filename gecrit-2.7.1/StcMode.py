import wx
import wx.lib.inspection

class StcMode(object):
    """
    This class is an interface for all clases that want to implement a Mode for the StyledTextControl
    The children class must overwrite all the empty methods and all None instance variables.
    This class will be passed an wx.StyledTextCtrl and can have an enourmous amount of control over it.
    """
    lexer = None                # a lexer that will provide syntax highlight for the control.
                                # Must be part of wx.stc.STC_LEX####
    lang_name = ""              # language name eg: python, ruby...
    file_extensions = []       # a list of file extensions that this mode is candidate for. (format: ["py","pyw"])
    keywords = []             # a keyword list for this mode. (format: ["for","while"])
    def __init__(self, stc_ctrl):
        self.stc_ctrl = stc_ctrl
        
    def CommentSelection(self, comment_string):
        """
        This is a helper function for child classes.
        It appends @comment_string in front of every selected line.

        """
        # from drPython source code
        selstart, selend = self.stc_ctrl.GetSelection()
        #From the start of the first line selected
        oldcursorpos = self.stc_ctrl.GetCurrentPos()
        startline = self.stc_ctrl.LineFromPosition(selstart)
        self.stc_ctrl.GotoLine(startline)
        start = self.stc_ctrl.GetCurrentPos()
        #To the end of the last line selected
        #Bugfix Chris Wilson
        #Edited by Dan (selend fix)
        if selend == selstart:
            tend = selend
        else:
            tend = selend - 1

        docstring = comment_string

        end = self.stc_ctrl.GetLineEndPosition(self.stc_ctrl.LineFromPosition(tend))
        #End Bugfix Chris Wilson
        eol = self.stc_ctrl.GetEndOfLineCharacter()
        corr = 0
        l = len(self.stc_ctrl.GetText())
        # if self.prefs.doccommentmode == 0:
        self.stc_ctrl.SetSelection(start, end)
        text = docstring + self.stc_ctrl.GetSelectedText()
        text = text.replace(eol, eol + docstring)
        self.stc_ctrl.ReplaceSelection(text)
        corr = len(self.stc_ctrl.GetText()) - l
        self.stc_ctrl.GotoPos(oldcursorpos + corr)

    def UnCommentSelection(self, comment_string):
        """
        This is a helper function for child classes.
        It removes the leading @comment_string in selectod lines.
        """

        #from drPython source code
        #franz: pos is not used
        selstart, selend = self.stc_ctrl.GetSelection()
        #From the start of the first line selected
        startline = self.stc_ctrl.LineFromPosition(selstart)
        oldcursorpos = self.stc_ctrl.GetCurrentPos()
        self.stc_ctrl.GotoLine(startline)
        start = self.stc_ctrl.GetCurrentPos()
        #To the end of the last line selected
        #Bugfix Chris Wilson
        #Edited by Dan (selend fix)
        if selend == selstart:
            tend = selend
        else:
            tend = selend - 1
        end = self.stc_ctrl.GetLineEndPosition(self.stc_ctrl.LineFromPosition(tend))
        #End Bugfix Chris Wilson

        mask = self.stc_ctrl.GetModEventMask()
        self.stc_ctrl.SetModEventMask(0)
        lpos = start
        newtext = ""
        l = len(self.stc_ctrl.GetText())
        docstring = comment_string
        ldocstring = len(docstring)
        while lpos < end:
            lpos = self.stc_ctrl.PositionFromLine(startline)
            line = self.stc_ctrl.GetLine(startline)
            lc = line.find(docstring)
            if lc > -1:
                prestyle = self.stc_ctrl.GetStyleAt(lpos + lc - 1)
                style = self.stc_ctrl.GetStyleAt(lpos + lc)

                newtext += line[0:lc] + line[lc+ldocstring:]
            else:
                newtext += line
            startline += 1
            lpos = self.stc_ctrl.PositionFromLine(startline)
        self.stc_ctrl.SetModEventMask(mask)
        self.stc_ctrl.SetSelection(start, end)
        self.stc_ctrl.ReplaceSelection(newtext.rstrip(self.stc_ctrl.GetEndOfLineCharacter()))
        corr = len(self.stc_ctrl.GetText()) - l
        self.stc_ctrl.GotoPos(oldcursorpos + corr)

    # every method will be passed the event argument. The method must not event.Skip() it.
    #interface functions
    def OnComment(self, event):
        """This method will mangage commenting selections of text."""
        pass

    def OnUnComment(self, event):
        """ This method will manage uncommenting selections of text."""
        pass

    def AutoIndent(self, event):
        """
        This method will be called when the Enter key is pressed and autoindentation is enabled.
        This method must manage autoindentation.
        """
        pass

    def OnSelectCodeBlock(self, event):
        """
        This method manages selecting code blocks.
        """
        pass

