
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


#PrintDialog.py


import  wx.html
import wx

class PrettyPrinter(wx.html.HtmlEasyPrinting):

    def __init__(self,filename, text_id, parent = None):
            wx.html.HtmlEasyPrinting.__init__(self)
            self.parent = parent

            data = wx.PrintDialogData()

            data.EnableSelection(True)
            data.EnablePrintToFile(True)
            data.EnablePageNumbers(True)
            data.SetMinPage(1)
            data.SetMaxPage(5)
            data.SetAllPages(True)


            dlg = wx.PrintDialog(parent, data)

            #if dlg.ShowModal() == wx.ID_OK:
            #    data = dlg.GetPrintDialogData()
                #self.log.WriteText('GetAllPages: %d\n' % data.GetAllPages())

            dlg.Destroy()
            cur_doc= wx.FindWindowById(text_id)
            content = cur_doc.GetText()
            linenumbers = cur_doc.GetLineCount()
            self.DoPrint(content, filename, linenumbers)


    def DoPrint(self,text, filename, linenumbers = 1):
        self.SetHeader(filename)
        self.PrintText(self.ToHTML(text, linenumbers), filename)



    #FROM DRPYTHON SOURCE CODE.
    def ToHTML(self,text, linenumbers):
            text = text.replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;")
            #Line numbers:
            if linenumbers:
                text = "1<a href=\"#\">00000</a>" + text.replace(' ', " &nbsp;")
                x = 0
                l = len(text)
                line = 2
                n = ""
                while x < l:
                    if text[x] == '\n':
                        n = n + "\n" + str(line)
                        if line < 10:
                            n = n + "<a href=\"#\">00000</a>"
                        elif line < 100:
                            n = n + "<a href=\"#\">0000</a>"
                        elif line < 1000:
                            n = n + "<a href=\"#\">000</a>"
                        else:
                            n = n + "<a href=\"#\">00</a>"
                        line = line + 1
                    else:
                        n = n + text[x]
                    x = x + 1

                text = n

            #htmlify the text:
            thehtml = "<html><body link=\"#FFFFFF\" vlink=\"#FFFFFF\" alink=\"#FFFFFF\">" \
            + text.replace('\n', "\n<br>") \
            + "</span></body></html>"
            return thehtml
