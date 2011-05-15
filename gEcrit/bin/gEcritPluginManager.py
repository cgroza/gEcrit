import wx, gettext
from configClass import *

class gEcritPluginManager(wx.Frame):
    def __init__(self, parent, id = -1):
        self.parent = parent
        self._ = self.parent._

        wx.Frame.__init__(self, self.parent, id, self._("Plugin Manager"),
                                size = (510, 435), pos = (-1, -1))
        self._ = self.parent._
        self.main_panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.button_sizer = wx.BoxSizer(wx.VERTICAL)


        self.remove_pl = wx.Button(self.main_panel, -1,self._("Remove"),
                                                        size = (110,40))
        self.remove_pl.Bind(wx.EVT_BUTTON, self.OnDeletePlugin)

        #self.install_pl = wx.Button(self.main_panel, -1,"Install",
        #                                               size = (110,40))

        font = wx.Font(18, wx.ROMAN ,wx.BOLD, wx.NORMAL)
        self.pl_list_desc = wx.StaticText(self.main_panel, -1, self._("Plugins:"),
                                                         size = (-1,-1))
        self.pl_list_desc.SetFont(font)

        self.plugin_list = wx.CheckListBox(self,-1, size = (380,280),
                              style = wx.LB_MULTIPLE | wx.RAISED_BORDER|wx.LB_ALWAYS_SB)
        self.plugin_list_selection = False

        self.Bind(wx.EVT_LISTBOX, self.OnListItemClick)

        self.pl_description = wx.TextCtrl(self.main_panel,-1,
                              size = (380,100), style = wx.TE_MULTILINE)
        self.pl_description.SetEditable(False)



        self.button_sizer.Add(self.remove_pl, 0 , wx.EXPAND)
        self.button_sizer.AddSpacer(10)
        #self.button_sizer.Add(self.install_pl, 0 , wx.EXPAND)

        self.horizontal_sizer.AddSpacer(5)
        self.horizontal_sizer.Add(self.plugin_list, 1, wx.EXPAND)
        self.horizontal_sizer.AddSpacer(10)
        self.horizontal_sizer.Add(self.button_sizer, 0, wx.EXPAND)

        self.main_sizer.AddSpacer(5)
        self.main_sizer.Add(self.pl_list_desc, 0 , wx.EXPAND)
        self.main_sizer.AddSpacer(10)
        self.main_sizer.Add(self.horizontal_sizer, 1, wx.EXPAND)
        self.main_sizer.AddSpacer(5)
        self.main_sizer.Add(self.pl_description, 0 , wx.EXPAND)

        self.main_panel.SetSizer(self.main_sizer)
        self.main_panel.Fit()
        self.pl_lst = []
        self.PopulatePluginList()
        self.Hide()
        self.Bind(wx.EVT_CLOSE, self.HideMe)

    def PopulatePluginList(self):
        self.parent.plugin_manager.locatePlugins()
        self.pl_lst = self.parent.plugin_manager.getPluginCandidates()
        index = 0
        for p in self.pl_lst:
            self.plugin_list.AppendAndEnsureVisible(p[2].name)
            if p[2].name in self.parent.activated_plugins:
                self.plugin_list.Check(index, True)
            index += 1

    def OnDeletePlugin(self, event):
        if self.plugin_list_selection >= 0:
            os.remove(self.pl_lst[self.plugin_list_selection][0])
            os.remove(self.pl_lst[self.plugin_list_selection][1] + ".py")

            self.pl_lst.pop(self.plugin_list_selection)
            self.plugin_list.Delete(self.plugin_list_selection)
            #update config file
            conf = Config.GetOption("ActivePlugins")
            conf = list(self.plugin_list.GetCheckedStrings())
            Config.ChangeOption("ActivePlugins", conf)

    #def OnInstallPlugins(self, event):
    #    self.plugin_list.GetChecked()



    def OnListItemClick(self,event):
        plugin = self.pl_lst[event.GetSelection()]

        #read and display plugin description
        self.pl_description.SetValue(self._("Author: ") + plugin[2].author  + "\n"+
                                     self._("Version: ") + plugin[2].version + "\n"+
                                     self._("Website: ") + plugin[2].website + "\n"+
                                     self._("Description: ")+plugin[2].description + "\n")

        #update config file
        conf = Config.GetOption("ActivePlugins")
        conf = list(self.plugin_list.GetCheckedStrings())
        Config.ChangeOption("ActivePlugins", conf)
        self.plugin_list_selection = event.GetSelection()


    def ShowMe(self, event):
        self.Show()

    def HideMe(self, event):
        self.Hide()
