#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
from PastebinLib import *


class PastebinWin(wx.Frame):

    def __init__(self, parent):
        self.text_id = 0
        self.src_formats = [
            'python',
            'abap',
            'actionscript',
            'actionscript3',
            'ada',
            'apache',
            'applescript',
            'apt_sources',
            'asm',
            'asp',
            'autoit',
            'avisynth',
            'bash',
            'basic4gl',
            'bibtex',
            'blitzbasic',
            'bnf',
            'boo',
            'bf',
            'c',
            'c_mac',
            'cill',
            'csharp',
            'cpp',
            'caddcl',
            'cadlisp',
            'cfdg',
            'klonec',
            'klonecpp',
            'cmake',
            'cobol',
            'cfm',
            'css',
            'd',
            'dcs',
            'delphi',
            'dff',
            'div',
            'dos',
            'dot',
            'eiffel',
            'email',
            'erlang',
            'fo',
            'fortran',
            'freebasic',
            'gml',
            'genero',
            'gettext',
            'groovy',
            'haskell',
            'hq9plus',
            'html4strict',
            'idl',
            'ini',
            'inno',
            'intercal',
            'io',
            'java',
            'java5',
            'javascript',
            'kixtart',
            'latex',
            'lsl2',
            'lisp',
            'locobasic',
            'lolcode',
            'lotusformulas',
            'lotusscript',
            'lscript',
            'lua',
            'm68k',
            'make',
            'matlab',
            'matlab',
            'mirc',
            'modula3',
            'mpasm',
            'mxml',
            'mysql',
            'text',
            'nsis',
            'oberon2',
            'objc',
            'ocaml-brief',
            'ocaml',
            'glsl',
            'oobas',
            'oracle11',
            'oracle8',
            'pascal',
            'pawn',
            'per',
            'perl',
            'php',
            'php-brief',
            'pic16',
            'pixelbender',
            'plsql',
            'povray',
            'powershell',
            'progress',
            'prolog',
            'properties',
            'providex',
            'qbasic',
            'rails',
            'rebol',
            'reg',
            'robots',
            'ruby',
            'gnuplot',
            'sas',
            'scala',
            'scheme',
            'scilab',
            'sdlbasic',
            'smalltalk',
            'smarty',
            'sql',
            'tsql',
            'tcl',
            'tcl',
            'teraterm',
            'thinbasic',
            'typoscript',
            'unreal',
            'vbnet',
            'verilog',
            'vhdl',
            'vim',
            'visualprolog',
            'vb',
            'visualfoxpro',
            'whitespace',
            'whois',
            'winbatch',
            'xml',
            'xorg_conf',
            'xpp',
            'z80',
            ]

        self.exp_dates = ['N', '10M', '1H', '1D', '1M']

        Paste = Pastebin()

        self.parent = parent
        wx.Frame.__init__(self, self.parent, -1, "Pastebin Snippet",
                          size=(300, 330))
        pastebin_pnl = wx.Panel(self)

        name_info = wx.StaticText(pastebin_pnl, -1, "Snippet name:", pos=
                                  (10, 10), size=(-1, -1))
        self.paste_name = wx.TextCtrl(pastebin_pnl, -1, "", pos=(10, 30),
                size=(200, 30))

        formats_info = wx.StaticText(pastebin_pnl, -1,
                "Choose a source format:", pos=(10, 65), size=(-1, -1))
        self.formats = wx.Choice(pastebin_pnl, -1, choices=self.src_formats,
                                 pos=(10, 90), size=(-1, -1))

        date_info = wx.StaticText(pastebin_pnl, -1, "Expire in:", pos=(10,
                                  130), size=(-1, -1))
        self.date = wx.Choice(pastebin_pnl, -1, choices=self.exp_dates,
                              pos=(10, 155), size=(-1, -1))

        self.private_paste = wx.CheckBox(pastebin_pnl, -1,
                "Make this snippet private.", pos=(10, 195), size=(-1, -1))

        SubmitBtn = wx.Button(pastebin_pnl, -1, "Submit", pos=(200, 290),
                              size=(-1, -1))
        CloseBtn = wx.Button(pastebin_pnl, -1, "Close", pos=(100, 290),
                             size=(-1, -1))

        SubmitBtn.Bind(wx.EVT_BUTTON, self.OnSubmit)
        CloseBtn.Bind(wx.EVT_BUTTON, self.HideMe)
        self.Bind(wx.EVT_CLOSE, self.HideMe)

        self.Centre()
        self.Hide()

    def OnSubmit(self, event):
        try:
            url = Paste.submit(wx.FindWindowById(self.text_id).GetText(),
                               self.paste_name.GetValue(), paste_private=
                               self.private_paste.GetValue(),
                               paste_expire_date=(self.exp_dates)[self.date.GetCurrentSelection()],
                               paste_format=(self.src_formats)[self.formats.GetCurrentSelection()])
        except IOError:
            url = "The connection has timed out."
        if "http://pastebin" not in url:
            error_msg = wx.MessageDialog(None, "An error has occured:\n" +
                    url, "Failed", wx.ICON_ERROR)
            if error_msg.ShowModal() == wx.ID_OK:
                error_msg.Destroy()
            return

        say_url = wx.MessageDialog(None,
                                   "The snippet is available at:\n" +
                                   url, "Success", wx.ICON_INFORMATION)
        if say_url.ShowModal() == wx.ID_OK:
            say_url.Destroy()

    def ShowMe(self, event, text_id):
        self.Show()
        self.text_id = text_id

    def HideMe(self, event):
        self.Hide()


