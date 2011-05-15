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
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, lambda event: self.parent.ManageCloseTab(event,self.parent.IdRange[self.GetSelection()]))
        self.Bind(wx.aui.EVT_AUINOTEBOOK_BEGIN_DRAG, self.OnBeginDrag)
        self.Bind(wx.aui.EVT_AUINOTEBOOK_END_DRAG, self.OnEndDrag)
        self.SetId(900)  #Needed in StcControl.py

        self.__dragged_doc = None


    def OnChangeTab(self, event):
        """
        OnChangeTab

        Alerts the plugins of the current document change.
        """


        wx.FindWindowById((self.parent.IdRange)[self.GetSelection()]).SetStatusFileExt()

        for g in self.parent.general_plugins:
            self.parent.general_plugins[g].NotifyTabChanged() #tells the plugins the document
                                                            # has changed.

    def OnBeginDrag(self, event):
        """
        OnBeginDrag

        Updates the internal representation of the tabs.
        You should have nothing to do with this method.
        """
        self.__dragged_doc = self.parent.IdRange.pop(self.GetSelection())
        event.Skip()

    def OnEndDrag(self, event):
        """
        OnEndDrag

        Updates the internal representation of the tabs.
        You should have nothing to do with this method.
        """

        self.parent.IdRange.insert(self.GetSelection(),self.__dragged_doc)
        event.Skip()
