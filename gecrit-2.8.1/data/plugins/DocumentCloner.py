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

from data.plugins.categories import General
import yapsy.IPlugin
import wx


class DocumentCloner(General, yapsy.IPlugin.IPlugin):
    def __init__(self):
        self.name = "Document Cloner"

    def Init(self, parent):
        self.parent = parent

        self.plugins_menu = wx.Menu()
        clone_entry = self.plugins_menu.Append(-1,"Clone Current Document")

        self.menu_item = self.parent.AddToMenuBar("Document Cloner",
                                                      self.plugins_menu)
        self.parent.BindMenubarEvent(clone_entry, self.OnClone)

    def OnClone(self, event):
        origin = self.parent.GetCurrentDocument()
        doc =  self.parent.CreateNewDocument(self.parent.GetCurrentDocument
                                             ().GetFileName()+" -Clone")
        doc.SetText(origin.GetText())
