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

import wx.html
import wx


class PrettyPrinter(wx.html.HtmlEasyPrinting):
    """
    PrettyPrinter

    Provides the necessary functions for printing
    documents.

    Build the GUI and provides the appropriate controls.
    """

    def __init__(self, parent=None):
        """
        __init__

        Initializes the HtmlEasyPrinting object.

        Creates the necessary dialogs.
        Retrieves the content to be printed.

        """
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


        self.DoPrint()

    def DoPrint(self):
        """
        DoPrint

        Sets the print hedear and calls the HTML
        generation function.

        Sends the output to HtmlEasyPrinting object for printing.
        """
        filename = self.parent.GetCurrentDocument().GetFileName()
        self.SetHeader(filename)
        self.PrintText(self.ToHTML(), filename)

    def ToHTML(self):
        """
        ToHTML

        Formats the document text to HTML form.
        Returns it.
        """
        self.current_doc = self.parent.GetCurrentDocument()
        text = self.current_doc.GetText().replace('&', "&amp;").replace('<', "&lt;").replace('>',
                "&gt;")

        if self.current_doc.GetLineCount():
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
