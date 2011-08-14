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
import yapsy.IPlugin
from data.plugins.categories import General

class HierarchyCtrl(wx.TreeCtrl):
    """
    HierarchyCtrl

    Manages data colection, processing and displaying of python
    classes from a source of files.
    Creates hierarchies of them in tree.
    """

    class Class():
        def __init__(self, name = "", bases = []):
            self.name = name
            self.bases = bases
            self.children = []
            self.tree_ctrl_root = None

    def __init__(self,parent = None, id = wx.ID_ANY, pos = (10,10), size=(-1,-1)):
        """
        __inti__

        Initializes the wx.TreeCtrl object, creates a tree root
        and the environment.
        """

        wx.TreeCtrl.__init__(self, parent, id,pos,size,style =
                                   wx.TR_HIDE_ROOT | wx.TR_HAS_BUTTONS |
                                   wx.TR_HAS_VARIABLE_ROW_HEIGHT)

        self.root = self.AddRoot("Top")
        self.classes = []

    def GenerateHierarchies(self,docs):
        """
        GenerateHierarchies

        Gathers data using helper functions and organizes it
        on the tree.
        First clears the tree with the help of the helper function
        and then populates it.
        """
        file_list = self.GetFileList(docs)
        for fl in file_list:
             self.GetClassesFromFile(fl)

        # base attributes are nothing but strings now. replace them with real Class objects
        for cl in self.classes:
            bases = []
            for c in self.classes:
                if c.name in cl.bases:
                    bases.append(c)
            cl.bases = bases


        # get list of children
        to_be_removed = []
        for cl in self.classes:
            for c in self.classes:
                if cl in c.bases:
                    cl.children.append(c)
                    to_be_removed.append(c)


        self.classes = [ c for c in self.classes if not c in to_be_removed ]

        def WalkAndAddTree(node,root):
            node.tree_ctrl_root = self.AppendItem(root, node.name)

            for child in node.children:
                child.tree_ctrl_root = self.AppendItem(node.tree_ctrl_root, child.name)
                if child.children:
                    WalkAndAddTree(child, child.tree_ctrl_root)

        for cls in self.classes:
            cls.tree_ctrl_root = self.AppendItem(self.root, cls.name)
            for child in cls.children:
                WalkAndAddTree(child,cls.tree_ctrl_root)

        # filter out child classes
        # tree_roots = list(set([ cls for cls in self.clasess if not cls.bases]))
        self.classes = []

    def FindChilds(self,cls):
        """
        FindChilds

        Finds the child classes of the suplied argument cls.
        Uses a helper class to check inheritance.
        Return the list of childs.
        """
        childs = []
        for c in self.classes:
            if cls.name in c.bases:
                childs.append(c)
        return childs

    def GetClassesFromFile(self,file_path):
        """
        GetClassesFromFile

        Reads and collects the class statements from the suplied
        file_path argument.
        Creates a list of found classes and returns it if not empty.
        """

        with  open(file_path,"r") as fl:
            for line in fl:
                if "class" in line and ":" in line:
                    name = line.lstrip("class").split("(")[0].rstrip(":").strip() # extract class name
                    bases = line.split("(")[1].split(")")[0].split(",") # extract bases
                    bases = [ b.strip() for b in bases] # remove whitespace
                    self.classes.append(HierarchyCtrl.Class(name,bases))


    def GetFileList(self,docs):
        """
        GetFileList

        Iterates through all the editor objects, retrieves their
        file paths, gathers them into a list and returns it.
        If none Found, return False.
        """
        file_list = []
        for d in docs:
            file_name = d.GetFilePath()
            if file_name != "":
                file_list.append(file_name)

        return file_list


    def Refresh(self,docs):
        """
        Refresh

        Rebuild the class hierarchy tree.
        """
        self.DeleteChildren(self.root)
        self.GenerateHierarchies(docs)

class ClassHierarchyWin(wx.Frame, General,yapsy.IPlugin.IPlugin):
    """
    HierarchyFrame

    Provides a display space and controls for the
    ClassHierarchyCtrl object.
    """
    def __init__(self):
        self.name = "Class Hierarchy Tree"


    def Init(self,parent = None,id = wx.ID_ANY):
        """
        Init

        Build the frame GUI components and initializes the wx.Frame
        object.
        Initializes the ClassHierarchyCtrl object.
        """

        self.parent = parent
        wx.Frame.__init__(self, parent,id,"Class Hierarchies",size=(300,500))
        self.panel = wx.Panel(self)
        panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.tree_ctrl = HierarchyCtrl(self.panel)
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.refresh = wx.Button(self.panel,-1,"Refresh", pos=(200,400),
                                                         size=(-1,-1))

        self.close = wx.Button(self.panel,-1, "Close", pos = (250,400),
                                                       size=(-1,-1))
        self.button_sizer.Add(self.refresh,0)
        self.button_sizer.Add(self.close,0)

        panel_sizer.Add(self.tree_ctrl,1,wx.EXPAND)
        panel_sizer.Add(self.button_sizer,0)

        self.panel.SetSizer(panel_sizer)
        self.panel.Fit()
        self.Hide()

        self.Bind(wx.EVT_CLOSE, self.HideMe)
        self.refresh.Bind(wx.EVT_BUTTON, self.OnRefresh)
        self.close.Bind(wx.EVT_BUTTON, self.HideMe)

        #creating plugin menu entry

        self.plugins_menu = wx.Menu()
        show_entry = self.plugins_menu.Append(-1,"Show Tree")

        self.menu_item = self.parent.AddToMenuBar("Class Hiererchy Tree",
                                                      self.plugins_menu)
        self.parent.BindMenubarEvent(show_entry, self.ShowMe)

    def ShowMe(self,event):
        """
        ShowMe

        Makes window visible and refreshes the class hierarchy tree.
        """
        self.documents = self.parent.GetAllDocuments()
        self.tree_ctrl.Refresh(self.documents)
        self.Show()

    def HideMe(self,event):
        """
        HideMe

        Hides the window.
        """
        self.Hide()

    def OnRefresh(self,event):
        """
        OnRefresh

        Calls the ClassHierarchyCtrl's function Refresh.
        """
        self.tree_ctrl.Refresh(self.documents)

    def NotifyTabChanged(self):
        self.Notify()

    def NotifyDocumentOpened(self):
        self.Notify()

    def NotifyDocumentSaved(self):
        self.Notify()

    def Notify(self):
        try:#the tab change event is produced prematurely
            self.documents = self.parent.GetAllDocuments()
        except: pass

    def Stop(self):
        self.parent.RemoveFromMenubar(self.menu_item)
        self.Destroy()
