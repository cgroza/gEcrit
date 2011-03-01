#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib


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


Paste = Pastebin()
