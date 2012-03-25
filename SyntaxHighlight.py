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



class SyntaxHighlight:
    """
    SyntaxColorizer

    Sets up the lexer for syntax highlighting.

    """


    def __init__(self):
        """
        __init__

        Generates a default color dictionary.

        """

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

        self.__HOMEDIR = os.path.expanduser('~')
        self.cfg_path = os.path.join(self.__HOMEDIR, ".gEcrit", ".gEcritColor")
        self.cfg_dir = os.path.join(self.__HOMEDIR, ".gEcrit")
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
            colour_file = open(self.cfg_path, "r")
            self.__color_dict = eval(colour_file.read())
        except:
            if not os.path.exists(self.cfg_dir):
                os.mkdir(self.cfg_dir)
            self.__color_dict = self.__default_color_dict
            colour_file = open(self.cfg_path, "w")
            colour_file.write(str(self.__default_color_dict))
        colour_file.close()

    def ChangeColorFile(self, item, newcolor):
        """
        Changecolour_file

        Modifies the value of the suplied argument item
        with the suplied argument newcolor.
        Writes changes to file.

        """
        self.__color_dict[item] = newcolor
        with open(self.cfg_path, "w") as colour_file:
            colour_file.write(str(self.__color_dict))



SyntCol = SyntaxHighlight()
