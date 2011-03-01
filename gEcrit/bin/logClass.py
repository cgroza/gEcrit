#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from configClass import *


class Logger:

    def AddLogEntry(self, entry):
        if Config.GetOption("ActLog"):
            LogFile = open("data/gEcrit.log", "a")
            LogFile.write("\n")
            LogFile.write(entry)
            LogFile.close()

    def EraseLog(self, event):
        LogFile = open("data/gEcrit.log", "w")
        LogFile.write("")
        LogFile.close()

    def ReadLog(self):
        LogFile = open("data/gEcrit.log", "r")
        logcontent = ""
        try:
            for line in LogFile.readlines():
                logcontent += line
        except:
            logcontent = ""

        return logcontent


Log = Logger()
