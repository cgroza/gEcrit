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
        find_data = wx.FindReplaceData()
        find_dlg = wx.FindReplaceDialog(None, find_data, self._("Find"))
        find_dlg.find_data = find_data  # save a reference to it...
        find_dlg.Bind(wx.EVT_FIND_NEXT, lambda event: self.SearchWord(event,
                        text_id, find_data, other_flags))
        find_dlg.Bind(wx.EVT_FIND, lambda event: self.SearchWord(event,
                        text_id, find_data, other_flags))
        find_dlg.Show(True)
        find_dlg.Bind(wx.EVT_CLOSE,lambda event: self.OnClose(event,find_dlg))
        find_dlg.Bind(wx.EVT_FIND_CLOSE, lambda event: self.OnClose(event,find_dlg))

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
        find_repl_frame = wx.Frame(None, -1, self._("Search and Replace"), size=(300,
                             300))
        find_repl_data = wx.FindReplaceData()
        replace_dlg = wx.Findreplace_dlg(find_repl_frame, find_repl_data,
               self._("Search and Replace"), style=wx.FR_REPLACEDIALOG)
        replace_dlg.find_repl_data = find_repl_data
        replace_dlg.Bind(wx.EVT_FIND_NEXT, lambda event: self.SearchWord(event,
                           text_id, find_repl_data, other_flags))
        replace_dlg.Bind(wx.EVT_FIND, lambda event: self.SearchWord(event,
                           text_id, find_repl_data, other_flags))

        replace_dlg.Bind(wx.EVT_FIND_REPLACE, lambda event: self.ReplaceWord(event,
                           text_id, find_repl_data, other_flags))
        replace_dlg.Bind(wx.EVT_FIND_REPLACE_ALL, lambda event: self.ReplaceAllWords(event,
                           text_id, find_repl_data, other_flags))
        replace_dlg.Show(True)
        replace_dlg.Bind(wx.EVT_CLOSE,lambda event: self.OnClose(event,replace_dlg))
        replace_dlg.Bind(wx.EVT_FIND_CLOSE, lambda event: self.OnClose(event,replace_dlg))

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
