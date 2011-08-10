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

import wx
import os



class SyntaxColorizer:
    """
    SyntaxColorizer

    Sets up the lexer for syntax highlighting.

    """


    def __init__(self):
        """
        __init__

        Generates a default color dictionary.

        """
        self.__HOMEDIR = os.path.expanduser('~')

        self.__default_color_dict = {
            "Integers": wx.Colour(181, 69, 166, 255),
            "Brackets": wx.Colour(25, 57, 185, 255),
            "Identifiers": wx.Colour(0, 0, 0, 255),
            "BadEOL": wx.Colour(231, 0, 255, 255),
            "Comments": wx.Colour(214, 214, 214, 255),
            "Strings": wx.Colour(255, 0, 22),
            "MethodNames": wx.Colour(0, 7, 255, 255),
            "Keywords": wx.Colour(26, 32, 189, 255),
            "Operators": wx.Colour(210, 147, 29, 255),
            "TripleQuotes": wx.Color(210, 149, 29, 255),
            "EdgeLine": wx.Color(255, 0, 22),
            }
        self.__color_dict = {}
        self.ReadColorFile()

    def GetColor(self, item):
            return self.__color_dict[item]

    def ReadColorFile(self):
        """
        ReadColorFile

        Reads the configuration file and generates
        a color dictionary for the lexer.

        """
        try:
            colour_file = open(self.__HOMEDIR + "/.gEcrit/.gEcritColor", "r")
            self.__color_dict = eval(colour_file.read())
        except:
            if not os.path.exists(self.__HOMEDIR + "/.gEcrit"):
                os.mkdir(self.__HOMEDIR + "/.gEcrit/")
            self.__color_dict = self.__default_color_dict
            colour_file = open(self.__HOMEDIR + "/.gEcrit/.gEcritColor", "w")
            colour_file.write(str(self.__default_color_dict))
        colour_file.close()

    def ChangeColorFile(self, item, newcolor):
        """
        Changecolour_file

        Modifies the value of the suplied argument item
        with the suplied argument newcolor.
        Writes changes to file.

        """
        try:
            (self.__default_color_dict)[item]
            colour_file = open(self.__HOMEDIR + "/.gEcrit/.gEcritColor", "r")
            self.__color_dict = eval(colour_file.read())
            self.__color_dict[item] = newcolor
            colour_file = open(self.__HOMEDIR + "/.gEcrit/.gEcritColor", "w")
            colour_file.write(str(self.__color_dict))
        except:
            if not os.path.exists(self.__HOMEDIR + "/.gEcrit"):
                os.mkdir(self.__HOMEDIR + "/.gEcrit/")
            self.__color_dict = self.__default_color_dict
            colour_file = open(self.__HOMEDIR + "/.gEcrit/.gEcritColor", "w")
            colour_file.write(str(self.__default_color_dict))
            colour_file = open(self.__HOMEDIR + "/.gEcrit/.gEcritColor", "r")
            self.__color_dict[item] = newcolor

        colour_file.close()


    def ActivateSyntaxHighLight(self, text_id):
        """
        ActivateSyntaxHighLight

        Initializes the lexer and sets the color styles.

        """
        cur_doc = wx.FindWindowById(text_id)
        keywords = cur_doc.lang_mode.__class__.keywords
        cur_doc.SetKeyWords(0, (" ").join(keywords))

        cur_doc.SetProperty("fold", "1")

        cur_doc.StyleSetSpec(wx.stc.STC_P_DEFAULT, "fore:#000000")

        cur_doc.StyleSetSpec(wx.stc.STC_P_COMMENTLINE, "fore:" + self.GetColor("Comments").GetAsString(wx.C2S_HTML_SYNTAX))

        cur_doc.StyleSetSpec(wx.stc.STC_P_NUMBER, "fore:" + self.GetColor("Integers").GetAsString(wx.C2S_HTML_SYNTAX))

        cur_doc.StyleSetSpec(wx.stc.STC_P_STRING, "fore:" + self.GetColor("Strings").GetAsString(wx.C2S_HTML_SYNTAX))

        cur_doc.StyleSetSpec(wx.stc.STC_P_CHARACTER, "fore:" + self.GetColor("Strings").GetAsString(wx.C2S_HTML_SYNTAX))

        cur_doc.StyleSetSpec(wx.stc.STC_P_WORD, "fore:" + self.GetColor("Keywords").GetAsString(wx.C2S_HTML_SYNTAX))

        cur_doc.StyleSetSpec(wx.stc.STC_P_TRIPLE, "fore:" + self.GetColor("TripleQuotes").GetAsString(wx.C2S_HTML_SYNTAX))

        cur_doc.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, "fore:" + self.GetColor("TripleQuotes").GetAsString(wx.C2S_HTML_SYNTAX))

        cur_doc.StyleSetSpec(wx.stc.STC_P_CLASSNAME, "fore:" + self.GetColor("MethodNames").GetAsString(wx.C2S_HTML_SYNTAX) +
                             ",bold,underline")

        cur_doc.StyleSetSpec(wx.stc.STC_P_DEFNAME, "fore:" + self.GetColor("MethodNames").GetAsString(wx.C2S_HTML_SYNTAX) +
                             ",bold,underline")

        cur_doc.StyleSetSpec(wx.stc.STC_P_OPERATOR, "fore:" + self.GetColor("Operators").GetAsString(wx.C2S_HTML_SYNTAX))

        cur_doc.StyleSetSpec(wx.stc.STC_P_IDENTIFIER, "fore:" + self.GetColor("Identifiers").GetAsString(wx.C2S_HTML_SYNTAX))

        cur_doc.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK, "fore:" + self.GetColor("Comments").GetAsString(wx.C2S_HTML_SYNTAX))

        cur_doc.StyleSetSpec(wx.stc.STC_P_STRINGEOL,
                             "fore:#000000,face:%s,back:" + self.GetColor("BadEOL").GetAsString(wx.C2S_HTML_SYNTAX) +
                             "eol")

        cur_doc.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT, "back:" + self.GetColor("Brackets").GetAsString(wx.C2S_HTML_SYNTAX))

        cur_doc.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD,
                             "fore:#000000,back:#FF0000,bold")

        cur_doc.SetCaretForeground("BLUE")

        cur_doc.SetEdgeColour(self.GetColor("EdgeLine"))



SyntCol = SyntaxColorizer()
