#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx, gettext
import os.path
from configClass import *




class MainMenu(wx.MenuBar):
    """
    MainMenu

    Creates the application menubar.
    Provides a few helper functios.

    """
    def __init__(self, parent, id=wx.ID_ANY):
        """
        __init__

        Build the application menu. Adds the entryes, creates recent
        file list.

        """
        #creating application menu
        self.parent = parent
        self._ = self.parent._
        menubar = wx.MenuBar()
        self.recent_dict = {}
        wx.MenuBar.__init__(self)
        file = wx.Menu()
        self.recent_files = wx.Menu()
        edit = wx.Menu()
        help = wx.Menu()
        search = wx.Menu()
        view = wx.Menu()
        document = wx.Menu()
        session = wx.Menu()
        self.plugins = wx.Menu()

        if Config.GetOption("RecentFiles"):  # check if list is empty
            self.last_recent = Config.GetOption("RecentFiles")[-1]
        else:
            self.last_recent = ""

        file.Append(500, self._('&New Tab\tCtrl+N'), self._('Open a new tab.'))
        file.Append(501, self._('&Open\tCtrl+O'),self._('Open a new document.'))
        file.Append(502, self._('&Save\tCtrl+S'),self._('Save the document.'))
        file.Append(503, self._('Save As'),
           self._('Save the document under a different name.'))
        file.Append(563, self._("Save All"),
                self._("Saves all the open documents that have a path."))
        file.Append(507,self._("Reload\tCtrl+R"),self._("Reload the current file from disk."))
        file.Append(504, self._('&Print\tCtrl+P'), self._('Print the current document.'))
        file.Append(505, self._('Close &Tab\tCtrl+W'), self._('Close the current tab.'))



        self.recent_submenu = wx.Menu()

        self.GenerateRecentFiles()

        file.AppendMenu(700, self._("Recent files\tShow the last opened files."),self.recent_submenu)
        file.AppendSeparator()
        quit = wx.MenuItem(file, 506, self._('&Quit\tCtrl+Q'), self._('Quit gEcrit.'))
        file.AppendItem(quit)


        edit.Append(520, self._("&Undo\tCtrl+Z"), self._("Cancel the last action."))
        edit.Append(521, self._("&Redo\tCtrl+Y"), self._("Bring back the last action."))
        edit.AppendSeparator()
        edit.Append(522, self._("&Cut\tCtrl+X"), self._("Cut the selection."))
        edit.Append(523, self._("C&opy\tCtrl+C"), self._("Copy the selection."))
        edit.Append(524, self._("P&aste\tCtrl+V"), self._("Paste the selection."))
        edit.AppendSeparator()
        edit.Append(525, self._("Select All\tCtrl+A"),
                    self._("Select all the document."))
        edit.Append(562, self._("Select Code Block\tCtrl+Shift+A"),
                  self._("Select all the current code block."))
        edit.AppendSeparator()
        edit.Append(529, self._("Indent\tCtrl+K"), self._("Indent the selected lines."))
        edit.Append(528, self._("Dedent\tCtrl+J"), self._("Dedent the selected lines."))

        edit.Append(559, self._("Comment Lines\tCtrl+Shift+C"), self._("Comment the selected lines."))
        edit.Append(560, self._("Uncomment Lines\tCtrl+Shift+X"), self._("Uncomment the selected lines."))

        edit.AppendSeparator()
        edit.Append(526, self._("Insert date"),
                   self._("Insert the date at cursor position."))
        edit.AppendSeparator()
        edit.Append(527, self._("Preferences\tCtrl+E"),
                    self._("Open the configuration window."))

        search.Append(530, self._("Find\tCtrl+F"),
                 self._("Search text in the current document."))
        search.Append(531, self._("Find and Replace\tCtrl+H"),
      self._("Search and replace text in the current document."))

        search.Append(532, self._("Regex Search\tCtrl+Shift+F"),self._("Find text using a regular expression."))
        search.Append(533, self._("Regex Search and Replace\tCtrl+Shift+H"), self._("Find and replace text using a regular expression."))

        view.Append(535, self._("Zoom In\tCtrl++"),
            self._("Increase the size of the text."))
        view.Append(536, self._("Zoom Out\tCtrl+-"),
            self._("Decrease the size of the text."))
        view.Append(537, self._("Normal Size\tCtrl+0"),
            self._("Set the size of the text to normal."))
        view.AppendSeparator()
        view.AppendCheckItem(538, self._("Line Numbers"),
            self._("Show/Hide line numbers.")).Check(Config.GetOption("LineNumbers"))
        view.AppendCheckItem(539, self._("Fold Marks"), self._("Show/Hide fold marks.")).Check(Config.GetOption("FoldMarks"))
        view.AppendCheckItem(540, self._("White Space"),
            self._("Show/Hide white spaces.")).Check(Config.GetOption("Whitespace"))
        view.AppendCheckItem(541, self._("Indentation Guides"),
                             self._("Show/Hide indentation guides.")).Check(Config.GetOption("IndetationGuides"))
        view.AppendCheckItem(546, self._("Edge Line"),
            self._("Show/Hide the edge line.")).Check(Config.GetOption("EdgeLine"))
        view.AppendCheckItem(547, self._("Syntax Highlight"),
            self._("Enable/Disable Syntax Highlight.")).Check(Config.GetOption("SyntaxHighlight"))
        view.AppendSeparator()

        view.AppendCheckItem(545, self._("Statusbar"), self._("Show/Hide statusbar.")).Check(Config.GetOption("StatusBar"))
        view.AppendCheckItem(557, self._("Fullscreen\tF11"), self._("Toggle Fullscreen mode."))
        view.Append(548, self._("Toggle Toolbox"), self._("Show/Hide Toolbox window."))
        view.Append(549, self._("Toggle Assistants"), self._("Show/Hide Assistants window."))

        document.Append(551, self._("Remove Trailing  Spaces"), self._("Remove spaces at the end of the line."))
        document.Append(558, self._("Run File\tF5"), self._("Run the current document.(python only)"))
        document.Append(552, self._("Tabify"), self._("Replace spaces by tabs."))
        document.Append(553, self._("Untabify"), self._("Replace tabs by spaces."))

        session.AppendCheckItem(556, self._("Enable Session"), self._("Enable/Disable Session support.")).Check(Config.GetOption("Session"))
        session.Append(554, self._("Save Session"), self._("Save the current application state.")) 
        session.Append(555, self._("Delete Session"), self._("Delete the saved session file."))

        self.plugins.Append(564, self._("Plugin Manager"), self._("Manage gEcrit Plugins."))

        help.Append(550, self._("About"), self._("Open the about window."))

        self.Append(file, self._('&File'))
        self.Append(edit, self._('&Edit'))
        self.Append(search, self._("&Search"))
        self.Append(view, self._("&View"))
        self.Append(document, self._("&Document"))
        self.Append(session, self._("&Session"))
        self.Append(self.plugins, self._("&Plugins"))
        self.Append(help, self._('&Help'))


    def NewTabHelper(self,event):
        """
        NewTabHelper

        Used to help for calling the NewTab function of this object
        parent.
        """
        self.parent.NewTab(0,os.path.split(self.recent_dict[event.GetId()])[-1],
        self.recent_dict[event.GetId()])
        self.last_recent = self.recent_dict[event.GetId()]

    def ClearRecentFiles(self):
        """
        ClearRecentFiles

        Deletes all the entryes under the Recent Files submenu.
        """
        #deleting items from menu
        items = self.recent_submenu.GetMenuItems()
        for i in items:
            self.recent_submenu.DeleteItem(i)

    def GenerateRecentFiles(self):
        """
        GenerateRecentFiles

        Takes the recent files list from config and generates
        a Recent Files submenu with them.
        Binds the events to them with NewTabHelper.
        """
        #generating new items
        st_id = 701
        last_nm = ""
        #cleaning it first (must have less than 10 elements)
        lst = Config.GetOption("RecentFiles")
        if len(lst) >10:
            while len(lst) > 10:
                lst.remove(lst[0])
            Config.ChangeOption("RecentFiles",lst)

        lst = Config.GetOption("RecentFiles") # refreshing list
        # creating recent file menu list

        for i in lst:
            if last_nm != i:
                self.recent_submenu.Append(st_id,i)
                st_id+=1
                last_nm = i

        #binding events
        st_id = 701
        items = self.recent_submenu.GetMenuItems()
        for item in items:
            self.parent.Bind(wx.EVT_MENU, self.NewTabHelper,id=item.GetId())
            self.recent_dict[item.GetId()] = item.GetLabel()


    def UpdateRecentFiles(self):
        """
        UpdateRecentFiles

        Calls the 2 function that are involved in creating a new
        Recent Files submenu.
        """
        self.ClearRecentFiles()
        self.GenerateRecentFiles()
