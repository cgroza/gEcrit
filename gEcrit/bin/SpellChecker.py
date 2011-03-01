#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    import enchant
except:
    print "Spell checker pyenchant is not available."


class NeatSpell:

    def __init__(self):
        try:
            self.dictionary = enchant.Dict()
        except enchant.Error:
            print "The Dictionary could not be identified.\n  Falling back to English."
            self.dictionary = enchant.Dict("en_US")

    def CheckWord(self, word):
        return self.dictionary.check(word)

    def GetSuggestion(self, word):
        return self.dictionary.suggest(word)

    def ShowSpellDialog(self, event):
        pass


WordSpeller = NeatSpell()
