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

import os
import sys
import time
from Configuration import *



class Logger:
    """
    Logger

    Provides function to record applications activity, view the log, and
    erasing it.
    """
    def __init__(self):
        self.__HOMEDIR = os.path.expanduser('~')
        self.log_path = os.path.join(self.__HOMEDIR, ".gEcrit", "gEcrit.log")

    def AddLogEntry(self, entry):
        """
        AddLogEntry

        Opens the log file and appends a string with
        the format date,time : string to it.
        The string is received from its argument.
        """
        if Config.GetOption("ActLog"):
            log_file = open(self.log_path, "a")
            log_file.write("\n")
            log_file.write(time.ctime() + " : "+ entry)
            log_file.close()

    def EraseLog(self, event):
        """
        EraseLog

        Opens the log file and erases its contents.
        """
        log_file = open(self.log_path, "w")
        log_file.write("")
        log_file.close()

    def ReadLog(self):
        """
        ReadLog

        Reads the log file and returns a string with its contents.
        """
        log_file = open(self.log_path, "r")
        logcontent = ""
        try:
            for line in log_file.readlines():
                logcontent += line
        except:
            logcontent = ""
        finally:
            log_file.close()

        return logcontent


Log = Logger()
