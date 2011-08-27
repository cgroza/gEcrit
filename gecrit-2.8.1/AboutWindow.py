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

class AboutWindow():
    """
    AboutWindow

    Constructs and about window.

    """

    def __init__(self):
        """
        __init__

        Initializes the AboutDialogInfo object and sets
        all the required data.
        """
        AboutInfo = wx.AboutDialogInfo()
        AboutInfo.Name = "gEcrit"
        AboutInfo.Version = "2.8.1"
        AboutInfo.Copyright = """
gEcrit 2.7
The Python Code Editor"""
        AboutInfo.Developers = ["Groza Anna e-mail: anna.balerina@yahoo.com\n",
                                 "Groza Cristian e-mail: kristi9524@gmail.com\n",
                                "Groza Mihai e-mail: grozam@ymail.com\n",
                                 "Victor Pruteanu e-mail: vikkhackerz@gmail.com"]
        AboutInfo.Website = "http://www.cristigrozatips.do.am"
        AboutInfo.License = \
            """
  Copyright (C) 2011  Groza Cristian

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
        wx.AboutBox(AboutInfo)

