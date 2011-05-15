import wx
from data.plugins.categories import General
import yapsy

class WordCounter(wx.Frame, General, yapsy.IPlugin.IPlugin):
    def __init__(self):
        self.name = "Word Counter"

    def Init(self, parent):
        self.parent = parent
        self.current_doc = None

        wx.Frame.__init__(self, self.parent, -1, "Word Counter" ,size = (300 , 132))

        self.main_panel = wx.Panel(self)
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.plugins_menu = wx.Menu()
        show_entry = self.plugins_menu.Append(-1, "Advanced")
        words_entry = self.plugins_menu.Append(-1, "Count Words")
        char_entry = self.plugins_menu.Append(-1, "Count Characters" )

        self.count_desc = wx.StaticText(self.main_panel,-1,"Count:")
        self.count_string = wx.TextCtrl(self.main_panel)
        self.count_bt = wx.Button(self.main_panel, -1, "Count",
                                                        size = (-1, -1))

        self.case_sesitive = wx.CheckBox(self.main_panel, -1, "Case Sensitive")
        self.occurrences = wx.StaticText(self.main_panel, -1, "Occurrences: ")

        self.h_sizer.Add(self.count_string, 1, wx.EXPAND)
        self.h_sizer.AddSpacer(10)
        self.h_sizer.Add(self.count_bt)

        self.close = wx.Button(self.main_panel, -1, "Close")

        self.v_sizer.Add(self.count_desc)
        self.v_sizer.Add(self.h_sizer, 0, wx.EXPAND)
        self.v_sizer.AddSpacer(5)
        self.v_sizer.Add(self.case_sesitive)
        self.v_sizer.AddSpacer(5)
        self.v_sizer.Add(self.occurrences, 0 ,wx.EXPAND)
        self.v_sizer.AddSpacer(5)
        self.v_sizer.Add(self.close)

        self.menu_item = self.parent.AddToMenuBar("Word Counter",
                                                      self.plugins_menu)

        self.parent.BindMenubarEvent(show_entry, self.ShowMe)
        self.parent.BindMenubarEvent(words_entry, self.OnMenuWordCount)
        self.parent.BindMenubarEvent(char_entry, self.OnMenuCharCount)


        self.main_panel.SetSizer(self.v_sizer)
        self.main_panel.Fit()

        self.Bind(wx.EVT_CLOSE, self.HideMe)
        self.close.Bind(wx.EVT_BUTTON, self.HideMe)
        self.count_bt.Bind(wx.EVT_BUTTON, self.OnWordCount)
        self.Hide()

    def NotifyTabChanged(self):
        self.current_doc = self.parent.GetCurrentDocument()

    def OnWordCount(self, event):
        if self.case_sesitive.GetValue():
            self.occurrences.SetLabel("Occurrences: " + str(
            self.current_doc.GetText().lower().count(self.count_string.GetValue().lower())))
        else:
            self.occurrences.SetLabel("Occurrences: " + str(
            self.current_doc.GetText().count(self.count_string.GetValue())))

    def OnMenuCharCount(self, event):
        msg = str(self.current_doc.GetText().count(""))
        show = wx.MessageDialog(None, msg+" character have been counted.",
            style = wx.OK)
        show.ShowModal()


    def OnMenuWordCount(self, event):
        msg = str(len(self.current_doc.GetText().split()))
        show = wx.MessageDialog(None, msg+" words have been counted.",
            style = wx.OK)
        show.ShowModal()


    def ShowMe(self, event):
        self.Show()

    def HideMe(self, event):
        self.Hide()
