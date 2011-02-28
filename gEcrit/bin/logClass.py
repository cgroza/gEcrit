
#   Distributed under the terms of the GPL (GNU Public License)
#
#   gEcrit is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


#logClass.py


import os,sys
from configClass import *


class Logger():
    def AddLogEntry(self,entry):
        if Config.GetOption("ActLog"):
            LogFile = open("data/gEcrit.log","a")
            LogFile.write("\n")
            LogFile.write(entry)
            LogFile.close()
    
    
    def EraseLog(self,event):
        LogFile = open("data/gEcrit.log","w")
        LogFile.write("")
        LogFile.close()


    def ReadLog(self):
        LogFile = open("data/gEcrit.log","r")
        logcontent=""
        try:
            for line in LogFile.readlines():
                logcontent += line
        except: logcontent = ""

        return logcontent

Log = Logger()
