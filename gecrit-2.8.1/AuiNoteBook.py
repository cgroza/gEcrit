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


import wx.aui

class AuiNoteBook(wx.aui.AuiNotebook):
    def __init__(self, parent):
        """
        __init__
        
        Basic constructor.
        """
        self.parent = parent

        wx.aui.AuiNotebook.__init__(self, self.parent, -1 ,style=wx.aui.AUI_NB_TOP|wx.BORDER_SUNKEN|wx.aui.AUI_NB_TAB_SPLIT|wx.aui.AUI_NB_TAB_MOVE|wx.aui.AUI_NB_CLOSE_ON_ACTIVE_TAB|wx.aui.AUI_NB_SCROLL_BUTTONS )

        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnChangeTab)
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, lambda event: self.parent.ManageCloseTab(event,self.parent.id_range[self.GetSelection()]))
        self.Bind(wx.aui.EVT_AUINOTEBOOK_BEGIN_DRAG, self.OnBeginDrag)
        self.Bind(wx.aui.EVT_AUINOTEBOOK_END_DRAG, self.OnEndDrag)
        self.SetId(900)  #Needed in StcControl.py

        self.__dragged_doc = None


    def OnChangeTab(self, event):
        """
        OnChangeTab

        Alerts the plugins of the current document change.
        """

        wx.FindWindowById((self.parent.id_range)[self.GetSelection()]).SetStatusFileMode()

        for g in self.parent.general_plugins:
            self.parent.general_plugins[g].NotifyTabChanged() #tells the plugins the document
                                                            # has changed.

    def OnBeginDrag(self, event):
        """
        OnBeginDrag

        Updates the internal representation of the tabs.
        You should have nothing to do with this method.
        """
        self.__dragged_doc = self.parent.id_range.pop(self.GetSelection())
        event.Skip()

    def OnEndDrag(self, event):
        """
        OnEndDrag

        Updates the internal representation of the tabs.
        You should have nothing to do with this method.
        """

        self.parent.id_range.insert(self.GetSelection(),self.__dragged_doc)
        event.Skip()
