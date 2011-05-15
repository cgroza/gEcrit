#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx


class SearchReplace:
    """
    SearchReplace

    Provied the necessary dialogs and functions for the text search
    feature.

    """


    def OnClose(self,event,widget):
        """
        OnClose

        Destroys the suplied widet.
        """
        widget.Destroy()


    def FindDocText(self, event, text_id, other_flags = 0):
        """
        FindDocText

        Creates and initializes the neccesary dialog for text searching.
        Sets up the environment and the variables that indicate the
        position in the text document.
        """
        self._ = wx.FindWindowById(text_id)._

        self.min_text_range = 0
        self.max_text_range = wx.FindWindowById(text_id).GetLength()
        #FindFrame = wx.Frame(None, -1, "Search", size=(200, 200))
        FindData = wx.FindReplaceData()
        FindDialog = wx.FindReplaceDialog(None, FindData, self._("Find"))
        FindDialog.FindData = FindData  # save a reference to it...
        FindDialog.Bind(wx.EVT_FIND_NEXT, lambda event: self.SearchWord(event,
                        text_id, FindData, other_flags))
        FindDialog.Bind(wx.EVT_FIND, lambda event: self.SearchWord(event,
                        text_id, FindData, other_flags))
        FindDialog.Show(True)
        FindDialog.Bind(wx.EVT_CLOSE,lambda event: self.OnClose(event,FindDialog))
        FindDialog.Bind(wx.EVT_FIND_CLOSE, lambda event: self.OnClose(event,FindDialog))

    def SearchWord(self, event, text_id, item, other_flags):
        """
        SearchWord

        Searches the suplied string in the current document.
        Manages highlighting and scrolling to that position.
        Returns the text position if found and -1 if not found.
        When reaches end, resets the current postion in the document to 0.
        """
        cur_doc = wx.FindWindowById(text_id)
        search_flags = item.GetFlags()
        word = item.GetFindString()
        max_pos = cur_doc.GetLength()
        if search_flags in [0, 2, 4, 6]:
            text_pos = cur_doc.FindText(self.max_text_range, self.min_text_range,
                    word, search_flags | other_flags)
            if text_pos != -1:
                start_pos = text_pos
                end_pos = start_pos + len(word)
                self.max_text_range = text_pos - len(word)
                cur_doc.GotoPos(self.max_text_range)
                cur_doc.SetSelection(end_pos, start_pos)
            elif text_pos == -1:
                cur_doc.GotoPos(1)
                self.min_text_range = 0
        else:

            text_pos = cur_doc.FindText(self.min_text_range, max_pos,
                    word, search_flags|other_flags)
            start_pos = text_pos
            end_pos = text_pos + len(word)

            if text_pos != -1:
                cur_doc.GotoPos(text_pos)
                self.min_text_range = end_pos
                cur_doc.SetSelection(start_pos, end_pos)
            elif text_pos == -1:
                cur_doc.GotoPos(1)
                self.min_text_range = 0

    def ReplaceDocText(self, event, text_id, other_flags = 0):
        """
        ReplaceDocText

        Creates and initializes the neccesary dialog for text searching
        and replaceing. Sets up the environment and the variables that indicate the
        position in the text document.
        """

        self._ = wx.FindWindowById(text_id)._

        self.max_text_range = wx.FindWindowById(text_id).GetLength()
        self.min_text_range = 1
        FdRpFrame = wx.Frame(None, -1, self._("Search and Replace"), size=(300,
                             300))
        FdRpData = wx.FindReplaceData()
        ReplaceDialog = wx.FindReplaceDialog(FdRpFrame, FdRpData,
               self._("Search and Replace"), style=wx.FR_REPLACEDIALOG)
        ReplaceDialog.FdRpData = FdRpData
        ReplaceDialog.Bind(wx.EVT_FIND_NEXT, lambda event: self.SearchWord(event,
                           text_id, FdRpData, other_flags))
        ReplaceDialog.Bind(wx.EVT_FIND, lambda event: self.SearchWord(event,
                           text_id, FdRpData, other_flags))

        ReplaceDialog.Bind(wx.EVT_FIND_REPLACE, lambda event: self.ReplaceWord(event,
                           text_id, FdRpData, other_flags))
        ReplaceDialog.Bind(wx.EVT_FIND_REPLACE_ALL, lambda event: self.ReplaceAllWords(event,
                           text_id, FdRpData, other_flags))
        ReplaceDialog.Show(True)
        ReplaceDialog.Bind(wx.EVT_CLOSE,lambda event: self.OnClose(event,ReplaceDialog))
        ReplaceDialog.Bind(wx.EVT_FIND_CLOSE, lambda event: self.OnClose(event,ReplaceDialog))

    def ReplaceWord(self, event, text_id, item, other_flags):
        """
        ReplaceWord

        Searches the suplied string in the current document and replaces
        it with the suplied replacement.
        Manages scrolling to that position.
        Returns the text position if found and -1 if not found.
        When reaches end, resets the current postion in the document to 0.
        """

        cur_doc = wx.FindWindowById(text_id)
        max_pos = cur_doc.GetLength()
        op_flags = item.GetFlags()

        search_word = item.GetFindString()
        replace_word = item.GetReplaceString()
        if op_flags in [0, 2, 4, 6]:
            to_pos = cur_doc.FindText(self.max_text_range, self.min_text_range,
                    search_word, op_flags|other_flags)
            from_pos = to_pos + len(search_word)
            cur_doc.SetTargetStart(to_pos)
            cur_doc.SetTargetEnd(from_pos)

            if from_pos != -1:
                cur_doc.ReplaceTarget(replace_word)
                self.max_text_range = to_pos
                cur_doc.GotoPos(to_pos)
                cur_doc.SetSelection(to_pos, from_pos)
                return to_pos
            elif from_pos == -1:

                self.max_text_range = cur_doc.GetLength()
                return -1
        else:

            from_pos = cur_doc.FindText(self.min_text_range, max_pos,
                    search_word, op_flags|other_flags)
            to_pos = from_pos + len(search_word)
            cur_doc.SetTargetStart(from_pos)
            cur_doc.SetTargetEnd(to_pos)
            if from_pos != -1:
                cur_doc.ReplaceTarget(replace_word)
                self.min_text_range = to_pos
                cur_doc.GotoPos(from_pos)
                cur_doc.SetSelection(to_pos, from_pos)
                return from_pos
            elif from_pos == -1:
                self.min_text_range = 0
                return -1

    def ReplaceAllWords(self, event, text_id, item, other_flags):
        """
        ReplaceAllWords

        Replaces all the occurences of the suplied string with the
        suplie replacement. Promps user when end of file was reached.
        """
        while self.ReplaceWord(0, text_id, item) != -1:
            self.ReplaceWord(0, text_id, item)
        EndReached = wx.MessageDialog(None,
            self._("The end of file was reached!\nNothing to replace."), "",
                style=wx.OK)
        EndReached.ShowModal()


FindRepl = SearchReplace()
