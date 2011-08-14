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

import wx, gettext
from SyntaxHighlight import *
import wx.lib.colourselect as csel



class ColorPFrame(wx.Frame):
    """
    ColorPFrame

    Provides the necessary function and control to modify
    the lexer styles.
    """
    def __init__(self, parent=None):
        """
        __init__

        Makes its parent class global.
        """
        self.parent = parent
  

    def CollorPaletteWindow(self, event, parent,id_range):
        """
        CollorPaletteWindow

        Builds the GUI controls and binds the necessary
        binds to the corresponding functions.
        """
        wx.Frame.__init__(self, self.parent, -1, "Colour Palette", size=
                          (145, 530))
        self._ = parent._      
        self.SetIcon(wx.Icon('icons/gEcrit.png', wx.BITMAP_TYPE_PNG))
        cpalette_panel = wx.Panel(self)
        self.Bind(wx.EVT_CLOSE, self.HideMe)
        color_sizer = wx.BoxSizer(wx.VERTICAL)

        cpalette_panel.SetAutoLayout(True)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        cpalette_panel.SetSizer(mainSizer)

        keyword_sel = csel.ColourSelect(cpalette_panel, -1, self._("Keywords"),
                SyntCol.GetColor("Keywords"), pos=(10, 10), size=(121,
                35))

        keyword_sel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                        "Keywords"))

        strings_sel = csel.ColourSelect(cpalette_panel, -1, self._("Strings"),
                SyntCol.GetColor("Strings"), pos=(10, 50), size=(121,
                35))
        strings_sel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                        "Strings"))

        quote3_sel = csel.ColourSelect(cpalette_panel, -1, self._("Triple Quotes"),
                SyntCol.GetColor("TripleQuotes"), pos=(10, 90),
                size=(121, 35))
        quote3_sel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                       "TripleQuotes"))

        int_sel = csel.ColourSelect(cpalette_panel, -1, self._("Integers"),
                                   SyntCol.GetColor("Integers"),
                                   pos=(10, 130), size=(121, 35))
        int_sel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                    "Integers"))

        comments_sel = csel.ColourSelect(cpalette_panel, -1, self._("Comments"),
                SyntCol.GetColor("Comments"), pos=(10, 170), size=(121,
                35))
        comments_sel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                        "Comments"))

        brackets_sel = csel.ColourSelect(cpalette_panel, -1, self._("Brackets"),
                SyntCol.GetColor("Brackets"), pos=(10, 210), size=(121,
                35))
        brackets_sel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                        "Brackets"))

        bad_eol_sel = csel.ColourSelect(cpalette_panel, -1, self._("Bad EOL"),
                SyntCol.GetColor("BadEOL"), pos=(10, 250), size=(121,
                35))
        bad_eol_sel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                       "BadEOL"))

        function_sel = csel.ColourSelect(cpalette_panel, -1, self._("Method Names"),
                                    SyntCol.GetColor("MethodNames"),
                                    pos=(10, 290), size=(121, 35))
        function_sel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                     "MethodNames"))

        operator_sel = csel.ColourSelect(cpalette_panel, -1, self._("Operators"),
                SyntCol.GetColor("Operators"), pos=(10, 330), size=
                (121, 35))
        operator_sel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                         "Operators"))

        identifier_sel = csel.ColourSelect(cpalette_panel, -1,
                self._("Identifiers"), SyntCol.GetColor("Identifiers"), pos=
                (10, 370), size=(121, 35))
        identifier_sel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                           "Identifiers"))

        edge_line_sel = csel.ColourSelect(cpalette_panel, -1, self._("Edge Line"),
                SyntCol.GetColor("EdgeLine"), pos=(10, 410), size=(121,
                35))

        edge_line_sel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                       "EdgeLine"))

        ok_button = wx.Button(cpalette_panel, -1, self._("OK"), pos=(35, 455),
                             size=(-1, -1))
        ok_button.Bind(wx.EVT_BUTTON, lambda event: self.Close(True))
        ok_button.Bind(wx.EVT_BUTTON, lambda event: self.RefreshLexer(event,
                      id_range))
        ok_button.Bind(wx.EVT_BUTTON, lambda event: self.RefreshLexer(event,
                      id_range))

        color_sizer.Add(keyword_sel, 0, wx.EXPAND | wx.ALL, 5)
        color_sizer.Add(strings_sel, 0, wx.EXPAND | wx.ALL, 5)
        color_sizer.Add(quote3_sel, 0, wx.EXPAND | wx.ALL, 5)
        color_sizer.Add(int_sel, 0, wx.EXPAND | wx.ALL, 5)
        color_sizer.Add(comments_sel, 0, wx.EXPAND | wx.ALL, 5)
        color_sizer.Add(brackets_sel, 0, wx.EXPAND | wx.ALL, 5)
        color_sizer.Add(bad_eol_sel, 0, wx.EXPAND | wx.ALL, 5)
        color_sizer.Add(function_sel, 0, wx.EXPAND | wx.ALL, 5)
        color_sizer.Add(operator_sel, 0, wx.EXPAND | wx.ALL, 5)
        color_sizer.Add(identifier_sel, 0, wx.EXPAND | wx.ALL, 5)
        color_sizer.Add(edge_line_sel, 0, wx.EXPAND | wx.ALL, 5)
        color_sizer.Add(ok_button, 0, wx.EXPAND | wx.ALL, 5)

        cpalette_panel.SetSizer(color_sizer)
        self.Hide()
        self.Centre()

    def HideMe(self, event):
        """
        HideMe

        Hides the window.
        """
        self.Hide()

    def ShowMe(self, event):
        """
        ShowMe

        Makes window visible.
        """
        self.Show()

    def OnSelectColor(self, event, item):
        """
        OnSelectColor

        Helper function to call SyntCol.ChangeColorFile
        """
        SyntCol.ChangeColorFile(item, event.GetValue())

    def RefreshLexer(self, event, id_range):
        """
        RefreshLexer

        Updates the lexer with the changes.
        """
        for id in id_range:
            stc_control = wx.FindWindowById(id)
            stc_control.ActivateSyntaxHighLight()
        event.Skip()


ColPal = ColorPFrame()
