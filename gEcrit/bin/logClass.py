#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
from configClass import *



class Logger:
    """
    Logger

    Provides function to record applications activity, view the log, and
    erasing it.
    """
    def __init__(self):
        self.HOMEDIR = os.path.expanduser('~')

    def AddLogEntry(self, entry):
        """
            AddLogEntry

            Opens the log file and appends a string with
            the format date,time : string to it.
            The string is received from its argument.
        """
        if Config.GetOption("ActLog"):
            LogFile = open(self.HOMEDIR+"/.gEcrit/gEcrit.log", "a")
            LogFile.write("\n")
            LogFile.write(time.ctime() + " : "+ entry)
            LogFile.close()

    def EraseLog(self, event):
        """
        EraseLog

        Opens the log file and erases its contents.
        """
        LogFile = open(self.HOMEDIR+"/.gEcrit/gEcrit.log", "w")
        LogFile.write("")
        LogFile.close()

    def ReadLog(self):
        """
        ReadLog

        Reads the log file and returns a string with its contents.
        """
        LogFile = open(self.HOMEDIR+"/.gEcrit/gEcrit.log", "r")
        logcontent = ""
        try:
            for line in LogFile.readlines():
                logcontent += line
        except:
            logcontent = ""

        return logcontent


Log = Logger()
