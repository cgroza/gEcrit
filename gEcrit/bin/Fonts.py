#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx


def ChangeFont(event, font, IdRange):
    """
    Change Fond

    Updates the editor's font.
    """

    for text_id in IdRange:
        wx.FindWindowById(text_id).StyleSetFont(0, font)
