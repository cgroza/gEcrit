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
import re
from pyctags import exuberant_ctags, ctags_file
from pyctags.harvesters import name_lookup_harvester, by_name_harvester

class AutoComplet:
    """
    AutoComplet

    Manages the editors autocompletion features.
    """
    def __init__(self):
        """
        __init__

        Creates the re pattern used for special character removal.
        """
        #self.pattern = re.compile('\W')
        self.source_files = []
        self.UpdateCTagsFiles([])
        self.entered_chars = 0

    def CreateCompList(self, chunk):
        """
        CreateCompList

        Interacts with pyctags to create a completition list.
        """
        #text = re.sub(self.pattern, " ", text)

        #split_text = text.split(" ")

        names = self.names.starts_with(chunk)

        return list(set(names))

    def OnKeyPressed(self, event, text_id):
        """
        OnKeyPressed

        Using the editors facilities, it pops a list of possible
        completions on Ctrl+Space shortcut.
        """
        cur_doc = wx.FindWindowById(text_id)
        cur_doc.AutoCompSetIgnoreCase(False)

        key = event.GetKey()

        #if key == 32 and event.ControlDown():

        self.entered_chars += 1


        if self.entered_chars == 3 and key not in [10,32]:
            pos = cur_doc.GetCurrentPos()
            word_start = cur_doc.WordStartPosition(pos, True)
            word = cur_doc.GetTextRange(word_start, pos)

            try:
                del lst[0]
            except:
                pass

            lst = self.CreateCompList(word)
            st = (" ").join(lst)

            if st != "":
                if cur_doc.CallTipActive():
                    cur_doc.CallTipCancel()
                    
                cur_doc.AutoCompShow(pos - word_start, st)
            self.entered_chars = 0

        if self.entered_chars > 3:
            self.entered_chars = 0

        event.Skip()

    def UpdateCTagsFiles(self, id_range):
        for i in id_range:
            doc = wx.FindWindowById(i)
            file_path = doc.GetFilePath()
            if file_path not in self.source_files:
                self.source_files.append(file_path)
        self.UpdateCTagsGenerator()

    def UpdateCTagsGenerator(self):
        self.ctags_generator =  exuberant_ctags(files = self.source_files)
        try:
            if self.source_files:
                self.list_of_tags = self.ctags_generator.generate_tags(
                                generator_options={'--fields' : '+n'})

            self.names =  name_lookup_harvester()
            self.by_name = by_name_harvester()
            self.tagfile = ctags_file(self.list_of_tags, harvesters=[
                                              self.names, self.by_name])
        except:
            pass

AutoComp = AutoComplet()
