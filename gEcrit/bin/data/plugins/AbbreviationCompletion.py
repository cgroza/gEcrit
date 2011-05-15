import wx, os
import yapsy.IPlugin
from data.plugins.categories import General

class AbbreviationSettingsWin(wx.Frame):
    def __init__(self, parent):
        self.parent = parent

        self.config_path = self.parent.HOMEDIR+"/.gEcrit/AbbreviationCompletion.conf"

        wx.Frame.__init__(self,self.parent, -1,"Abbreviation Editor" , size = (500,300))
        self.main_panel = wx.Panel(self)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.abbr_ctrl_sizer = wx.BoxSizer(wx.VERTICAL)
        self.bt_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.abbr_list = wx.ListCtrl(self.main_panel,style=wx.LC_REPORT)
        self.abbr_list.InsertColumn(0, "Abbreviaton")
        self.abbr_list.SetColumnWidth(0, 150)
        self.abbr_list.InsertColumn(1, "Value")
        self.abbr_list.SetColumnWidth(1, 350)
        self.abbreviations = []

        self.selected_abbr = None
        self.abbr_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)
        self.abbr_list.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnSelect)

        self.add_abbr_bt = wx.Button(self.main_panel, -1, "Add")
        self.add_abbr_bt.Bind(wx.EVT_BUTTON, self.OnAddAbbreviation)

        self.remove_abbr_bt = wx.Button(self.main_panel, -1, "Remove")
        self.remove_abbr_bt.Bind(wx.EVT_BUTTON, self.OnRemoveAbbreviation)

        self.new_abbr_txt_lbl = wx.StaticText(self.main_panel,-1,"Abbreviation:")
        self.new_abbr_txt = wx.TextCtrl(self.main_panel, -1)
        self.new_abbr_val_txt_lbl = wx.StaticText(self.main_panel,-1,"Abbreviation Value:")
        self.new_abbr_val_txt = wx.TextCtrl(self.main_panel, -1)

        self.abbr_ctrl_sizer.AddSpacer(5)
        self.abbr_ctrl_sizer.Add(self.new_abbr_txt_lbl,0)
        self.abbr_ctrl_sizer.AddSpacer(5)
        self.abbr_ctrl_sizer.Add(self.new_abbr_txt, 0 , wx.EXPAND)
        self.abbr_ctrl_sizer.AddSpacer(5)
        self.abbr_ctrl_sizer.Add(self.new_abbr_val_txt_lbl, 0)
        self.abbr_ctrl_sizer.AddSpacer(5)
        self.abbr_ctrl_sizer.Add(self.new_abbr_val_txt, 0 , wx.EXPAND)

        self.bt_sizer.Add(self.add_abbr_bt, 0)
        self.bt_sizer.AddSpacer(5)
        self.bt_sizer.Add(self.remove_abbr_bt, 0)

        self.main_sizer.Add(self.abbr_list, 1, wx.EXPAND)
        self.main_sizer.Add(self.abbr_ctrl_sizer, 0 , wx.EXPAND)
        self.main_sizer.AddSpacer(10)
        self.main_sizer.Add(self.bt_sizer, 0)
        self.main_panel.SetSizer(self.main_sizer)
        self.main_panel.Fit()
        self.Populate()
        self.Bind(wx.EVT_CLOSE, self.HideMe)
        self.Hide()

    def Populate(self):
        self.abbr_list.DeleteAllItems()
        self.ReadAbbrConfig()
        for a in self.abbreviations:
            self.abbr_list.Append(a)


    def ReadAbbrConfig(self):
        if os.path.exists(self.config_path):
            cfg_fl = open(self.config_path,"r")
            self.abbreviations = eval(cfg_fl.read())
        else:
            cfg_fl = open(self.config_path,"w")
            cfg_fl.write(str([]))
            cfg_fl.close()

    def SaveAbbrConfig(self):
        cfg_fl = open(self.config_path,"w")
        cfg_fl.write(str(self.abbreviations))
        cfg_fl.close()

    def OnAddAbbreviation(self, event):
        abbr = self.new_abbr_txt.GetValue()
        abbr_val = self.new_abbr_val_txt.GetValue()
        if not abbr.isspace() and not abbr_val.isspace():
            self.abbreviations.append([abbr,abbr_val])
            self.abbr_list.Append([abbr,abbr_val])
            self.SaveAbbrConfig()

    def OnSelect(self, event):
        self.selected_abbr = event.GetSelection()

    def OnDeselect(self, event):
        self.selected_abbr = None

    def OnRemoveAbbreviation(self, event):
        if self.selected_abbr == None:
            return

        self.abbr_list.DeleteItem(self.selected_abbr)
        items = self.abbr_list.GetItemCount()
        if items == 0:
            self.abbreviations = []

        for i in xrange(0, items):
            txt = self.abbr_list.GetItemText(i)
            k = 0
            v = False
            for j in self.abbreviations:
                if txt == j[0]: v = True ;break
                k += 1
            if v:
                self.abbreviations.pop(k)

        self.SaveAbbrConfig()

    def ShowMe(self, event):
        self.Show()

    def HideMe(self,event):
        self.Hide()

class AbbreviationCompletion(yapsy.IPlugin.IPlugin, General):
    def __init__(self):
        self.name = "Abbreviation Completion"

    def Init(self, parent):
        self.parent = parent
        self.pref_win = AbbreviationSettingsWin(self.parent)
        self.current_doc = None
        #creating plugin menu entry

        self.plugins_menu = wx.Menu()
        edit_entry = self.plugins_menu.Append(-1,"Edit Abbreviations")

        self.menu_item = self.parent.AddToMenuBar("Abbreviation Completion",
                                                      self.plugins_menu)
        self.parent.BindMenubarEvent(edit_entry, self.pref_win.ShowMe)

    def NotifyDocumentOpened(self):
        self.current_doc = self.parent.GetCurrentDocument()
        self.current_doc.Bind(wx.stc.EVT_STC_CHARADDED, self.OnEditorChar)

    def NotifyTabChanged(self):
        self.current_doc = self.parent.GetCurrentDocument()

    def NotifyNewTabOpened(self):
        self.NotifyDocumentOpened()

    def ReplaceAbbr(self):
        abbr_found = False
        abbr_val = None
        st = self.current_doc.WordStartPosition(self.current_doc.GetCurrentPos()-1, False)
        end = self.current_doc.WordEndPosition(self.current_doc.GetCurrentPos()-1, False)
        word = self.current_doc.GetTextRange(st, end)
        for a in self.pref_win.abbreviations:
            if word.rstrip() == a[0].rstrip():
                abbr_found = True
                abbr_val = a[1]
                break

        if abbr_found:
            self.current_doc.SetTargetStart(st)
            self.current_doc.SetTargetEnd(end)
            self.current_doc.ReplaceTarget(abbr_val)
            self.current_doc.WordRight()
            return True
        return False

    def OnEditorChar(self, event):
        key = event.GetKey()
        if chr(key).isspace():
          if self.ReplaceAbbr():
            self.current_doc.InsertText(self.current_doc.GetCurrentPos(),chr(key))
            self.current_doc.CharRight()
        event.Skip()

    def Stop(self):
         self.parent.RemoveFromMenubar(self.menu_item)
         self.pref_win.Destroy()
