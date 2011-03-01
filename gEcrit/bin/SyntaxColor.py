#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
from SyntaxHighlight import *
import wx.lib.colourselect as csel


class ColorPFrame(wx.Frame):

    def __init__(self, parent=None):
        self.parent = parent

    def CollorPaletteWindow(self, event, IdRange):
        wx.Frame.__init__(self, self.parent, -1, "Colour Palette", size=
                          (145, 530))

        self.SetIcon(wx.Icon('icons/gEcrit.png', wx.BITMAP_TYPE_PNG))
        CPalettePanel = wx.Panel(self)
        self.Bind(wx.EVT_CLOSE, self.HideMe)
        color_sizer = wx.BoxSizer(wx.VERTICAL)

        CPalettePanel.SetAutoLayout(True)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        CPalettePanel.SetSizer(mainSizer)

        KeyWordSel = csel.ColourSelect(CPalettePanel, -1, "Keywords",
                SyntCol.ReadColorFile("Keywords"), pos=(10, 10), size=(121,
                35))

        KeyWordSel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                        "Keywords"))

        StringsSel = csel.ColourSelect(CPalettePanel, -1, "Strings",
                SyntCol.ReadColorFile("Strings"), pos=(10, 50), size=(121,
                35))
        StringsSel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                        "Strings"))

        Quote3Sel = csel.ColourSelect(CPalettePanel, -1, "Triple Quotes",
                SyntCol.ReadColorFile("TripleQuotes"), pos=(10, 90),
                size=(121, 35))
        Quote3Sel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                       "TripleQuotes"))

        IntSel = csel.ColourSelect(CPalettePanel, -1, "Integers",
                                   SyntCol.ReadColorFile("Integers"),
                                   pos=(10, 130), size=(121, 35))
        IntSel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                    "Integers"))

        CommentSel = csel.ColourSelect(CPalettePanel, -1, "Comments",
                SyntCol.ReadColorFile("Comments"), pos=(10, 170), size=(121,
                35))
        CommentSel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                        "Comments"))

        BracketSel = csel.ColourSelect(CPalettePanel, -1, "Brackets",
                SyntCol.ReadColorFile("Brackets"), pos=(10, 210), size=(121,
                35))
        BracketSel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                        "Brackets"))

        BadEOLSel = csel.ColourSelect(CPalettePanel, -1, "Bad EOL",
                SyntCol.ReadColorFile("BadEOL"), pos=(10, 250), size=(121,
                35))
        BadEOLSel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                       "BadEOL"))

        FuncSel = csel.ColourSelect(CPalettePanel, -1, "Method Names",
                                    SyntCol.ReadColorFile("MethodNames"),
                                    pos=(10, 290), size=(121, 35))
        FuncSel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                     "MethodNames"))

        OperatorSel = csel.ColourSelect(CPalettePanel, -1, "Operators",
                SyntCol.ReadColorFile("Operators"), pos=(10, 330), size=
                (121, 35))
        OperatorSel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                         "Operators"))

        IdentifierSel = csel.ColourSelect(CPalettePanel, -1,
                "Identifiers", SyntCol.ReadColorFile("Identifiers"), pos=
                (10, 370), size=(121, 35))
        IdentifierSel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                           "Identifiers"))

        EdgeLnSel = csel.ColourSelect(CPalettePanel, -1, "Edge Line",
                SyntCol.ReadColorFile("EdgeLine"), pos=(10, 410), size=(121,
                35))

        EdgeLnSel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                       "EdgeLine"))

        OKButton = wx.Button(CPalettePanel, -1, "OK", pos=(35, 455),
                             size=(-1, -1))
        OKButton.Bind(wx.EVT_BUTTON, lambda event: self.Close(True))
        OKButton.Bind(wx.EVT_BUTTON, lambda event: self.RefreshLexer(event,
                      IdRange))
        OKButton.Bind(wx.EVT_BUTTON, lambda event: self.RefreshLexer(event,
                      IdRange))

        color_sizer.Add(KeyWordSel, 0, wx.EXPAND | wx.ALL, 5)
        color_sizer.Add(StringsSel, 0, wx.EXPAND | wx.ALL, 5)
        color_sizer.Add(Quote3Sel, 0, wx.EXPAND | wx.ALL, 5)
        color_sizer.Add(IntSel, 0, wx.EXPAND | wx.ALL, 5)
        color_sizer.Add(CommentSel, 0, wx.EXPAND | wx.ALL, 5)
        color_sizer.Add(BracketSel, 0, wx.EXPAND | wx.ALL, 5)
        color_sizer.Add(BadEOLSel, 0, wx.EXPAND | wx.ALL, 5)
        color_sizer.Add(FuncSel, 0, wx.EXPAND | wx.ALL, 5)
        color_sizer.Add(OperatorSel, 0, wx.EXPAND | wx.ALL, 5)
        color_sizer.Add(IdentifierSel, 0, wx.EXPAND | wx.ALL, 5)
        color_sizer.Add(EdgeLnSel, 0, wx.EXPAND | wx.ALL, 5)
        color_sizer.Add(OKButton, 0, wx.EXPAND | wx.ALL, 5)

        CPalettePanel.SetSizer(color_sizer)
        self.Hide()
        self.Centre()

    def HideMe(self, event):
        self.Hide()

    def ShowMe(self, event):
        self.Show()

    def OnSelectColor(self, event, item):
        SyntCol.ChangeColorFile(item, event.GetValue())

    def RefreshLexer(self, event, IdRange):
        for id in IdRange:
            SyntCol.ActivateSyntaxHighLight(id)
        event.Skip()


ColPal = ColorPFrame()
