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
        self.CommentSelection("#")


    def OnUnComment(self, event):
        self.UnCommentSelection("#")

    def AutoIndent(self, event):
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
        max_line = self.stc_ctrl.GetLineCount()
        while up_line > 0:
            if self.stc_ctrl.GetLineIndentation(up_line) >= indent:
                up_line -= 1
            elif self.stc_ctrl.GetLineIndentation(up_line) < indent:
                if self.stc_ctrl.GetLine(up_line).isspace():
                    up_line -= 1
                else: break

        while down_line < max_line:
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
    __block_start = ["begin", "BEGIN", "case", "class", "def", "do", "else",
                     "elseif", "ensure", "for", "if", "module", "rescue",
                     "then", "unless", "until", "when", "while"]
    __block_end = ["end", "END", ]
    
    def __init__(self, stc_ctrl):
        StcMode.__init__(self, stc_ctrl)
        
    def OnComment(self, event):
        self.CommentSelection("#")

    def OnUnComment(self, event):
        self.UnCommentSelection("#")
        
    def AutoIndent(self, event):
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
        up_line = self.stc_ctrl.GetCurrentLine()
        down_line = up_line

        max_line = self.stc_ctrl.GetLineCount()
        
        cur_line = ""

        while up_line > 0:
            cur_line = self.stc_ctrl.GetLine(up_line)
            if cur_line.isspace():
                pass
            elif StcRubyMode.__HasBlockStart(cur_line):
                break
            up_line -= 1

        ignore_delims = 0       # to keep track of nested blocks
        orig_line = down_line
        while down_line < max_line:
            cur_line = self.stc_ctrl.GetLine(down_line)
            if cur_line.isspace():
                pass
            elif StcRubyMode.__HasBlockStart(cur_line) and down_line != orig_line:
                ignore_delims += 1
            elif StcRubyMode.__HasBlockEnd(cur_line) and ignore_delims == 0:
                break
            down_line += 1

        self.stc_ctrl.SetSelection(self.stc_ctrl.GetLineEndPosition(up_line),
                                   self.stc_ctrl.GetLineEndPosition(down_line-1))

    # helper functions for OnSelectCodeBlock
    @staticmethod
    def __HasBlockStart(line):
        """ This method checks for Ruby block Starters"""
        line = line.split()
        for word in line:
            if word in StcRubyMode.__block_start:
                return True
        return False

    @staticmethod
    def __HasBlockEnd(line):
        """ This class check for Ruby block such as end """
        line = line.split()
        for word in line:  
            if word in StcRubyMode.__block_end:
                return True
        return False

class StcCppMode(StcMode):
    lexer = wx.stc.STC_LEX_CPP
    file_extensions = ["h", "cpp" ,"hpp", "c", "cxx", "C"]
    keywords = ["auto",
                "const",
                "double",
                "float",
                "int",
                "short",
                "struct",
                "unsigned",
                "break",
                "continue",
                "else",
                "for",
                "long",
                "signed",
                "switch",
                "void",
                "case",
                "default",
                "enum",
                "goto",
                "register",
                "sizeof",
                "typedef",
                "volatile","char",
                "do",
                "extern",
                "if",
                "return",
                "static",
                "union",
                "while",
                "asm",
                "dynamic_cast",
                "namespace",
                "reinterpret_cast",
                "try",
                "bool",
                "explicit",
                "new",
                "static_cast",
                "typeid",
                "catch",
                "false",
                "operator",
                "template",
                "typename",
                "class","friend",
                "private",
                "this"
                "using",
                "const_cast",
                "inline",
                "public",
                "throw",
                "virtual",
                "delete",
                "mutable",
                "protected",
                "true",
                "wchar_t"]

    lang_name = "C/C++"

    def __init__(self, stc_ctrl):
        StcMode.__init__(self, stc_ctrl)

    def OnComment(self, event):
        self.CommentSelection("//")

    def OnUnComment(self, event):
        # remove the  // in front of every selected line
        self.UnCommentSelection("//")
        
    def AutoIndent(self, event):
        try:  #to silence a useless error message
            line = self.stc_ctrl.GetCurrentLine()
            if self.stc_ctrl.GetLine(line - 1)[-2].rstrip() == "{":
                self.stc_ctrl.SetLineIndentation(line,self.stc_ctrl.GetLineIndentation(line-1)+self.stc_ctrl.GetIndent())
                self.stc_ctrl.LineEnd()
            else:
                self.stc_ctrl.SetLineIndentation(line, self.stc_ctrl.GetLineIndentation(line - 1))
                self.stc_ctrl.LineEnd()
        except: event.Skip()


    def OnSelectCodeBlock(self, event):
        up_line = self.stc_ctrl.GetCurrentLine()
        down_line = up_line
        max_line = self.stc_ctrl.GetLineCount()

        cur_line = ""

        while up_line > 0 or "{" in cur_line:
            cur_line = self.stc_ctrl.GetLine(up_line)
            up_line -= 1

        cur_line = ""
        ignore_delim = 0        # to keep track of nested blocks
        orig_line = down_line
        while down_line < max_line:
            cur_line = self.stc_ctrl.GetLine(down_line)
            if down_line == orig_line:
                pass
            elif "}" in cur_line and ignore_delim == 0:
                break
            down_line += 1

        self.stc_ctrl.SetSelection(self.stc_ctrl.GetLineEndPosition(up_line),
                                   self.stc_ctrl.GetLineEndPosition(down_line-1))


class StcPerlMode(StcMode):
    """
    This class implements the Perl mode.
    """
    lexer = wx.stc.STC_LEX_PERL
    file_extensions = ["perl", "pl"]
    keywords = ["if",
                "unless",
                "else",
                "elsif",
                "for",
                "foreach",
                "while",
                "until",
                "continue",
                "do",
                "use",
                "no",
                "last",
                "next",
                "redo",
                "goto",
                "my",
                "our",
                "state",
                "local",
                "sub",
                "eval",
                "package",
                "require",
                "defined",
                "delete",
                "eval",
                "exists",
                "grep",
                "map",
                "pos",
                "print",
                "return",
                "scalar",
                "sort",
                "split",
                "undef",
                "chop",
                "abs",
                "binmode",
                "bless",
                "caller",
                "chdir",
                "chr",
                "close",
                "die",
                "each",
                "glob",
                "hex",
                "index",
                "int",
                "join",
                "keys",
                "lc",
                "lcfirst",
                "length",
                "oct",
                "open",
                "ord",
                "pipe",
                "pop",
                "push",
                "quotemeta",
                "readline",
                "ref",
                "reverse",
                "rmdir",
                "shift",
                "splice",
                "sprintf",
                "substr",
                "uc",
                "ucfirst",
                "unlink",
                "unshift",
                "values",
                "vec",
                "wantarray",
                "warn"]

    lang_name = "Perl"

    def OnComment(self, event):
        self.CommentSelection("#")

    def OnUnComment(self, event):
        self.UnCommentSelection("#")


    def AutoIndent(self, event):
        try:  #to silence a useless error message
            line = self.stc_ctrl.GetCurrentLine()
            if self.stc_ctrl.GetLine(line - 1)[-2].rstrip() == "{":
                self.stc_ctrl.SetLineIndentation(line,self.stc_ctrl.GetLineIndentation(line-1)+self.stc_ctrl.GetIndent())
                self.stc_ctrl.LineEnd()
            else:
                self.stc_ctrl.SetLineIndentation(line, self.stc_ctrl.GetLineIndentation(line - 1))
                self.stc_ctrl.LineEnd()
        except: event.Skip()


    def OnSelectCodeBlock(self, event):
        up_line = self.stc_ctrl.GetCurrentLine()
        down_line = up_line
        max_line = self.stc_ctrl.GetLineCount()

        cur_line = ""

        while up_line > 0 or "{" in cur_line:
            cur_line = self.stc_ctrl.GetLine(up_line)
            up_line -= 1

        cur_line = ""
        ignore_delim = 0        # to keep track of nested blocks
        orig_line = down_line
        while down_line < max_line:
            cur_line = self.stc_ctrl.GetLine(down_line)
            if down_line == orig_line:
                pass
            elif "}" in cur_line and ignore_delim == 0:
                break
            down_line += 1

        self.stc_ctrl.SetSelection(self.stc_ctrl.GetLineEndPosition(up_line),
                                   self.stc_ctrl.GetLineEndPosition(down_line-1))


class StcJavaMode(StcCppMode):
    lexer = wx.stc.STC_LEX_CPP
    file_extensions = ["java"]
    keywords = ["abstract",
        "continue",
        "for",
        "new",
        "switch",  
        "assert",
        "default",
        "package",
        "synchronized",
        "boolean",
        "do",
        "if",
        "private",
        "this",
        "break",
        "double",
        "implements",
        "protected",
        "throw",
        "byte",
        "else",
        "import",
        "public",
        "throws",
        "case",
        "enum",
        "instanceof",
        "return",
        "transient",
        "catch",
        "extends",
        "int",
        "short",
        "try",
        "char",
        "final",
        "interface",
        "static",
        "void",
        "class",
        "finally",
        "long",
        "volatile",
        "float",
        "native",
        "super",
        "while"]
    lang_name = "Java"

    def __init__(self, stc_ctrl):
        StcCppMode.__init__(self, stc_ctrl)


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
