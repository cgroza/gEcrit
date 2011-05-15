#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
from data.plugins.categories import General
import yapsy.IPlugin

class SrcTree(wx.TreeCtrl):
    def __init__(self, parent, file_br):
        self.parent = parent
        wx.TreeCtrl.__init__(self ,self.parent, -1, size = (-1,-1) ,name="Source Browser",
                             style=wx.TR_HIDE_ROOT | wx.TR_HAS_BUTTONS |
                             wx.TR_HAS_VARIABLE_ROW_HEIGHT)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK,  self.OnTreeClick)

        self.file_br = file_br


    def OnTreeClick(self, event):
        """
        OnTreeClick

        Scrolls the editor to the appropriate line upon right click.
        """
        id = self.GetSelection()

        text = self.GetItemText(id)
        self.parent.current_doc.ScrollToLine(int(text.split(" ")[-1]) - 1)

    def RefreshTree(self):
        """
        RefreshTree

        Finds the current document, gathers data and displays
        it in the TreeCtrl.
        """

        self.DeleteAllItems()
        #collect data  and add it on  the tree
        if self.file_br not in ["","New Document"]:
            try:
                br_file = open(self.file_br, "r")
                n = 0
                root = self.AddRoot("Top")
                for line in br_file.readlines():
                    n += 1
                    if "class " in line and ":" in line:
                        root2 = self.AppendItem(root, line + " " +
                                str(n))
                        self.SortChildren(root2)
                    elif " def " in line and ":" in line:
                        self.AppendItem(root2, line.strip(" def ") +
                                " " + str(n))
                        self.SortChildren(root2)
                    elif "def " in line and ":" in line and line[0] != " ":
                        self.AppendItem(root, line.strip("def ") +
                                " " + str(n))

                self.SortChildren(root)
                br_file.close()
            except:
                pass


class PythonSourceBrowser(wx.Panel, General, yapsy.IPlugin.IPlugin):
    """
    SrcBrowser

    Provides the necessary functions for collecting data and
    displays the date using a TreeCtrl.

    Used to display the classes and functions in the current
    file.
    """
    def __init__(self):
        self.name = "Python Source Browser"

    def Init(self, parent):
        #set up the plugin into the application
        self.parent = parent
        wx.Panel.__init__(self, self.parent.GetSidePanel())
        self.parent.AddToSidePanel(self, "Source Browser")
        self.src_trees = {}
        self.current_doc = None
        self.last_doc = None
        self.tree_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.tree_sizer)
        self.Fit()

    def NewTree(self,file, doc):
        """
        NewTree

        Creates a new source tree.
        """
        #createa a new tree for the new file
        new_tree = SrcTree(self, file)
        new_tree.RefreshTree()
        self.src_trees[doc] = new_tree
        return new_tree

    def NotifyTabChanged(self):
        #update the displayed tree for the current file
        self.last_doc = self.current_doc
        self.current_doc = self.parent.GetCurrentDocument()
        if self.current_doc in self.src_trees:
            if self.last_doc != None:
                self.src_trees[self.last_doc].Hide()
            self.src_trees[self.current_doc].Show()

        else:
            self.src_trees[self.current_doc] = self.NewTree(
                       self.current_doc.GetFilePath(), self.current_doc)

            self.tree_sizer.Add(self.src_trees[self.current_doc], 1, wx.EXPAND)
            if self.last_doc != None:
                self.src_trees[self.last_doc].Hide()
            self.src_trees[self.current_doc].Show()
        self.Layout()

    def NotifyDocumentOpened(self):
        #create a new tree because a new document is present
        self.last_doc = self.current_doc
        self.current_doc = self.parent.GetCurrentDocument()
        if self.current_doc not in self.src_trees:
            self.src_trees[self.current_doc] = self.NewTree(
                       self.current_doc.GetFilePath(), self.current_doc)

    def NotifyDocumentSaved(self):
        #update the tree information because the contents of the file changed
        self.current_doc = self.parent.GetCurrentDocument()
        self.src_trees[self.current_doc].file_br = self.current_doc.GetFilePath()
        self.src_trees[self.current_doc].RefreshTree()


    def NotifyNewTabOpened(self):
        self.NotifyDocumentOpened()

    def Stop(self):
        self.parent.DeleteSidePage("Source Browser")
