#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx


class SyntaxDoctor:

    def CheckSyntax(self, event, text_id):
        cur_doc = wx.FindWindowById(text_id)
        file_nm = cur_doc.SaveTarget
        print file_nm

        try:

            ctext = cur_doc.GetText()
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


SyntaxDoc = SyntaxDoctor()
