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


import wx.lib.inspection
import sys, types
import collections
from Configuration import *
from Logger import *
from AboutWindow import *
from SyntaxHighlight import *
from ConfigWindow import *
from PrettyPrinter import *
from FindReplaceText import *
from AutoComplet import *
from StcTextCtrl import *
from Menu import *
from Toolbar import *
from gEcritPluginManager import *
from yapsy.PluginManager import PluginManager
from data.plugins.categories import *
from AuiNoteBook import *
from gEcritSession import *
import Exceptions
import wx.aui

import gettext
import logging
logging.basicConfig(level=logging.DEBUG)


class gEcrit(wx.Frame):
    """
    Editor

    This class is the entry point in the program.
    It creates all the user interface and initializes
    the required objects and classes.
    The functions that cannot go into another objects
    for diverse reasons go here.
    """

    def dummy_tr(self, tr):
        return tr

    def __init__(self, id, parent):
        """
        __init__

        Creates the user interface.
        Initializez the terminals if enabled.
        Creates the required GUI and non GUI objects.

        """
        BOTTOMPANEL_ID = 4002
        SIDEPANEL_ID = 3999

        try:
            self.presLang = gettext.translation("gEcrit", "./locale")
            self._ = self.presLang.ugettext
            self.presLang.install()
        except:
            print("Translation for local language not found.")
            self._ = self.dummy_tr

        pathname = os.path.abspath(os.path.dirname((sys.argv)[0]))  #  Finding where
        os.chdir(pathname)  #  gEcrit is running

        #Setting up the plugin envirenment

        self.general_plugins = {}
        self.passive_plugins = {}
        self.plugin_manager = PluginManager(
            categories_filter={"General": General,
                               "Passives" : Passive})

        #Sets YAPSY the plugin directory.

        self.plugin_path = os.path.join(pathname, "data", "plugins")
        self.plugin_manager.setPluginPlaces([self.plugin_path])

        self.plugin_manager.locatePlugins()
        #self.plugin_manager.collectPlugins()

        self.plugin_manager.loadPlugins()

        self.activated_plugins = Config.GetOption("ActivePlugins")

        #populating the general plugin index
        for f in self.plugin_manager.getPluginsOfCategory("General"):
            if f.plugin_object.name in self.activated_plugins:
                self.general_plugins[f.plugin_object.name] = f.plugin_object

        #the passive plugins now
        for p in self.plugin_manager.getPluginsOfCategory("Passives"):
            if p.plugin_object.name in self.activated_plugins:
                self.passive_plugins[p.plugin_object.name] = p.plugin_object

        self.id_range = []

        #getting the command line file argument
        if "gEcrit.py" not in (sys.argv)[-1]:
            target_file = os.path.normpath(os.path.realpath(sys.argv[-1]))

        #no file was provided
        else:
            target_file = None

        wx.Frame.__init__(self, parent, 1000, 'gEcrit', size=(700, 600))
        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        #this object will handle layout and docking/undocking of widgets
        self.aui_manager = wx.aui.AuiManager(self)

        #creating the status bar
        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetStatusText("Done")
        self.status_bar.SetFieldsCount(3)
        self.status_bar.SetId(999)
        if not Config.GetOption("StatusBar"):
            self.status_bar.Hide()

        self.menubar = MainMenu(self)
        self.SetMenuBar(self.menubar)

        #setting the application icon
        self.SetIcon(wx.Icon('icons/gEcrit.png', wx.BITMAP_TYPE_PNG))

        #this variable is incremented each time we create a StcControl
        self.text_id = 0

        #finding the user home folder
        self.HOMEDIR = os.path.expanduser('~')
        os.chdir(os.path.abspath(self.HOMEDIR))

        #creating a plugin manager instance
        self.plugin_conf_manager = gEcritPluginManager(self)

        #creating the left side notebook
        self.side_notebook = wx.aui.AuiNotebook(self, id=SIDEPANEL_ID, size=(-1,-1),
                                                style=wx.BORDER_SUNKEN|wx.aui.AUI_NB_TAB_SPLIT|wx.aui.AUI_NB_TAB_MOVE|wx.aui.AUI_NB_SCROLL_BUTTONS )

        #creating the bottom side notebook
        self.bottom_notebook = wx.aui.AuiNotebook(self, id=BOTTOMPANEL_ID, size=(-1,
                                                                               -1), style=wx.BORDER_SUNKEN|wx.aui.AUI_NB_TAB_SPLIT|wx.aui.AUI_NB_TAB_MOVE|wx.aui.AUI_NB_SCROLL_BUTTONS )

        #the aui notebook that will manage editor tabs
        self.nb = AuiNoteBook(parent = self)

        #going back to application running point
        os.chdir(pathname)

        #binding the menubar events
        f = wx.FindWindowById
        self.Bind(wx.EVT_MENU, lambda event: self.NewTab(event,
                                                         "New Document", "New Document"), id=500)
        self.Bind(wx.EVT_MENU, lambda event: self.OnOpenFile(event), id=
                  501)
        self.Bind(wx.EVT_MENU, lambda event: f((self.id_range)[self.nb.GetSelection()]).Save(event),
                  id=502)
        self.Bind(wx.EVT_MENU, lambda event: f((self.id_range)[self.nb.GetSelection()]).SaveAs(event),
                  id=503)
        self.Bind(wx.EVT_MENU,  self.OnPrint,id=504)
        self.Bind(wx.EVT_MENU, lambda event: self.OnMenuCloseTab(event,
                                                                 (self.id_range)[self.nb.GetSelection()]), id=505)
        self.Bind(wx.EVT_MENU, lambda event: self.OnQuit(event), id=506)
        self.Bind(wx.EVT_MENU, self.SaveAll, id=563)
        self.Bind(wx.EVT_MENU, lambda event: f((self.id_range)[self.nb.GetSelection()]).OnReload(event),id = 507)

        self.Bind(wx.EVT_MENU, lambda event: f((self.id_range)[self.nb.GetSelection()]).OnUndo(event),
                  id=520)
        self.Bind(wx.EVT_MENU, lambda event: f((self.id_range)[self.nb.GetSelection()]).OnRedo(event),
                  id=521)
        self.Bind(wx.EVT_MENU, lambda event: f((self.id_range)[self.nb.GetSelection()]).OnCut(event),
                  id=522)
        self.Bind(wx.EVT_MENU, lambda event: f((self.id_range)[self.nb.GetSelection()]).OnCopy(event),
                  id=523)
        self.Bind(wx.EVT_MENU, lambda event: f((self.id_range)[self.nb.GetSelection()]).OnPaste(event),
                  id=524)
        self.Bind(wx.EVT_MENU, lambda event: f((self.id_range)[self.nb.GetSelection()]).OnSelectAll(event),
                  id=525)
        self.Bind(wx.EVT_MENU, lambda event: f((self.id_range)[self.nb.GetSelection()]).OnSelectCodeBlock(event),
                  id=562)
        self.Bind(wx.EVT_MENU, lambda event: f((self.id_range)[self.nb.GetSelection()]).OnInsertDate(event),
                  id=526)
        self.Bind(wx.EVT_MENU, lambda event: self.OnPrefs(event), id=527)
        self.Bind(wx.EVT_MENU, lambda event: f((self.id_range)[self.nb.GetSelection()]).OnDedent(event),
                  id=528)
        self.Bind(wx.EVT_MENU, lambda event: f((self.id_range)[self.nb.GetSelection()]).OnIndent(event),
                  id=529)
        self.Bind(wx.EVT_MENU, lambda event:f((self.id_range)[self.nb.GetSelection()]).OnComment(event),
                  id=559)
        self.Bind(wx.EVT_MENU, lambda event:f((self.id_range)[self.nb.GetSelection()]).OnUnComment(event),
                  id=560)
        self.Bind(wx.EVT_MENU, lambda event: FindRepl.FindDocText(event, (self.id_range)[self.nb.GetSelection()]),
                  id=530)
        self.Bind(wx.EVT_MENU, lambda event: FindRepl.ReplaceDocText(event, (self.id_range)[self.nb.GetSelection()]),
                  id=531)
        self.Bind(wx.EVT_MENU, lambda event: FindRepl.FindDocText(event, (self.id_range)[self.nb.GetSelection()],wx.stc.STC_FIND_REGEXP),
                  id=532)
        self.Bind(wx.EVT_MENU, lambda event: FindRepl.ReplaceDocText(event ,(self.id_range)[self.nb.GetSelection()], wx.stc.STC_FIND_REGEXP),
                  id=533)
        self.Bind(wx.EVT_MENU, lambda event: f((self.id_range)[self.nb.GetSelection()]).OnStartRecordMacro(event), id=534)
        self.Bind(wx.EVT_MENU, lambda event: f((self.id_range)[self.nb.GetSelection()]).OnStopRecordMacro(event), id=542)
        self.Bind(wx.EVT_MENU, lambda event: f((self.id_range)[self.nb.GetSelection()]).OnMacroPlayback(event), id=543)

        self.Bind(wx.EVT_MENU, lambda event: f((self.id_range)[self.nb.GetSelection()]).OnZoomIn(event),
                  id=535)
        self.Bind(wx.EVT_MENU, lambda event: f((self.id_range)[self.nb.GetSelection()]).OnZoomOut(event),
                  id=536)
        self.Bind(wx.EVT_MENU, lambda event: f((self.id_range)[self.nb.GetSelection()]).OnResetZoom(event),
                  id=537)

        self.Bind(wx.EVT_MENU, lambda event: Config.ChangeOption("LineNumbers",
                                                                 self.menubar.IsChecked(538), self.id_range), id=538)
        self.Bind(wx.EVT_MENU, lambda event: Config.ChangeOption("FoldMarks",
                                                                 self.menubar.IsChecked(539), self.id_range), id=539)
        self.Bind(wx.EVT_MENU, lambda event: Config.ChangeOption("Whitespace",
                                                                 self.menubar.IsChecked(540), self.id_range), id=540)
        self.Bind(wx.EVT_MENU, lambda event: Config.ChangeOption("IndetationGuides",
                                                                 self.menubar.IsChecked(541), self.id_range), id=541)
        self.Bind(wx.EVT_MENU, lambda event: Config.ChangeOption("EdgeLine",
                                                                 self.menubar.IsChecked(546), self.id_range), id=546)
        self.Bind(wx.EVT_MENU, lambda event: Config.ChangeOption("SyntaxHighlight",
                                                                 self.menubar.IsChecked(547), self.id_range), id=547)

        self.Bind(wx.EVT_MENU, lambda event: Config.ChangeOption("StatusBar",
                                                                 self.menubar.IsChecked(545), self.id_range), id=545)
        self.Bind(wx.EVT_MENU, self.OnFullScreen, id=557)

        self.Bind(wx.EVT_MENU, self.ToggleSidePanel, id = 548)
        self.Bind(wx.EVT_MENU, self.ToggleBottomPanel, id = 549)

        self.Bind(wx.EVT_MENU, lambda event: f((self.id_range)[self.nb.GetSelection()]).OnRemoveTrails(event),id=551)
        self.Bind(wx.EVT_MENU, lambda event: self.OnRun(event,self.id_range[self.nb.GetSelection()]), id = 558)
        self.Bind(wx.EVT_MENU, lambda event: f((self.id_range)[self.nb.GetSelection()]).Tabify(event), id = 552 )
        self.Bind(wx.EVT_MENU, lambda event: f((self.id_range)[self.nb.GetSelection()]).UnTabify(event), id = 553 )

        self.Bind(wx.EVT_MENU, self.SaveSessionFile , id = 554)
        self.Bind(wx.EVT_MENU, gEcritSession.DeleteSessionFile , id = 555)
        self.Bind(wx.EVT_MENU, lambda event: Config.ChangeOption("Session",self.menubar.IsChecked(556)) , id = 556)

        self.Bind(wx.EVT_MENU, self.plugin_conf_manager.ShowMe, id = 564 )
        self.Bind(wx.EVT_MENU, lambda event: self.OnAbout(event), id=550)

        #setting up the toolbar
        self.toolbar = MainToolbar(self, -1)

        self.FontCtrl = wx.FontPickerCtrl(self.toolbar, 607, size=(100,
                                                                   30))
        self.Bind(wx.EVT_FONTPICKER_CHANGED, lambda event: ChangeFont(event,
                                                                      self.FontCtrl.GetSelectedFont(), self.id_range))
        #the goto line text box
        self.toolbar.AddControl(self.FontCtrl)
        self.toolbar.AddControl(wx.TextCtrl(self.toolbar, 608, size=(-1,
                                                                      -1), style=wx.TE_PROCESS_ENTER))

        #Binding toolbar events
        self.Bind(wx.EVT_TOOL, lambda event: self.NewTab(event,
                                                         "New Document", "New Document"), id=600)
        self.Bind(wx.EVT_TOOL, self.OnOpenFile, id=601)
        self.Bind(wx.EVT_TOOL, lambda event: f((self.id_range)[self.nb.GetSelection()]).Save(event),
                  id=602)
        self.Bind(wx.EVT_TOOL, lambda event: f((self.id_range)[self.nb.GetSelection()]).SaveAs(event),
                  id=603)
        self.Bind(wx.EVT_TOOL, self.OnPrefs, id=604)
        self.Bind(wx.EVT_TOOL, self.OnQuit, id=605)

        self.Bind(wx.EVT_TEXT_ENTER, lambda event: self.OnGotoBox(event,
                                                                  (self.id_range)[self.nb.GetSelection()]), id=608)

        self.Bind(wx.EVT_TOOL,  self.OnPrint, id=609)
        self.Bind(wx.EVT_TOOL, lambda event: self.OnRun(event, (self.id_range)[self.nb.GetSelection()]),
                  id=610)

        #Give the plugins a chance to set themselves in the system
        #generals first

        for g in self.general_plugins:
            self.general_plugins[g].Init(self)

        #passives now
        for p in self.passive_plugins:
            self.passive_plugins[p].Init(self)

		#put it in the middle of the sceen
        self.Centre()

        #the preferences window
        self.conf_win = ConfFrame = CfgFrame(self)

        #addung the pane to the aui manager.
        self.aui_manager.AddPane(self.toolbar, wx.aui.AuiPaneInfo().Name("toolbar").Caption(self._("Toolbar")).ToolbarPane().Top().CloseButton(False))
        self.aui_manager.AddPane(self.nb, wx.aui.AuiPaneInfo().Name("editor tabs").Caption(self._("Tabs")).CenterPane())
        self.aui_manager.AddPane(self.bottom_notebook, wx.aui.AuiPaneInfo().Name("bottom panel").Caption(self._("Assistants and others")).Bottom().BestSize((700,150)).PinButton(True).MaximizeButton(True))
        self.aui_manager.AddPane(self.side_notebook, wx.aui.AuiPaneInfo().Name("left_side panel").Caption(self._("Toolbox")).Left().BestSize((150,400)).PinButton(True).MaximizeButton(True))

        #loading saved session if any exists and if enabled
        if Config.GetOption("Session"):
            self.LoadSessionFile()

        #make changes visible
        self.aui_manager.Update()

        if target_file: #load command line file path argument
            self.NewTab(0, os.path.split(target_file)[-1], target_file)

    def LoadSessionFile(self):
        """
        LoadSessionFile

        Loads the session file if it exists.
        If it does not, creates an instance.
        """
        try:
            self.session =  gEcritSession.LoadFromFile()
            self.session.RestoreAppState(self)
            self.SetStatus(0,self._ ( "Session file loaded."))
        except Exceptions.NoSessionFile:
            self.session = gEcritSession()

    def SaveSessionFile(self, event):
        """
        SaveSessionFile

        Reccords the application state and saves it to disk via the
        session instance.
        """
        try: #testing if a session object exists
            self.session
        except AttributeError:
            self.session = gEcritSession()

        self.session.RecordAppState(self)
        self.session.SaveToFile()
        self.SetStatus(event, self._ ("Session saved."))

    def OnFullScreen(self,event):
        """
        OnFullScreen

        Makes the main window fullscreen.
        """
        self.ShowFullScreen(not self.IsFullScreen(),wx.FULLSCREEN_NOCAPTION)

    def OnPrefs(self, event):
        """
        OnPrefs

        Shows the preferences window.
        """
        self.conf_win.ShowMe(0)

    def NewTab(self, event, nb, file_path):
        """
        NewTab

        Creates a new AUI NOTEBOOK tab, adds the contents,
        initializez a STC object for it and binds some of its events.
        Creates the sidebar, adds a notebook and adds its utilities
        in its tabs.
        """
        if not file_path:
            return

        #update recent file list
        if file_path != "New Document" and file_path != "":
            if not os.path.exists(file_path):
                wx.MessageDialog(None, self._ ("Could not load file.\nThe file ")+file_path+self._ (" does not exists."),self._ ("Input Error") ,wx.OK).ShowModal()
                return
            lst = Config.GetOption("RecentFiles")
            lst.append(file_path)
            Config.ChangeOption("RecentFiles",lst)
            self.menubar.UpdateRecentFiles()

        #the parent of the StcControl
        panel = wx.Panel(self)
        panel.identifierTag = nb

       	#hiding self.text_id
        text_id = self.text_id

        #set up the editor
        text_ctrl = StcTextCtrl(panel, self.text_id, file_path)

	#the StcControl sizer
        text_ctrl_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text_ctrl_sizer.Add(text_ctrl, 1, wx.EXPAND)
        panel.SetSizer(text_ctrl_sizer)
        panel.Fit()

	#append the id of this StcControl to the id_range
        self.id_range.append(text_id)

        text_ctrl.SetBufferedDraw(True)
        #apply the font
        text_ctrl.StyleSetFont(0, self.FontCtrl.GetSelectedFont())

        #add the panel as a new tab
        self.nb.AddPage(panel, str(nb), select=True)
        if file_path == "New Document" or file_path == "":
            #notify plugins
            for g in self.general_plugins:
                self.general_plugins[g].NotifyNewTabOpened()

        self.text_id += 1
        return text_ctrl

    def OnRun(self, event, text_id):
        """
        Runs the current document in a xterm window, for testing.
        """
        cur_doc = wx.FindWindowById(text_id)
        cur_doc.Save(0)
        os.system("xterm -e sh runner.sh "+cur_doc.GetFilePath())

    def OnGotoBox(self, event, text_id):
        """
        OnGotoBox

        Finds the current document, and scrolls to the line indicated
        by its input upon the Return key.
        """
        cur_doc = wx.FindWindowById(text_id)
        goto = wx.FindWindowById(608)
        scroll_pos = int(goto.GetLineText(0))
        cur_doc.ScrollToLine(scroll_pos - 1)

    def OnPrint(self, event):
        """
        OnPrint

        Finds the document, sets the prints name, and calls the
        wxPython toolkit to print the contents
        """
        print_dlg = PrettyPrinter(self)
        del print_dlg

    def OnAbout(self, event):
        """
        OnAbout

        Shows the about window.
        """
        #ShowAbout = AboutWindow
        about_win = AboutWindow()
        del about_win

    def OnQuit(self, event):
        """
        OnQuit

        Closes the main window, stops the terminals, and kills the
        application process.
        It promps the user for confirmation.
        """
        #warn the user
        warn_dlg = wx.MessageDialog(None,
                    self._ ("Please make sure that your data is\
 saved.\nAre you sure you want to quit?"),
                      self._ ("Are you sure?"), style=wx.YES_NO)
        warn_dlg_val = warn_dlg.ShowModal()
        if warn_dlg_val != 5104: #YES
            #call the quit method to stop the terminals and the plugins
            self.Quit()

    def Quit(self):
        #stop ond notify all plugins of application shutdown.
        #generals now
        for g in self.general_plugins:
            self.general_plugins[g].Stop()

        for p in self.passive_plugins:
            self.passive_plugins[p].Stop()

        #stop the shells if activated

        if Config.GetOption("Session"):
            self.SaveSessionFile(0)

        #exit status 0, all ok
        sys.exit(0)

    def OnMenuCloseTab(self, event, text_id):
        self.ManageCloseTab(False, text_id)

    def ManageCloseTab(self, event, text_id):
        """
        ManageCloseTab

        Manages the process of closing a tab.
        Checks if document is saved, prompts the user if not.
        If this is the last tab in the application, it closes the
        terminals, the window and kills the application.
        If not, it decreases the number of tabs and delted the AUI
        NETBOOK page.
        """
        cur_doc = wx.FindWindowById(text_id)
        current_text = cur_doc.GetText()
        #check if the user saved the changes
        if cur_doc.save_record != current_text:
			#if not, notify him
            save_prompt = wx.MessageDialog(None, self._ ("The file ") + os.path.split(cur_doc.GetFilePath())[-1] +
                    self._ (" is not saved.\n\
Do you wish to save it?"), "",
                    style=wx.CANCEL | wx.YES | wx.NO)
            prompt_val_ = save_prompt.ShowModal()

            if prompt_val_ == 5103:     #YES
                if not cur_doc.Save(0):
                    event.Veto()
                    return
                else:
                    self.id_range.remove(text_id)

            elif prompt_val_ == 5101:   #CANCEL
                event.Veto()
                return
            elif prompt_val_ == 5104:   #NO
                self.id_range.remove(text_id)

            save_prompt.Destroy()
        else:
                self.id_range.remove(text_id)
                # skip the event and let the AuiNotebook handle the deletion
                cur_doc.Deactivate() # tell the StcTextCtrl to prepare for deletition
                if not event:        # check if it was fired from menu
                    self.nb.DeletePage(self.nb.GetSelection())
                else:
                    event.Skip()

    def OnOpenFile(self, event):
        """
        OnOpenFile

        Collects a path for a new file via a file dialog.
        """
        open_file_dlg = wx.FileDialog(None, style=wx.OPEN | wx.FD_MULTIPLE)
        if self.menubar.last_recent != "":
		#go to the last accessed folder
            open_file_dlg.SetDirectory(os.path.split(self.menubar.last_recent)[0])
        else:
            open_file_dlg.SetDirectory(self.HOMEDIR)

        if open_file_dlg.ShowModal() == wx.ID_OK:
            paths = open_file_dlg.GetPaths()
            self.OpenFile(paths)

        del open_file_dlg

    def OpenFile(self, paths):
        """
        OpenFile

        Calls NewTab with the collected path.
        Supports multiple path selection.
        """
        # if paths is a list, open an StcContrel for each of them
        if isinstance(paths, types.ListType):
            for f in paths:
                self.NewTab(0, os.path.split(f)[-1], f)
                Log.AddLogEntry(self._ ("Opened file ") + f)
        #if a string, open an StcControl for it
        else:
            self.NewTab(0, os.path.split(paths)[-1], paths)
            Log.AddLogEntry(self._ ("Opened file ") + paths)

        #notify general  plugins
        for t in self.general_plugins:
            try: #insulate from possible plugin errors
                self.general_plugins[t].NotifyDocumentOpened()
            except: pass
        AutoComp.UpdateCTagsFiles(self.id_range)

    def SetStatus(self, event, text):
        """
        ResetStatus

        Sets the status of statusbar.
        """
        self.status_bar.SetStatusText(text)
       # event.Skip()

    def ResetStatus(self, event):
        """
        ResetStatus

        Sets the status bar status to nothing.
        """
        self.status_bar.SetStatusText("")
        event.Skip()

    def SaveAll(self, event):
        """
        SaveAll

        Saves all the current documents using the
        objects Save function.

        """
        for id in self.id_range:
            cur_doc = wx.FindWindowById(id)
            if cur_doc.GetFilePath() != "" and cur_doc.GetFilePath() != \
                "New Document":
                cur_doc.Save(0)


    ####################################################################
    #                        PLUGIN INTERFACE                          #
    ####################################################################

    def ToggleSidePanel(self, event):
        pane = self.aui_manager.GetPane(self.side_notebook)
        if pane.IsShown(): pane.Hide()
        else: pane.Show()
        self.aui_manager.Update()

    def ToggleBottomPanel(self, event):
        pane = self.aui_manager.GetPane(self.bottom_notebook)
        if pane.IsShown(): pane.Hide()
        else: pane.Show()
        self.aui_manager.Update()

    def GetCurrentDocument(self):
        """
        GetCurrentDocument

        Returns the selected active buffer object.
        """

        return wx.FindWindowById(self.id_range[self.nb.GetSelection()])

    def GetAllDocuments(self):
        """
        GetALlDocuments

        Returns all existing buffers.
        """
        docs = []
        for d in self.id_range:
            docs.append(wx.FindWindowById((d)))
        return docs

    def AddToMenuBar(self,label,menu):
        """
        AddToMenuBar

        @id The id of the new menu entry.
        @label The label of the new menu entry.
        @menu A wx.Menu object which will be added in the Plugins menu.

        Adds a wx.Menu object to menubar.
        """
        return self.menubar.plugins.AppendMenu(-1,label,menu)

    def RemoveFromMenubar(self, menu):
        """
        RemoveFromMenubar

        Removes the supplied argument menu from the plugins submenu.
        """
        self.menubar.plugins.RemoveItem(menu)

    def BindMenubarEvent(self, item, function):
        """
        BindMenuBarEvent

        @item The menu entry object which to be bint.

        @function The function the item to be bint to.

        Binds a wx.EVT_MENU event to the suplied function.

        """
        self.Bind(wx.EVT_MENU, function, id = item.GetId())

    def GetBottomPanel(self):
        """
        GetBottomPanel

        Returns the lower notebook.
        """
        return self.bottom_notebook

    def AddToBottomPanel(self, panel, name):
        """
        AddToBottomPanel

        Adds the suplied panel to the lower notebook with tho supplied
        name label.
        """
        self.bottom_notebook.AddPage(panel, name)

    def GetSidePanel(self):
        """
        GetSidePanel

        Returns the side notebook.
        """
        return self.side_notebook

    def AddToSidePanel(self, panel, name):
        """
        AddToSidePanel

        Adds the suplied panel to the side notebook with tho supplied
        name label.
        """
        self.side_notebook.AddPage(panel, name)

    def DeleteBottomPage(self, name):
        """
        DeleteBottomPage

        Deletes the tab named name from the lower notebook.
        """
        self.bottom_notebook.DeletePage(Config.GetTab(name,
                                                  self.bottom_notebook))


    def DeleteSidePage(self, name):
        """
        DeleteSidePage

        Deletes the tab named name from the side notebook.
        """
        self.side_notebook.DeletePage(Config.GetTab(name,
                                                    self.side_notebook))

    def AddPaneToAui(self, widget ,pane_info):
        """
        "AddPaneToAui
        @widget the widget to be added
        @pane needs to be an AuiPaneInfo object.

        Adds the pane to the aui manager.
        """
        self.aui_manager.AddPane(widget, pane_info)

    def AddToolbarToAui(self, toolbar, pane_info):
        """
        AddToosbartoAui

        @toolbar the wx.Toolbar object
        @pane_info needs to be a wx.AuiPaneInfo object with it's name and caption
        defined.
        """
        self.aui_manager.AddPane(toolbar, pane_info.ToolbarPane().Top().CloseButton(False))


    def GetAuiManager(self):
        """
        GetAuiManager

        Returns the AuiManager that is responsable for window layout.
        """
        return self.aui_manager


    def GetTabManager(self):
        """
        GetTabManager

        Returns the AuiNoteBook that is resposible for tabs management.
        """
        return self.nb

    def CreateNewDocument(self, name):
        """
        CreateNewDocument

        @name a string to be given to the new document as a name.

        Creates a new empty document.
        Returns a reference to the now StcControl
        """
        return self.NewTab(0, name, "")


def main():
    app = wx.PySimpleApp()
    frame = gEcrit(parent=None, id=-1)
    frame.Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
