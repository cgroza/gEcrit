#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import keyword
import difflib
import re


class AutoComplet:

    def __init__(self):
        self.replace_dic = {
            "\n": " ",
            ".": " ",
            ",": " ",
            ")": " ",
            "(": " ",
            "]": " ",
            "[": " ",
            "{": " ",
            "}": " ",
            "\"": " ",
            "'": " ",
            ";": " ",
            ":": " ",
            }
        self.pattern = re.compile('\W')

    def CreateCompList(self, text):
        text = re.sub(self.pattern, " ", text)

        split_text = text.split(" ")

        return list(set(split_text))

    def OnKeyPressed(self, event, text_id):
        cur_doc = wx.FindWindowById(text_id)
        cur_doc.AutoCompSetIgnoreCase(False)
        if cur_doc.CallTipActive():
            cur_doc.CallTipCancel()
        key = event.GetKeyCode()

        if key == 32 and event.ControlDown():
            pos = cur_doc.GetCurrentPos()
            word_start = cur_doc.WordStartPosition(pos, True)
            content = cur_doc.GetText()
            word = cur_doc.GetTextRange(word_start, pos)

            lst = difflib.get_close_matches(word, self.CreateCompList(content),
                    5)

            try:
                del lst[0]
            except:
                pass

            st = (" ").join(lst)  #.strip(word)

            if st != "":
                cur_doc.AutoCompShow(pos - word_start, st)

        event.Skip()


AutoComp = AutoComplet()
