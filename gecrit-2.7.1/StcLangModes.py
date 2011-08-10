from StcMode import StcMode
import keyword
import wx
import wx.lib.inspection

class StcPythonMode(StcMode):
    """ This class implements a python language mode."""
    lexer = wx.stc.STC_LEX_PYTHON
    file_extensions = ["py","pyw"]
    keywords = keyword.kwlist
    lang_name = "Python"
    def __init__(self, stc_ctrl):
        StcMode.__init__(self, stc_ctrl)

    def OnComment(self, event):
        sel_end = self.stc_ctrl.LineFromPosition(self.stc_ctrl.GetSelectionEnd())
        sel_start = self.stc_ctrl.LineFromPosition(self.stc_ctrl.GetSelectionStart())
        for line in range(sel_start, sel_end+1):
            line_text = "# "+self.stc_ctrl.GetLine(line)
            ln_length = self.stc_ctrl.LineLength(line)
            st = self.stc_ctrl.GetLineEndPosition(line) - ln_length
            end = self.stc_ctrl.GetLineEndPosition(line)
            self.stc_ctrl.SetTargetStart(st+1)
            self.stc_ctrl.SetTargetEnd(end+1)
            self.stc_ctrl.ReplaceTarget(line_text)

    def OnUnComment(self, event):
        sel_end = self.stc_ctrl.LineFromPosition(self.stc_ctrl.GetSelectionEnd())
        sel_start = self.stc_ctrl.LineFromPosition(self.stc_ctrl.GetSelectionStart())
        for line in range(sel_start, sel_end+1):
            line_text = self.stc_ctrl.GetLine(line)
            #Remove Comment:
            comment = line_text.find('#')
            if comment > -1:
                line_text = line_text[comment+1:]
                ln_length = self.stc_ctrl.LineLength(line)
                st = self.stc_ctrl.GetLineEndPosition(line) - ln_length
                end = self.stc_ctrl.GetLineEndPosition(line)
                self.stc_ctrl.SetTargetStart(st+1)
                self.stc_ctrl.SetTargetEnd(end+1)
                self.stc_ctrl.ReplaceTarget(line_text)

    def AutoIndent(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_NUMPAD_ENTER or key == wx.WXK_RETURN:
            try:  #to silence a useless error message
                line = self.stc_ctrl.GetCurrentLine()
                if self.stc_ctrl.GetLine(line - 1)[-2].rstrip() == ":":
                    self.stc_ctrl.SetLineIndentation(line,self.stc_ctrl.GetLineIndentation(line-1)+self.stc_ctrl.GetIndent())
                    self.stc_ctrl.LineEnd()
                else:
                    self.stc_ctrl.SetLineIndentation(line, self.stc_ctrl.GetLineIndentation(line - 1))
                    self.stc_ctrl.LineEnd()
            except: event.Skip()


    def OnSelectCodeBlock(self, event):
        up_line = self.stc_ctrl.GetCurrentLine()
        down_line = up_line
        indent = self.stc_ctrl.GetLineIndentation(up_line)

        while True:
            if self.stc_ctrl.GetLineIndentation(up_line) >= indent:
                up_line -= 1
            elif self.stc_ctrl.GetLineIndentation(up_line) < indent:
                if self.stc_ctrl.GetLine(up_line).isspace():
                    up_line -= 1
                else: break

        while True:
            if self.stc_ctrl.GetLineIndentation(down_line) >= indent:
                down_line += 1
            elif self.stc_ctrl.GetLineIndentation(down_line) < indent:
                if self.stc_ctrl.GetLine(down_line).isspace():
                    down_line += 1
                else: break

        self.stc_ctrl.SetSelection(self.stc_ctrl.GetLineEndPosition(up_line),
                                   self.stc_ctrl.GetLineEndPosition(down_line-1))

        
class StcRubyMode(StcMode):
    """
    This class implements the Ruby language mode.
    """

    lexer = wx.stc.STC_LEX_RUBY
    file_extensions= ["rb"] 
    keywords = ["alias",
                "and",
                "BEGIN",
                "begin",
                "break",
                "case",
                "class",
                "def",
                "defined",
                "do",
                "else",
                "elsif",
                "END",
                "end,"
                "ensure",
                "false",
                "for",
                "if",
                "in",
                "module",
                "next",
                "nil",
                "not",
                "or",
                "redo",
                "rescue",
                "retry",
                "return",
                "self",
                "super",
                "then",
                "true",
                "undef",
                "unless",
                "until",
                "when",
                "while",
                "yield"]

    lang_name = "Ruby"

    def __init__(self, stc_ctrl):
        StcMode.__init__(self, stc_ctrl)
        
    def OnComment(self, event):
        sel_end = self.stc_ctrl.LineFromPosition(self.stc_ctrl.GetSelectionEnd())
        sel_start = self.stc_ctrl.LineFromPosition(self.stc_ctrl.GetSelectionStart())
        for line in range(sel_start, sel_end+1):
            line_text = "# "+self.stc_ctrl.GetLine(line)
            ln_length = self.stc_ctrl.LineLength(line)
            st = self.stc_ctrl.GetLineEndPosition(line) - ln_length
            end = self.stc_ctrl.GetLineEndPosition(line)
            self.stc_ctrl.SetTargetStart(st+1)
            self.stc_ctrl.SetTargetEnd(end+1)
            self.stc_ctrl.ReplaceTarget(line_text)

    def OnUnComment(self, event):
        sel_end = self.stc_ctrl.LineFromPosition(self.stc_ctrl.GetSelectionEnd())
        sel_start = self.stc_ctrl.LineFromPosition(self.stc_ctrl.GetSelectionStart())
        for line in range(sel_start, sel_end+1):
            line_text = self.stc_ctrl.GetLine(line)
            #Remove Comment:
            comment = line_text.find('#')
            if comment > -1:
                line_text = line_text[comment+1:]
                ln_length = self.stc_ctrl.LineLength(line)
                st = self.stc_ctrl.GetLineEndPosition(line) - ln_length
                end = self.stc_ctrl.GetLineEndPosition(line)
                self.stc_ctrl.SetTargetStart(st+1)
                self.stc_ctrl.SetTargetEnd(end+1)
                self.stc_ctrl.ReplaceTarget(line_text)

    def AutoIndent(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_NUMPAD_ENTER or key == wx.WXK_RETURN:
            linenr = self.stc_ctrl.GetCurrentLine()
            line = self.stc_ctrl.GetLine(linenr - 1)
            if not line.isspace():
                line = line.split()
                if line[-1].rstrip() in ["do","begin","ensure","{","else","then"] or line[0].lstrip() in ["def","class", "module", "rescue","while", "for", "when", "if", "case", "until","unless"]:
                    self.stc_ctrl.SetLineIndentation(linenr,self.stc_ctrl.GetLineIndentation(linenr-1)+self.stc_ctrl.GetIndent())
                    self.stc_ctrl.LineEnd()
                else:
                    self.stc_ctrl.SetLineIndentation(linenr, self.stc_ctrl.GetLineIndentation(linenr - 1))
                    self.stc_ctrl.LineEnd()

            else:
                self.stc_ctrl.SetLineIndentation(linenr, self.stc_ctrl.GetLineIndentation(linenr - 1))
                self.stc_ctrl.LineEnd()

    def OnSelectCodeBlock(self, event):
        pass



class StcFundamentalMode(StcMode):
    """
    This mode is used for files for wich no appropriate mode exists.
    """

    lexer = wx.stc.STC_LEX_NULL
    file_extensions = []
    keywords = []
    lang_name = "Fundamental"
    def __init__(self, stc_ctrl):
        self.stc_ctrl = stc_ctrl
        StcMode.__init__(self, stc_ctrl);
