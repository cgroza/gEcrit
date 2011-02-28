
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


#SyntaxHighlight.py


import wx
import keyword
import os

class SyntaxColorizer():
    def __init__(self):
        self.HOMEDIR= os.path.expanduser('~')

        self.DefaultColorDict = {'Integers': wx.Colour(181, 69, 166, 255), 'Brackets'\
        : wx.Colour(25, 57, 185, 255), 'Identifiers': wx.Colour(0, 0, 0, 255), \
        'BadEOL': wx.Colour(231, 0, 255, 255), 'Comments': wx.Colour(214, 214, 214, 255)\
        , 'Strings': wx.Colour(255, 0, 22), 'MethodNames':wx.Colour(0, 7, 255, 255),\
         'Keywords': wx.Colour(26, 32, 189, 255), 'Operators': wx.Colour(210, 147, 29, 255)\
         ,"TripleQuotes":wx.Color(210,149,29,255), "EdgeLine":wx.Color(255,0,22)}

    def ReadColorFile(self,color):
        try:
            ColorFile = open(self.HOMEDIR+"/.gEcritColor","r")
            ColorDict = eval(ColorFile.read())
            ColorDict[color]
        except:
            ColorDict = self.DefaultColorDict
            ColorFile = open(self.HOMEDIR+"/.gEcritColor","w")
            ColorFile.write(str(self.DefaultColorDict))
        ColorFile.close()
        return ColorDict[color]



    def ChangeColorFile(self,item, newcolor):
        try:
            self.DefaultColorDict[item]
            ColorFile = open(self.HOMEDIR+"/.gEcritColor","r")
            ColorDict = eval(ColorFile.read())
            ColorDict[item] = newcolor
            ColorFile = open(self.HOMEDIR+"/.gEcritColor","w")
            ColorFile.write(str(ColorDict))
        except:
            ColorDict = self.DefaultColorDict
            ColorFile = open(self.HOMEDIR+"/.gEcritColor","w")
            ColorFile.write(str(self.DefaultColorDict))
            ColorFile = open(self.HOMEDIR+"/.gEcritColor","r")
            ColorDict[item] = newcolor

        ColorFile.close()


    def ActivateSyntaxHighLight(self,text_id):
        cur_doc = wx.FindWindowById(text_id)
        cur_doc.SetLexer(wx.stc.STC_LEX_PYTHON)
        cur_doc.SetKeyWords(0, " ".join(keyword.kwlist))
        cur_doc.SetProperty("fold", "1")


        # Python styles
        # Default
        cur_doc.StyleSetSpec(wx.stc.STC_P_DEFAULT, "fore:#000000")
        # Comments
        cur_doc.StyleSetSpec(wx.stc.STC_P_COMMENTLINE, "fore:"+\
        self.ReadColorFile("Comments").GetAsString(wx.C2S_HTML_SYNTAX))

        # Number
        cur_doc.StyleSetSpec(wx.stc.STC_P_NUMBER, "fore:"+self.ReadColorFile\
        ("Integers").GetAsString(wx.C2S_HTML_SYNTAX))

        # String
        cur_doc.StyleSetSpec(wx.stc.STC_P_STRING, "fore:"+self.ReadColorFile\
        ("Strings").GetAsString(wx.C2S_HTML_SYNTAX))

        # Single quoted string
        cur_doc.StyleSetSpec(wx.stc.STC_P_CHARACTER, "fore:"+self.ReadColorFile\
        ("Strings").GetAsString(wx.C2S_HTML_SYNTAX))

        # Keyword
        cur_doc.StyleSetSpec(wx.stc.STC_P_WORD, "fore:"+self.ReadColorFile\
        ("Keywords").GetAsString(wx.C2S_HTML_SYNTAX))

        # Triple quotes
        cur_doc.StyleSetSpec(wx.stc.STC_P_TRIPLE, "fore:"+self.ReadColorFile\
        ("TripleQuotes").GetAsString(wx.C2S_HTML_SYNTAX))

        # Triple double quotes
        cur_doc.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, "fore:"+self.ReadColorFile\
        ("TripleQuotes").GetAsString(wx.C2S_HTML_SYNTAX))

        # Class name definition
        cur_doc.StyleSetSpec(wx.stc.STC_P_CLASSNAME, "fore:"+self.ReadColorFile\
        ("MethodNames").GetAsString(wx.C2S_HTML_SYNTAX)+",bold,underline")

        # Function or method name definition
        cur_doc.StyleSetSpec(wx.stc.STC_P_DEFNAME, "fore:"+self.ReadColorFile\
        ("MethodNames").GetAsString(wx.C2S_HTML_SYNTAX)+",bold,underline")

        # Operators
        cur_doc.StyleSetSpec(wx.stc.STC_P_OPERATOR,"fore:"+self.ReadColorFile\
        ("Operators").GetAsString(wx.C2S_HTML_SYNTAX))

        # Identifiers
        cur_doc.StyleSetSpec(wx.stc.STC_P_IDENTIFIER, "fore:"+self.ReadColorFile\
        ("Identifiers").GetAsString(wx.C2S_HTML_SYNTAX))

        # Comment-blocks
        cur_doc.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK, "fore:"+self.ReadColorFile\
        ("Comments").GetAsString(wx.C2S_HTML_SYNTAX))

        # End of line where string is not closed
        cur_doc.StyleSetSpec(wx.stc.STC_P_STRINGEOL, "fore:#000000,face:%s,back:"\
        +self.ReadColorFile("BadEOL").GetAsString(wx.C2S_HTML_SYNTAX)+"eol")

        cur_doc.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT,  "back:"+\
        self.ReadColorFile("Brackets").GetAsString(wx.C2S_HTML_SYNTAX))

        cur_doc.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD,    "fore:#000000,back:#FF0000,bold")

        cur_doc.SetCaretForeground("BLUE")


        cur_doc.SetEdgeColour(self.ReadColorFile("EdgeLine"))


SyntCol = SyntaxColorizer()
