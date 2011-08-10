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
        
    # every method will be passed the event argument. The method must not event.Skip() it.
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

