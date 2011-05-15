#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import yapsy.IPlugin
from data.plugins.categories import General


class HtmlConverter(General, yapsy.IPlugin.IPlugin):

    def __init__(self):
        self.name = "HTML Converter"

    def Init(self, parent):
        self.parent = parent
        self.current_doc = None

        self.plugins_menu = wx.Menu()
        convert_entry = self.plugins_menu.Append(-1,"Convert File")

        self.menu_item = self.parent.AddToMenuBar("HTML Converter ",
                                                      self.plugins_menu)
        self.parent.BindMenubarEvent(convert_entry, self.ToHtmlHelper)


    def ToHtmlHelper(self,event):
        save_path = wx.FileDialog(None, style=wx.SAVE)
        if save_path.ShowModal() == wx.ID_OK:
            html_file = open(save_path.GetPath(),"w")
            html_file.write(self.ToHTML())
            html_file.close()

    def ToHTML(self):
        """
        ToHTML

        Formats the document text to HTML form.
        Returns it.
        """
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

    def NotifyTabChanged(self):
        try: #the tab change event is produced prematurely
            self.current_doc = self.parent.GetCurrentDocument()
        except: pass

    def Stop(self):
         self.parent.RemoveFromMenubar(self.menu_item)
