#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import wx.richtext
from SyntaxHighlight import *
from configClass import *
from logClass import *
from SyntaxColor import *



def CallChangeOption(event, option, val, IdRange=0):
    """
    CallChangeOption

    Helper function used to call Config.ChangeOption.
    """
    Config.ChangeOption(option, val, IdRange)


def CallChangeColorFile(event, item, newcolor):
    """
    CallChangeColorFile

    Used to call ChangeColorFile
    """
    SyntCol.ChangeColorFile(item, newcolor)
    event.Skip()


def ToggleSpinner(event, state, widget):
    """
    ToggleSpinner

    Disables or enables the suplied widget depending on the arguments.
    """
    if state == True:
        widget.Enable()
    else:
        widget.Disable()
    event.Skip()



class CfgFrame(wx.Frame):
    """
    CfgFrame

    Creates the application configuration window and
    provides the necessary controls to modify the application
    preferences.
    """
    def __init__(self, parent, IdRange):
        """
        __init__

        Builds the entire frame GUI and binds their events across
        3 Notebook tabs.
        """
        self.parent = parent
        self._ = self.parent._
        wx.Frame.__init__(self, self.parent, -1, self._('Settings'), size=(400, 500))
        self.SetIcon(wx.Icon('icons/gEcrit.png', wx.BITMAP_TYPE_PNG))
        self.cfg_book_pnl = wx.Panel(self)
        self.book_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_bt_pnl = wx.Panel(self)

        self.ok_bt = wx.Button(self.ok_bt_pnl, -1, self._("OK"), size = (-1, -1))
        self.ok_bt.Bind(wx.EVT_BUTTON, self.HideMe)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.ConfigBook = wx.Notebook(self.cfg_book_pnl)

        self.general = GeneralSettingsPanel(self.ConfigBook, IdRange)
        self.editor = EditorSettingsPanel(self.ConfigBook, IdRange)


        self.book_sizer.Add(self.ConfigBook, 1, wx.EXPAND)
        self.cfg_book_pnl.SetSizer(self.book_sizer)
        self.cfg_book_pnl.Fit()

        self.ConfigBook.AddPage(self.general, self._("General"))
        self.ConfigBook.AddPage(self.editor, self._("Editor"))

        self.Bind(wx.EVT_CLOSE, self.HideMe)

        self.main_sizer.Add(self.cfg_book_pnl, 1, wx.EXPAND)
        self.main_sizer.Add(self.ok_bt_pnl, 0)
        self.SetSizer(self.main_sizer)
        self.Fit()
        self.Hide()
        self.Centre()

    def ShowMe(self, event):
        """
        ShowMe

        Makes window visible.
        """
        #update the id range of documents(do dinamycally update settings)
        self.IdRange = self.parent.IdRange
        self.general.IdRange = self.IdRange
        self.editor.IdRange = self.IdRange
        self.Show(True)


    def HideMe(self, event):
        """
        HideMe

        Hides the window.
        """
        self.Hide()




class GeneralSettingsPanel(wx.Panel):
    def __init__(self, parent, IdRange):
        self.parent = parent
        self._ = self.parent.GetParent().GetParent().GetParent()._
        self.IdRange = IdRange
        wx.Panel.__init__(self, self.parent)
        ColPal.CollorPaletteWindow(0, self,self.IdRange)
        sizer = wx.BoxSizer(wx.VERTICAL)

        AutosaveBox = wx.CheckBox(self, -1, self._("Enable Autosave"), (10,
                                  10), (160, -1))
        AutosaveBox.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption(event,
                         "Autosave", AutosaveBox.GetValue(), self.IdRange))

        AutosaveBox.Bind(wx.EVT_CHECKBOX, lambda event: ToggleSpinner(event,
                         AutosaveBox.GetValue(), Interval))

        Inter_Info = wx.StaticText(self, -1,
            self._("Save data each # of characters:"), (20,35))

        Interval = wx.SpinCtrl(self, -1, "", (20, 60), (90, -1))
        Interval.SetRange(1, 500)
        Interval.SetValue(Config.GetOption("Autosave Interval"))
        Interval.Bind(wx.EVT_SPINCTRL, lambda event: CallChangeOption(event,
           "Autosave Interval", Interval.GetValue(), self.IdRange))

        if not Config.GetOption("Autosave"):
            AutosaveBox.SetValue(False)
            Interval.Disable()
        else:
            AutosaveBox.SetValue(True)

        RmTrlBox = wx.CheckBox(self,-1, self._("Strip Trailing Spaces On Save"),
                                        pos = (20, 70), size = (-1, -1))
        RmTrlBox.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption(event,
                        "StripTrails", RmTrlBox.GetValue()))
        RmTrlBox.SetValue(Config.GetOption("StripTrails"))

        StatusBarBox = wx.CheckBox(self, -1, self._("Enable Status Bar"),
                                   (10, 90), (160, -1))
        StatusBarBox.Bind(wx.EVT_CHECKBOX, lambda event: \
                          CallChangeOption(event, "StatusBar",
                          StatusBarBox.GetValue(), self.IdRange))

        StatusBarBox.SetValue(Config.GetOption("StatusBar"))


        SessionBox = wx.CheckBox(self, -1, self._("Enable Session"))
        SessionBox.SetValue(Config.GetOption("Session"))
        SessionBox.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption(event,
                                       "Session",SessionBox.GetValue()))

        LogActBox = wx.CheckBox(self, -1, self._("Enable Log"), (10, 140),
                                (160, -1))

        LogActBox.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption(event,
                       "ActLog", LogActBox.GetValue(), self.IdRange))

        LogActBox.SetValue(Config.GetOption("ActLog"))

        PalleteButton = wx.Button(self, -1, self._("Colour Palette"), pos=
                                  (10, 220), size=(-1, -1))

        PalleteButton.Bind(wx.EVT_BUTTON, ColPal.ShowMe)

        ViewButton = wx.Button(self, -1,self._("View Log"), pos=(10,
                               180), size=(-1, -1))

        ViewButton.Bind(wx.EVT_BUTTON, self.viewLog)

        EraseButton = wx.Button(self, -1,self._("Erase Log"), pos=(50,
                                180), size=(-1, -1))

        EraseButton.Bind(wx.EVT_BUTTON, Log.EraseLog)
        EraseButton.Bind(wx.EVT_BUTTON, lambda event: ToggleSpinner(event,
                         False, EraseButton))


        special_sizer = wx.BoxSizer(wx.HORIZONTAL)
        special_sizer.Add(ViewButton, 0)
        special_sizer.Add(EraseButton, 0)

        sizer.Add(AutosaveBox, 0, wx.EXPAND, wx.ALL, 5)
        sizer.Add(Inter_Info, 0, wx.ALL, 5)
        sizer.Add(Interval, 0, wx.LEFT, 30)
        sizer.Add(RmTrlBox, 0 , wx.EXPAND)
        sizer.Add(StatusBarBox, 0, wx.EXPAND, wx.ALL, 5)
        sizer.Add(SessionBox, 0)
        sizer.Add(LogActBox, 0, wx.EXPAND, wx.ALL, 5)
        sizer.Add(PalleteButton, 0, wx.ALL, 5)
        sizer.Add(special_sizer, 0, wx.ALL, 5)

        self.SetSizer(sizer)

    def viewLog(self, event):
        """
        viewLog

        Creates child class and the required controls to view the log
        file.
        """
        logcontent = ""
        if Config.GetOption("ActLog") == True:

            logFrame = wx.Frame(None, -1, self._("View Log"), size=(500, 500))
            panel5 = wx.Panel(logFrame)
            data = wx.richtext.RichTextCtrl(panel5, pos=(0, 0), size=(500,
                    500), style = wx.TE_READONLY)
            data.AppendText(Log.ReadLog())
            logFrame.Centre()
            logFrame.Show()
        else:

            inform = wx.MessageDialog(None,
                    self._("The Log is disabled!\
            \nEnable it to view."),
                    self._("Log Status"), wx.OK)
            inform.ShowModal()


class EditorSettingsPanel(wx.Panel):
    def __init__(self, parent, IdRange):
        self.parent = parent
        self.IdRange = IdRange
        self._ = self.parent.GetParent().GetParent().GetParent()._
        wx.Panel.__init__(self, self.parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        LineNrBox = wx.CheckBox(self, -1, self._("Show Line Numbers"), (10,
                                10), (-1, -1))

        LineNrBox.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption(event,
                    self._("LineNumbers"), LineNrBox.GetValue(), self.IdRange))

        LineNrBox.SetValue(Config.GetOption("LineNumbers"))

        SyntaxHgBox = wx.CheckBox(self, -1, self._("Syntax Highlight"),
                                  (10, 35), (-1, -1))

        SyntaxHgBox.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption(event,
                         "SyntaxHighlight", SyntaxHgBox.GetValue(),
                         self.IdRange))

        SyntaxHgBox.SetValue(Config.GetOption("SyntaxHighlight"))

        AutoIdentBox = wx.CheckBox(self, -1, self._("Autoindentation"),
                                   (10, 60), (-1, -1))

        AutoIdentBox.Bind(wx.EVT_CHECKBOX, lambda event: \
                          CallChangeOption(event, "Autoindentation",
                          AutoIdentBox.GetValue(), self.IdRange))

        AutoIdentBox.Bind(wx.EVT_CHECKBOX, lambda event: ToggleSpinner(event,
                          AutoIdentBox.GetValue(), IndentSizeBox))

        AutoIdentBox.SetValue(Config.GetOption("Autoindentation"))

        IndentSizeBox = wx.SpinCtrl(self, -1, "", (35, 85), (90,
                                    -1))

        IndentSizeBox.SetRange(1, 12)
        IndentSizeBox.SetValue(Config.GetOption("IndentSize"))

        IndentSizeBox.Bind(wx.EVT_SPINCTRL, lambda event: \
                           CallChangeOption(event, "IndentSize",
                           IndentSizeBox.GetValue(), self.IdRange))

        if Config.GetOption("Autoindentation") == True:
            IndentSizeBox.Enable()
        else:
            IndentSizeBox.Disable()

        IndentationGuidesBox = wx.CheckBox(self, -1,
            self._("Indentation Guides"), (10, 110), (-1, -1))

        IndentationGuidesBox.SetValue(Config.GetOption("IndetationGuides"))

        IndentationGuidesBox.Bind(wx.EVT_CHECKBOX, lambda event: \
                                  CallChangeOption(event,
                                  "IndetationGuides",
                                  IndentationGuidesBox.GetValue(),
                                  self.IdRange))

        BackSpaceUnindentBox = wx.CheckBox(self, -1,
                self._("Backspace to Unindent"), (10, 135), (-1, -1))
        BackSpaceUnindentBox.SetValue(Config.GetOption("BackSpaceUnindent"))

        BackSpaceUnindentBox.Bind(wx.EVT_CHECKBOX, lambda event: \
                                  CallChangeOption(event,
                                  "BackSpaceUnindent",
                                  BackSpaceUnindentBox.GetValue(),
                                  self.IdRange))

        WhitespaceBox = wx.CheckBox(self, -1, self._("Show Whitespace"),
                                    (10, 160), (-1, -1))
        WhitespaceBox.SetValue(Config.GetOption("Whitespace"))

        WhitespaceBox.Bind(wx.EVT_CHECKBOX, lambda event: \
                           CallChangeOption(event, "Whitespace",
                           WhitespaceBox.GetValue(), self.IdRange))

        UseTabsBox = wx.CheckBox(self, -1, self._("Use Tabs"), (10, 185),
                                 (160, -1))
        UseTabsBox.SetValue(Config.GetOption("UseTabs"))

        UseTabsBox.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption(event,
           "UseTabs", UseTabsBox.GetValue(), self.IdRange))

        CarretInfo = wx.StaticText(self, -1, self._('Carret Width:'), (10,
                                   210))

        CarretWidthSpin = wx.SpinCtrl(self, -1, "", (35, 235), (-1,
                -1))
        CarretWidthSpin.SetRange(1, 20)
        CarretWidthSpin.SetValue(Config.GetOption("CarretWidth"))

        CarretWidthSpin.Bind(wx.EVT_SPINCTRL, lambda event: \
                             CallChangeOption(event, "CarretWidth",
                             CarretWidthSpin.GetValue(), self.IdRange))

        FoldMarkBox = wx.CheckBox(self, -1, self._("Fold Marks"), (10,
                                  265), (160, -1))

        FoldMarkBox.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption(event,
                         "FoldMarks", FoldMarkBox.GetValue(), self.IdRange))

        FoldMarkBox.SetValue(Config.GetOption("FoldMarks"))

        TabInfo = wx.StaticText(self, -1, self._("Tab Width:"), pos=(10,
                                300), size=(-1, -1))

        TabWidthBox = wx.SpinCtrl(self, -1, "", pos=(35, 320),
                                  size=(90, -1))

        TabWidthBox.SetValue(Config.GetOption("TabWidth"))

        TabWidthBox.Bind(wx.EVT_SPINCTRL, lambda event: CallChangeOption(event,
                         "TabWidth", TabWidthBox.GetValue(), self.IdRange))

        EdgeLineBox = wx.CheckBox(self, -1, self._("Edge Line"), pos=(10,
                                  350), size=(-1, -1))
        EdgeLineBox.SetValue(Config.GetOption("EdgeLine"))

        EdgeLineBox.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption(event,
                         "EdgeLine", EdgeLineBox.GetValue(), self.IdRange))

        EdgeLineBox.Bind(wx.EVT_CHECKBOX, lambda event: ToggleSpinner(event,
                         EdgeLineBox.GetValue(), EdgeLinePos))

        EdgeInfo = wx.StaticText(self, -1, self._("Edge Line Position:"),
                                 pos=(35, 375), size=(-1, -1))

        EdgeLinePos = wx.SpinCtrl(self, -1, "", pos=(35, 400),
                                  size=(-1, -1))
        EdgeLinePos.SetValue(Config.GetOption("EdgeColumn"))

        if Config.GetOption("EdgeLine"):
            EdgeLinePos.Enable()
        else:
            EdgeLinePos.Disable()

        EdgeLinePos.Bind(wx.EVT_SPINCTRL, lambda event: CallChangeOption(event,
                         "EdgeColumn", EdgeLinePos.GetValue(), self.IdRange))

        EdgeLinePos.SetRange(0, 1000)

        BraceCompBox = wx.CheckBox(self,-1, self._("Autocomplete Braces"),
                                            pos=(10,200),size=(-1,-1))
        BraceCompBox.Bind(wx.EVT_CHECKBOX,lambda event: CallChangeOption(
                        event,"BraceComp",BraceCompBox.GetValue(),self.IdRange))
        BraceCompBox.SetValue(Config.GetOption("BraceComp"))

        sizer.Add(LineNrBox, 0, wx.EXPAND)
        sizer.Add(SyntaxHgBox, 0, wx.EXPAND)
        sizer.Add(AutoIdentBox, 0, wx.EXPAND)
        sizer.Add(IndentSizeBox, 0, wx.LEFT, 30)
        sizer.Add(IndentationGuidesBox, 0, wx.EXPAND)
        sizer.Add(BackSpaceUnindentBox, 0, wx.EXPAND)
        sizer.Add(WhitespaceBox, 0, wx.EXPAND)
        sizer.Add(UseTabsBox, 0, wx.EXPAND, 30)
        sizer.Add(CarretInfo, 0, wx.EXPAND)
        sizer.Add(CarretWidthSpin, 0, wx.LEFT, 30)
        sizer.Add(FoldMarkBox, 0, wx.EXPAND)
        sizer.Add(TabInfo, 0, wx.EXPAND)
        sizer.Add(TabWidthBox, 0, wx.LEFT, 30)
        sizer.Add(EdgeLineBox, 0, wx.EXPAND)
        sizer.Add(EdgeInfo, 0, wx.EXPAND)
        sizer.Add(EdgeLinePos, 0, wx.LEFT, 30)
        sizer.Add(BraceCompBox,0,wx.EXPAND)

        self.SetSizer(sizer)
