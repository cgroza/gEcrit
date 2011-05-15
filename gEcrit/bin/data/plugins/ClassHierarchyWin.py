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
        self.base_cls = []

    def GenerateHierarchies(self,docs):
        """
        GenerateHierarchies

        Gathers data using helper functions and organizes it
        on the tree.
        First clears the tree with the help of the helper function
        and then populates it.
        """
        classed = []
        file_list = self.GetFileList(docs)
        if file_list:
            for fl in file_list:
                cls = self.GetClassesFromFile(fl)
                if cls:
                    for c in cls:
                        self.classes.append(c)

        for c in self.classes:
            if not self.Inherits(c):
                self.base_cls.append(c)
                self.classes.remove(c)

        for c in self.classes:
            bases = self.GetClassBases(c)
            if self.GetClassBases(c):
                for b in bases:
                    if b not in self.classes:
                        self.base_cls.append(c)


        for c in self.base_cls:
            kids = self.FindChilds(c)
            if c not in classed:
                root = self.AppendItem(self.root,self.CleanName(c))
                classed.append(c)
            if kids:
                for n in kids:
                    root2 = self.AppendItem(root,self.CleanName(n))
                    kids_kids = self.FindChilds(n)
                    i = 0
                    if kids_kids:
                        kids_len = len(kids_kids)
                    while kids_kids:
                        try:
                            kid = kids_kids[i]
                        except: pass
                        has_kid = self.FindChilds(kid)
                        if not has_kid and i == kids_len: break
                        i+=1
                        root3 = self.AppendItem(root2,self.CleanName(kid))


        self.classes = []


    def FindChilds(self,cls):
        """
        FindChilds

        Finds the child classes of the suplied argument cls.
        Uses a helper class to check inheritance.
        Return the list if found. If not, returns False.
        """
        childs = []
        for i in self.classes:
            if self.InheritsFrom(cls,i):
                childs.append(i)
        if childs:
             return childs
        else:
             return False


    def GetClassesFromFile(self,file_path):
        """
        GetClassesFromFile

        Reads and collects the class statements from the suplied
        file_path argument.
        Creates a list of found classes and returns it if not empty.
        If empty, returns False.
        """
        classes = []
        try:
            fl = open(file_path,"r")
            for line in fl.readlines():
                if "class" in line and ":" in line:
                    line = line.strip("class ")
                    line2 = ""
                    for i in line:
                        if i!=":": line2+=i

                    classes.append(line2)
            if classes:
                 return classes
            else:
                 return False
            fl.close()
        except:
             return False


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
        if file_list:
             return file_list
        else:
             return False

    def Refresh(self,docs):
        """
        Refresh

        Rebuild the class hierarchy tree.
        """
        self.DeleteChildren(self.root)
        self.GenerateHierarchies(docs)


    def Inherits(self,cls_line):
        """
        Inherits

        Checks if the suplied argument cls_line has a base class.
        Returns True or False.
        """

        if "(" not in cls_line:
            return False
        else:
            lst = cls_line.split("(")

            if lst[-1][0] == ")":

                return False

            elif lst[-1][0] != " " or  lst[-1][-2] != ")":

                return True



    def GetClassBases(self,cls):
        """
        GetBaseClasses

        Iterates through the class list and makes a list with
        classes that have no base.
        """
        name = ""
        for i in cls:
            if i != ")":
                name+=i

        lst = name.split("(")
        cls_lst = lst[-1].split(",")
        if cls_lst:
             return cls_lst
        else:
             return False

    def CleanName(self,name):
        """
        CleanName

        Takes the argument name and clears all the syntactic
        elements to make it suitable for displaying.
        """
        name2 = ""
        for c in name:
            if c == "(":
                break
            else: name2+=c

        return name2.strip("\n")

    def InheritsFrom(self,base_class,child_class):
        """
        InheritsFrom

        Takes the sting argument base_class and checks if it the base
        of the string argument child_class.
        Returns True or False.
        """
        if self.CleanName(base_class) in child_class.split("(")[-1]:
            return True
        else:
            return False



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
