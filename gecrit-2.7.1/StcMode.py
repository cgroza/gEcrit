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
        sel_end = self.stc_ctrl.LineFromPosition(self.stc_ctrl.GetSelectionEnd())
        sel_start = self.stc_ctrl.LineFromPosition(self.stc_ctrl.GetSelectionStart())
        for line in xrange(sel_start, sel_end+1):
            ln_length = self.stc_ctrl.LineLength(line)
            if line == sel_end + 1:
                st = self.stc_ctrl.GetLineEndPosition(line) - ln_length
            else:
                st = self.stc_ctrl.GetLineEndPosition(line) - ln_length + 1
            self.stc_ctrl.InsertText(st, comment_string)

    def UnCommentSelection(self, comment_string):
        """
        This is a helper function for child classes.
        It removes the leading @comment_string in selectod lines.
        """
        sel_end = self.stc_ctrl.LineFromPosition(self.stc_ctrl.GetSelectionEnd())
        sel_start = self.stc_ctrl.LineFromPosition(self.stc_ctrl.GetSelectionStart())
        for line in range(sel_start, sel_end+1):
            line_text = self.stc_ctrl.GetLine(line)
            #Remove Comment:
            comment = line_text.find(comment_string)
            if comment > -1:
                line_text = line_text[comment+len(comment_string):]
                ln_length = self.stc_ctrl.LineLength(line)
                st = self.stc_ctrl.GetLineEndPosition(line) - ln_length
                end = self.stc_ctrl.GetLineEndPosition(line)
                self.stc_ctrl.SetTargetStart(st+1)
                self.stc_ctrl.SetTargetEnd(end+1)
                self.stc_ctrl.ReplaceTarget(line_text)

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

