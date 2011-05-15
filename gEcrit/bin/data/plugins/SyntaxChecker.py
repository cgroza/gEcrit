#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import yapsy.IPlugin
from data.plugins.categories import General

class SyntaxDoctor(General, yapsy.IPlugin.IPlugin):
    """
    SyntaxDoctor

    Manages the syntax checking feature.

    """
    def __init__(self):
        self.name = "Python Syntax Doctor"

    def Init(self, parent = None):
        self.parent = parent
        self.current_doc = None

        self.plugins_menu = wx.Menu()
        check_entry = self.plugins_menu.Append(-1,"Check Syntax")

        self.menu_item = self.parent.AddToMenuBar("Py Syntax Doctor",
                                                      self.plugins_menu)
        self.parent.BindMenubarEvent(check_entry, self.CheckSyntax)

    def CheckSyntax(self, event):
        """
        CheckSyntax

        Finds the current document and calls python
        to check the correctitude of the file.
        If error is reported, prompts the user with
        the error message.
        If not, prompts the user with a success message.

        """

        file_nm = self.current_doc.GetFilePath()


        try:

            ctext = self.current_doc.GetText()
            ctext = ctext.replace('\r\n', '\n').replace('\r', '\n')
            compile(ctext, file_nm, 'exec')
            say_ok = wx.MessageDialog(None,
                    "No errors have been detected.", "Syntax Check")
            if say_ok.ShowModal() == wx.ID_OK:
                say_ok.Destroy()
        except Exception, e:

            ln_num = ""
            excstr = str(e)
            try:
                for c in exctr:
                    if int(c):
                        ln_num += str(c)
                n = int(ln_num)

                cur_doc.ScrollToLine(n)
                cur_doc.GotoLine(n)
            except:
                say_error = wx.MessageDialog(None, 'Error:' + excstr,
                        'Error Found')
                if say_error.ShowModal() == wx.ID_OK:
                    say_error.Destroy()

    def NotifyTabChanged(self):
        try: #the tab change event is produced prematurely
            self.current_doc = self.parent.GetCurrentDocument()
        except: pass

    def Stop(self):
         self.parent.RemoveFromMenubar(self.menu_item)
