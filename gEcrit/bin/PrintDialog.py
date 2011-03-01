#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx.html
import wx


class PrettyPrinter(wx.html.HtmlEasyPrinting):

    def __init__(self, filename, text_id, parent=None):
        wx.html.HtmlEasyPrinting.__init__(self)
        self.parent = parent

        data = wx.PrintDialogData()

        data.EnableSelection(True)
        data.EnablePrintToFile(True)
        data.EnablePageNumbers(True)
        data.SetMinPage(1)
        data.SetMaxPage(5)
        data.SetAllPages(True)

        dlg = wx.PrintDialog(parent, data)

        dlg.Destroy()
        cur_doc = wx.FindWindowById(text_id)
        content = cur_doc.GetText()
        linenumbers = cur_doc.GetLineCount()
        self.DoPrint(content, filename, linenumbers)

    def DoPrint(self, text, filename, linenumbers=1):
        self.SetHeader(filename)
        self.PrintText(self.ToHTML(text, linenumbers), filename)

    def ToHTML(self, text, linenumbers):
        text = text.replace('&', "&amp;").replace('<', "&lt;").replace('>',
                "&gt;")

        if linenumbers:
            text = "1<a href=\"#\">00000</a>" + text.replace(' ',
                    " &nbsp;")
            x = 0
            l = len(text)
            line = 2
            n = ""
            while x < l:
                if text[x] == "\n":
                    n = n + "\n" + str(line)
                    if line < 10:
                        n = n + "<a href=\"#\">00000</a>"
                    elif line < 100:
                        n = n + "<a href=\"#\">0000</a>"
                    elif line < 1000:
                        n = n + "<a href=\"#\">000</a>"
                    else:
                        n = n + "<a href=\"#\">00</a>"
                    line = line + 1
                else:
                    n = n + text[x]
                x = x + 1

            text = n

        thehtml = \
            "<html><body link=\"#FFFFFF\" vlink=\"#FFFFFF\" alink=\"#FFFFFF\">" + \
            text.replace("\n", "\n<br>") + "</span></body></html>"
        return thehtml


