#!/usr/bin/python
# -*- coding: utf-8 -*-

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
import yapsy.IPlugin
from data.plugins.categories import General
import urllib

class PastebinDialog(wx.Frame,General, yapsy.IPlugin.IPlugin):
    """
    PastebinWin

    Provides the necessary controls and function to submit
    data to pastebin.com.
    Builds the GUI and interacts with the pastebin library.
    """

    def __init__(self):
        self.name = "Pastebin.com Uploader"

    def Init(self, parent):
        """
        __init__

        Initializes the frame and builds the GUI.
        Sets the format list dictionary and binds
        the appropriate events.

        Initializes the pastebin library.
        """
        self.parent = parent
        self.current_doc = None

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

        self.Paste = Pastebin()


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

        self.plugins_menu = wx.Menu()
        show_entry = self.plugins_menu.Append(-1,"Upload to Pastebin")

        self.menu_item = self.parent.AddToMenuBar("Pastebin Uploader",
                                                      self.plugins_menu)
        self.parent.BindMenubarEvent(show_entry, self.ShowMe)


    def OnSubmit(self, event):
        """
        OnSubmit

        Collects data from the controls and feeds it
        to the pastebin library for submition.

        If successful prompts the user. If not, returns
        a MessageDialog with the error returned by pastebin.
        """
        try:
            url = self.Paste.submit(self.current_doc.GetText(),
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


    def ShowMe(self, event):
        """
        ShowMe

        Makes window visible.
        """
        self.Show()
        self.current_doc = self.parent.GetCurrentDocument()

    def HideMe(self, event):
        """
        HideMe

        Hides the window.
        """
        self.Hide()

    def NotifyTabChanged(self):
        try:
            self.current_doc = self.parent.GetCurrentDocument()
        except: pass

    def Stop(self):
        self.parent.RemoveFromMenubar(self.menu_item)
        self.Destroy()

class Pastebin(object):

    prefix_url = 'http://pastebin.com/'

    subdomain_url = 'http://%s.pastebin.com/'  # % paste_subdomain

    api_url = 'http://pastebin.com/api_public.php'

    paste_expire_date = ('N', '10M', '1H', '1D', '1M')

    paste_format = (
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
        )

    @classmethod
    def submit(cls, paste_code, paste_name=None, paste_subdomain=None,
               paste_private=None, paste_expire_date=None, paste_format=None):

        argv = {'paste_code': str(paste_code)}

        if paste_name is not None:
            argv['paste_name'] = str(paste_name)

        if paste_subdomain is not None:
            paste_subdomain = str(paste_subdomain).strip().lower()
            argv['paste_subdomain'] = paste_subdomain

        if paste_private is not None:
            argv['paste_private'] = int(bool(int(paste_private)))

        if paste_expire_date is not None:
            paste_expire_date = str(paste_expire_date).strip().upper()
            if not paste_expire_date in cls.paste_expire_date:
                raise ValueError, "Bad expire date: %s" % \
                    paste_expire_date

        if paste_format is not None:
            paste_format = str(paste_format).strip().lower()
            if not paste_format in cls.paste_format:
                raise ValueError, "Bad format: %s" % paste_format
            argv['paste_format'] = paste_format

        fd = urllib.urlopen(cls.api_url, urllib.urlencode(argv))
        try:
            response = fd.read()
        finally:
            fd.close()
        del fd

        if argv.has_key('paste_subdomain'):
            prefix = cls.subdomain_url % paste_subdomain
        else:
            prefix = cls.prefix_url
        if not response.startswith(prefix):
            return response
        return response
