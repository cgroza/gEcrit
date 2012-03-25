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
import wx.richtext
from SyntaxHighlight import *
from Configuration import *
from Logger import *
from ColorPFrame import *



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
    def __init__(self, parent):
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
        self.config_book = wx.Notebook(self.cfg_book_pnl)

        self.general = GeneralSettingsPanel(self.config_book, self.parent.id_range)
        self.editor = EditorSettingsPanel(self.config_book, self.parent.id_range)


        self.book_sizer.Add(self.config_book, 1, wx.EXPAND)
        self.cfg_book_pnl.SetSizer(self.book_sizer)
        self.cfg_book_pnl.Fit()

        self.config_book.AddPage(self.general, self._("General"))
        self.config_book.AddPage(self.editor, self._("Editor"))

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
        self.id_range = self.parent.id_range
        self.general.id_range = self.id_range
        self.editor.id_range = self.id_range
        self.Show(True)


    def HideMe(self, event):
        """
        HideMe

        Hides the window.
        """
        self.Hide()




class GeneralSettingsPanel(wx.Panel):
    def __init__(self, parent, id_range):
        self.parent = parent
        self._ = self.parent.GetParent().GetParent().GetParent()._
        self.id_range = id_range
        wx.Panel.__init__(self, self.parent)
        ColPal.CollorPaletteWindow(0, self,self.id_range)
        sizer = wx.BoxSizer(wx.VERTICAL)

        autosave_box = wx.CheckBox(self, -1, self._("Enable Autosave"), (10,
                                  10), (160, -1))
        autosave_box.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption(event,
                         "Autosave", autosave_box.GetValue(), self.id_range))


        inter_info = wx.StaticText(self, -1,
            self._("Save interval in minutes:"), (20,35))

        interval_spin_ctrl = wx.SpinCtrl(self, -1, "", (20, 60), (90, -1))
        interval_spin_ctrl.SetRange(1, 500)
        interval_spin_ctrl.SetValue(Config.GetOption("Autosave Interval"))
        interval_spin_ctrl.Bind(wx.EVT_SPINCTRL, lambda event: CallChangeOption(event,
           "Autosave Interval", interval_spin_ctrl.GetValue(), self.id_range))

        autosave_box.Bind(wx.EVT_CHECKBOX, lambda event: ToggleSpinner(event,
                         autosave_box.GetValue(), interval_spin_ctrl))


        autosave_box.SetValue(Config.GetOption("Autosave"))
        interval_spin_ctrl.Enable(Config.GetOption("Autosave"))

        strip_trail_box = wx.CheckBox(self,-1, self._("Strip Trailing Spaces On Save"),
                                        pos = (20, 70), size = (-1, -1))
        strip_trail_box.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption(event,
                        "StripTrails", strip_trail_box.GetValue()))
        strip_trail_box.SetValue(Config.GetOption("StripTrails"))

        status_bar_box = wx.CheckBox(self, -1, self._("Enable Status Bar"),
                                   (10, 90), (160, -1))
        status_bar_box.Bind(wx.EVT_CHECKBOX, lambda event: \
                          CallChangeOption(event, "StatusBar",
                          status_bar_box.GetValue(), self.id_range))

        status_bar_box.SetValue(Config.GetOption("StatusBar"))


        session_box = wx.CheckBox(self, -1, self._("Enable Session"))
        session_box.SetValue(Config.GetOption("Session"))
        session_box.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption(event,
                                       "Session",session_box.GetValue()))

        log_act_box = wx.CheckBox(self, -1, self._("Enable Log"), (10, 140),
                                (160, -1))

        log_act_box.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption(event,
                       "ActLog", log_act_box.GetValue(), self.id_range))

        log_act_box.SetValue(Config.GetOption("ActLog"))

        pallete_button = wx.Button(self, -1, self._("Colour Palette"), pos=
                                  (10, 220), size=(-1, -1))

        pallete_button.Bind(wx.EVT_BUTTON, ColPal.ShowMe)

        view_button = wx.Button(self, -1,self._("View Log"), pos=(10,
                               180), size=(-1, -1))

        view_button.Bind(wx.EVT_BUTTON, self.viewLog)

        erase_button = wx.Button(self, -1,self._("Erase Log"), pos=(50,
                                180), size=(-1, -1))

        erase_button.Bind(wx.EVT_BUTTON, Log.EraseLog)
        erase_button.Bind(wx.EVT_BUTTON, lambda event: ToggleSpinner(event,
                         False, erase_button))


        special_sizer = wx.BoxSizer(wx.HORIZONTAL)
        special_sizer.Add(view_button, 0)
        special_sizer.Add(erase_button, 0)

        sizer.Add(autosave_box, 0, wx.EXPAND, wx.ALL, 5)
        sizer.Add(inter_info, 0, wx.ALL, 5)
        sizer.Add(interval_spin_ctrl, 0, wx.LEFT, 30)
        sizer.Add(strip_trail_box, 0 , wx.EXPAND)
        sizer.Add(status_bar_box, 0, wx.EXPAND, wx.ALL, 5)
        sizer.Add(session_box, 0)
        sizer.Add(log_act_box, 0, wx.EXPAND, wx.ALL, 5)
        sizer.Add(pallete_button, 0, wx.ALL, 5)
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

            log_frame = wx.Frame(None, -1, self._("View Log"), size=(500, 500))
            panel5 = wx.Panel(log_frame)
            data = wx.richtext.RichTextCtrl(panel5, pos=(0, 0), size=(500,
                    500), style = wx.TE_READONLY)
            data.AppendText(Log.ReadLog())
            log_frame.Centre()
            log_frame.Show()
        else:

            inform = wx.MessageDialog(None,
                    self._("The Log is disabled!\
            \nEnable it to view."),
                    self._("Log Status"), wx.OK)
            inform.ShowModal()


class EditorSettingsPanel(wx.Panel):
    def __init__(self, parent, id_range):
        self.parent = parent
        self.id_range = id_range
        self._ = self.parent.GetParent().GetParent().GetParent()._
        wx.Panel.__init__(self, self.parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        line_nr_box = wx.CheckBox(self, -1, self._("Show Line Numbers"), (10,
                                10), (-1, -1))

        line_nr_box.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption(event,
                    self._("LineNumbers"), line_nr_box.GetValue(), self.id_range))

        line_nr_box.SetValue(Config.GetOption("LineNumbers"))

        syntax_highlight_box = wx.CheckBox(self, -1, self._("Syntax Highlight"),
                                  (10, 35), (-1, -1))

        syntax_highlight_box.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption(event,
                         "SyntaxHighlight", syntax_highlight_box.GetValue(),
                         self.id_range))

        syntax_highlight_box.SetValue(Config.GetOption("SyntaxHighlight"))

        autoindent_box = wx.CheckBox(self, -1, self._("Autoindentation"),
                                   (10, 60), (-1, -1))

        autoindent_box.Bind(wx.EVT_CHECKBOX, lambda event: \
                          CallChangeOption(event, "Autoindentation",
                          autoindent_box.GetValue(), self.id_range))

        autoindent_box.SetValue(Config.GetOption("Autoindentation"))

        indent_size_spinctrl = wx.SpinCtrl(self, -1, "", (35, 85), (90,
                                    -1))
        autoindent_box.Bind(wx.EVT_CHECKBOX, lambda event: ToggleSpinner(event,
                          autoindent_box.GetValue(), indent_size_spinctrl))

        indent_size_spinctrl.SetRange(1, 12)
        indent_size_spinctrl.SetValue(Config.GetOption("IndentSize"))

        indent_size_spinctrl.Bind(wx.EVT_SPINCTRL, lambda event: \
                           CallChangeOption(event, "IndentSize",
                           indent_size_spinctrl.GetValue(), self.id_range))

        if Config.GetOption("Autoindentation") == True:
            indent_size_spinctrl.Enable()
        else:
            indent_size_spinctrl.Disable()

        indent_guides_box = wx.CheckBox(self, -1,
            self._("Indentation Guides"), (10, 110), (-1, -1))

        indent_guides_box.SetValue(Config.GetOption("IndetationGuides"))

        indent_guides_box.Bind(wx.EVT_CHECKBOX, lambda event: \
                                  CallChangeOption(event,
                                  "IndetationGuides",
                                  indent_guides_box.GetValue(),
                                  self.id_range))

        backspc_unindent_box = wx.CheckBox(self, -1,
                self._("Backspace to Unindent"), (10, 135), (-1, -1))
        backspc_unindent_box.SetValue(Config.GetOption("BackSpaceUnindent"))

        backspc_unindent_box.Bind(wx.EVT_CHECKBOX, lambda event: \
                                  CallChangeOption(event,
                                  "BackSpaceUnindent",
                                  backspc_unindent_box.GetValue(),
                                  self.id_range))

        whitespc_box = wx.CheckBox(self, -1, self._("Show Whitespace"),
                                    (10, 160), (-1, -1))
        whitespc_box.SetValue(Config.GetOption("Whitespace"))

        whitespc_box.Bind(wx.EVT_CHECKBOX, lambda event: \
                           CallChangeOption(event, "Whitespace",
                           whitespc_box.GetValue(), self.id_range))

        use_tabs_box = wx.CheckBox(self, -1, self._("Use Tabs"), (10, 185),
                                 (160, -1))
        use_tabs_box.SetValue(Config.GetOption("UseTabs"))

        use_tabs_box.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption(event,
           "UseTabs", use_tabs_box.GetValue(), self.id_range))

        caret_info = wx.StaticText(self, -1, self._('Carret Width:'), (10,
                                   210))

        caret_width_spinctrl = wx.SpinCtrl(self, -1, "", (35, 235), (-1,
                -1))
        caret_width_spinctrl.SetRange(1, 20)
        caret_width_spinctrl.SetValue(Config.GetOption("CarretWidth"))

        caret_width_spinctrl.Bind(wx.EVT_SPINCTRL, lambda event: \
                             CallChangeOption(event, "CarretWidth",
                             caret_width_spinctrl.GetValue(), self.id_range))

        fold_marks_box = wx.CheckBox(self, -1, self._("Fold Marks"), (10,
                                  265), (160, -1))

        fold_marks_box.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption(event,
                         "FoldMarks", fold_marks_box.GetValue(), self.id_range))

        fold_marks_box.SetValue(Config.GetOption("FoldMarks"))

        tab_info = wx.StaticText(self, -1, self._("Tab Width:"), pos=(10,
                                300), size=(-1, -1))

        tab_width_box = wx.SpinCtrl(self, -1, "", pos=(35, 320),
                                  size=(90, -1))

        tab_width_box.SetValue(Config.GetOption("TabWidth"))

        tab_width_box.Bind(wx.EVT_SPINCTRL, lambda event: CallChangeOption(event,
                         "TabWidth", tab_width_box.GetValue(), self.id_range))

        edge_line_box = wx.CheckBox(self, -1, self._("Edge Line"), pos=(10,
                                  350), size=(-1, -1))
        edge_line_box.SetValue(Config.GetOption("EdgeLine"))

        edge_line_box.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption(event,
                         "EdgeLine", edge_line_box.GetValue(), self.id_range))

        edge_line_box.Bind(wx.EVT_CHECKBOX, lambda event: ToggleSpinner(event,
                         edge_line_box.GetValue(), edge_line_pos))

        edge_info = wx.StaticText(self, -1, self._("Edge Line Position:"),
                                 pos=(35, 375), size=(-1, -1))

        edge_line_pos = wx.SpinCtrl(self, -1, "", pos=(35, 400),
                                  size=(-1, -1))
        edge_line_pos.SetValue(Config.GetOption("EdgeColumn"))

        if Config.GetOption("EdgeLine"):
            edge_line_pos.Enable()
        else:
            edge_line_pos.Disable()

        edge_line_pos.Bind(wx.EVT_SPINCTRL, lambda event: CallChangeOption(event,
                         "EdgeColumn", edge_line_pos.GetValue(), self.id_range))

        edge_line_pos.SetRange(0, 1000)

        brace_comp_box = wx.CheckBox(self,-1, self._("Autocomplete Braces"),
                                            pos=(10,200),size=(-1,-1))
        brace_comp_box.Bind(wx.EVT_CHECKBOX,lambda event: CallChangeOption(
                        event,"BraceComp",brace_comp_box.GetValue(),self.id_range))
        brace_comp_box.SetValue(Config.GetOption("BraceComp"))

        sizer.Add(line_nr_box, 0, wx.EXPAND)
        sizer.Add(syntax_highlight_box, 0, wx.EXPAND)
        sizer.Add(autoindent_box, 0, wx.EXPAND)
        sizer.Add(indent_size_spinctrl, 0, wx.LEFT, 30)
        sizer.Add(indent_guides_box, 0, wx.EXPAND)
        sizer.Add(backspc_unindent_box, 0, wx.EXPAND)
        sizer.Add(whitespc_box, 0, wx.EXPAND)
        sizer.Add(use_tabs_box, 0, wx.EXPAND, 30)
        sizer.Add(caret_info, 0, wx.EXPAND)
        sizer.Add(caret_width_spinctrl, 0, wx.LEFT, 30)
        sizer.Add(fold_marks_box, 0, wx.EXPAND)
        sizer.Add(tab_info, 0, wx.EXPAND)
        sizer.Add(tab_width_box, 0, wx.LEFT, 30)
        sizer.Add(edge_line_box, 0, wx.EXPAND)
        sizer.Add(edge_info, 0, wx.EXPAND)
        sizer.Add(edge_line_pos, 0, wx.LEFT, 30)
        sizer.Add(brace_comp_box,0,wx.EXPAND)

        self.SetSizer(sizer)
