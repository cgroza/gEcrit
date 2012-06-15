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

#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
from data.plugins.categories import General
import yapsy.IPlugin

try:
    import enchant
    import enchant.checker.wxSpellCheckerDialog
except:
    print "Spell checker pyenchant is not available."


class SpellCheckDialog(enchant.checker.wxSpellCheckerDialog.wxSpellCheckerDialog):
    def __init__(self, parent):
        self.parent = parent
        enchant.checker.wxSpellCheckerDialog.wxSpellCheckerDialog.__init__(self,self.parent,
                                            -1, title = "Spell Checker")



class SpellChecker(General, yapsy.IPlugin.IPlugin):
    """
    Provides the necessary functions for spellchecking.
    Uses the enchant module.

    """

    def __init__(self):
        """
        __init__

        Initializes the enchant module, sets the language
        dictionary.
        """

        self.name = "Spell Checker"

        try:
            self.dictionary = enchant.Dict()
        except enchant.Error:
            print "The Dictionary could not be identified.\n  Falling back to English."
            self.dictionary = enchant.Dict("en_US")
        self.spell_checker = enchant.checker.SpellChecker(self.dictionary.tag)

    def Init(self, parent):
        self.parent = parent
        self.current_doc = None
        self.last_word = ""

        self.plugins_menu = wx.Menu()
        edit_entry = self.plugins_menu.Append(-1,"Show Spell Checker")

        self.menu_item = self.parent.AddToMenuBar("Spell Checker",
                                                      self.plugins_menu)
        self.parent.BindMenubarEvent(edit_entry, self.ShowMe)

        self.spell_dlg = SpellCheckDialog(self.parent)
        self.spell_dlg.SetSpellChecker(self.spell_checker)
        self.spell_dlg.Bind(wx.EVT_CLOSE, self.HideMe)

    def CheckWord(self, word):
        """
        CheckWord

        Calls enchant to check the suplied argument word.
        """
        return self.dictionary.check(word)

    def GetSuggestion(self, word):
        """
        GetSuggestion

        Calls the enchant library to generate
        spelling suggestion for the suplied argument
        word.
        """
        return self.dictionary.suggest(word)

    def ShowSpellDialog(self, event):
        """"
        ShowSpellDialog

        not implemented
        """
        pass

    def SpellCheck(self, event):
        """
            OnSpellCheck

            Delivers the data to the spell checker, and manages
            the underlineing and clearing of the text.
        """

        st = self.current_doc.WordStartPosition(self.current_doc.GetCurrentPos(), False)
        end = self.current_doc.WordEndPosition(self.current_doc.GetCurrentPos(), False)
        word = self.current_doc.GetTextRange(st, end)
        self.last_word = word


        spelled_ok = self.CheckWord(word)

        if not spelled_ok:
            self.current_doc.StartStyling(st, wx.stc.STC_INDIC0_MASK)
            self.current_doc.SetStyling(end - st, wx.stc.STC_INDIC0_MASK)


        else:
            self.current_doc.StartStyling(st, wx.stc.STC_INDIC0_MASK)
            self.current_doc.SetStyling(end - st, 0)
            self.current_doc.spell_error = False

        event.Skip()

    def NotifyDocumentOpened(self):
        self.current_doc = self.parent.GetCurrentDocument()
        self.current_doc.Bind(wx.stc.EVT_STC_CHARADDED, self.SpellCheck)
    	self.current_doc.IndicatorSetStyle(0, wx.stc.STC_INDIC_SQUIGGLE)
    	self.current_doc.IndicatorSetForeground(0, wx.RED)

    def NotifyNewTabOpened(self):
        self.current_doc = self.parent.GetCurrentDocument()
        self.current_doc.Bind(wx.stc.EVT_STC_CHARADDED, self.SpellCheck)
    	self.current_doc.IndicatorSetStyle(0, wx.stc.STC_INDIC_SQUIGGLE)
    	self.current_doc.IndicatorSetForeground(0, wx.RED)

    def NotifyTabChanged(self):
        self.current_doc = self.parent.GetCurrentDocument()
        self.last_word = ""

    def HideMe(self, event):
        self.spell_dlg.Hide()

    def ShowMe(self, event):
        rng = self.current_doc.GetSelection()
        self.spell_checker.set_text(self.current_doc.GetTextRange(rng[0],rng[1]))
        self.spell_dlg.SetSpellChecker(self.spell_checker)
        self.spell_dlg.Show()
