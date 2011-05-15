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
  

    def CollorPaletteWindow(self, event, parent,IdRange):
        """
        CollorPaletteWindow

        Builds the GUI controls and binds the necessary
        binds to the corresponding functions.
        """
        wx.Frame.__init__(self, self.parent, -1, "Colour Palette", size=
                          (145, 530))
        self._ = parent._      
        self.SetIcon(wx.Icon('icons/gEcrit.png', wx.BITMAP_TYPE_PNG))
        CPalettePanel = wx.Panel(self)
        self.Bind(wx.EVT_CLOSE, self.HideMe)
        color_sizer = wx.BoxSizer(wx.VERTICAL)

        CPalettePanel.SetAutoLayout(True)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        CPalettePanel.SetSizer(mainSizer)

        KeyWordSel = csel.ColourSelect(CPalettePanel, -1, self._("Keywords"),
                SyntCol.ReadColorFile("Keywords"), pos=(10, 10), size=(121,
                35))

        KeyWordSel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                        "Keywords"))

        StringsSel = csel.ColourSelect(CPalettePanel, -1, self._("Strings"),
                SyntCol.ReadColorFile("Strings"), pos=(10, 50), size=(121,
                35))
        StringsSel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                        "Strings"))

        Quote3Sel = csel.ColourSelect(CPalettePanel, -1, self._("Triple Quotes"),
                SyntCol.ReadColorFile("TripleQuotes"), pos=(10, 90),
                size=(121, 35))
        Quote3Sel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                       "TripleQuotes"))

        IntSel = csel.ColourSelect(CPalettePanel, -1, self._("Integers"),
                                   SyntCol.ReadColorFile("Integers"),
                                   pos=(10, 130), size=(121, 35))
        IntSel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                    "Integers"))

        CommentSel = csel.ColourSelect(CPalettePanel, -1, self._("Comments"),
                SyntCol.ReadColorFile("Comments"), pos=(10, 170), size=(121,
                35))
        CommentSel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                        "Comments"))

        BracketSel = csel.ColourSelect(CPalettePanel, -1, self._("Brackets"),
                SyntCol.ReadColorFile("Brackets"), pos=(10, 210), size=(121,
                35))
        BracketSel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                        "Brackets"))

        BadEOLSel = csel.ColourSelect(CPalettePanel, -1, self._("Bad EOL"),
                SyntCol.ReadColorFile("BadEOL"), pos=(10, 250), size=(121,
                35))
        BadEOLSel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                       "BadEOL"))

        FuncSel = csel.ColourSelect(CPalettePanel, -1, self._("Method Names"),
                                    SyntCol.ReadColorFile("MethodNames"),
                                    pos=(10, 290), size=(121, 35))
        FuncSel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                     "MethodNames"))

        OperatorSel = csel.ColourSelect(CPalettePanel, -1, self._("Operators"),
                SyntCol.ReadColorFile("Operators"), pos=(10, 330), size=
                (121, 35))
        OperatorSel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                         "Operators"))

        IdentifierSel = csel.ColourSelect(CPalettePanel, -1,
                self._("Identifiers"), SyntCol.ReadColorFile("Identifiers"), pos=
                (10, 370), size=(121, 35))
        IdentifierSel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                           "Identifiers"))

        EdgeLnSel = csel.ColourSelect(CPalettePanel, -1, self._("Edge Line"),
                SyntCol.ReadColorFile("EdgeLine"), pos=(10, 410), size=(121,
                35))

        EdgeLnSel.Bind(csel.EVT_COLOURSELECT, lambda event: self.OnSelectColor(event,
                       "EdgeLine"))

        OKButton = wx.Button(CPalettePanel, -1, self._("OK"), pos=(35, 455),
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

    def RefreshLexer(self, event, IdRange):
        """
        RefreshLexer

        Updates the lexer with the changes.
        """
        for id in IdRange:
            SyntCol.ActivateSyntaxHighLight(id)
        event.Skip()


ColPal = ColorPFrame()
