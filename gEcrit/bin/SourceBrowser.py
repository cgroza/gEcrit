
#   Distributed under the terms of the GPL (GNU Public License)
#
#   gEcrit is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


#SourceBrowser.py


import wx
from configClass import *

class SrcBrowser(wx.TreeCtrl):
    def __init__(self,TargetFile, nb, text_id, parent):
        wx.TreeCtrl.__init__(self,parent, text_id+2000, pos = (0,70), size = (100,100),name = "Source Browser",style = wx.TR_HIDE_ROOT |wx.TR_HAS_BUTTONS |wx.TR_HAS_VARIABLE_ROW_HEIGHT)

        self.parent = parent
        if TargetFile != "" and TargetFile != "New Document":
            try:
                br_file = open(TargetFile, "r")
                n=0
                root = self.AddRoot("Top")
                for line in br_file.readlines():
                    n+=1
                    if "class " in line:
                        root2 = self.AppendItem(root,line+" "+str(n))
                    elif " def " in line:
                        self.AppendItem(root2, line.strip(" def ")+" "+str(n))
                    elif "def " in line and line[0] != " ":
                        self.AppendItem(root, line.strip("def ")+" "+str(n))
            except:
                pass
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, lambda event: self.OnTreeClick(event, text_id))


    def RefreshTree(self,text_id, file_br):
        CurrentTree = wx.FindWindowById(text_id+2000)
        CurrentTree.DeleteAllItems()

        if file_br != "" and file_br != "New Document":
            try:
                br_file = open(file_br, "r")
                n=0
                root = CurrentTree.AddRoot("Top")
                for line in br_file.readlines():
                    n+=1
                    if "class " in line:
                        root2 = CurrentTree.AppendItem(root,line+" "+str(n))
                    elif " def " in line:
                        CurrentTree.AppendItem(root2, line.strip(" def ")+" "+str(n))
                    elif "def " in line and line[0] != " ":
                        CurrentTree.AppendItem(root, line.strip("def ")+" "+str(n))
            except:
                pass

    def OnTreeClick(self,event,text_id):
        TextWidget = wx.FindWindowById(text_id)
        TreeWidget = wx.FindWindowById(text_id+2000)
        id = TreeWidget.GetSelection()

        text = TreeWidget.GetItemText(id)
        TextWidget.ScrollToLine(int(text.split(" ")[-1])-1)
