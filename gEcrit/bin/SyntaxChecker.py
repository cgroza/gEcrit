
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


#SyntaxChecker.py


import wx
#From drPython source code.
class SyntaxDoctor():
    def CheckSyntax(self,event, text_id):
        cur_doc = wx.FindWindowById(text_id)
        file_nm = cur_doc.SaveTarget
        print file_nm
        #Check Syntax First
        try:

            ctext = cur_doc.GetText()
            ctext = ctext.replace('\r\n', '\n').replace('\r', '\n')
            compile(ctext, file_nm, 'exec')
            say_ok = wx.MessageDialog(None,"No errors have been detected.","Syntax Check")
            if say_ok.ShowModal() == wx.ID_OK: say_ok.Destroy()

        except Exception, e:
            ln_num = ""
            excstr = str(e)
            try:
                for c in exctr:
                    if int(c):
                        ln_num+=str(c)
                n = int(ln_num)

                cur_doc.ScrollToLine(n)
                cur_doc.GotoLine(n)
            except:
                say_error = wx.MessageDialog(None,'Error:'+excstr, 'Error Found')
                if say_error.ShowModal() == wx.ID_OK: say_error.Destroy()

        #~ #Now Check Indentation
        #~ result = drTabNanny.Check(fn)
        #~ results = result.split()
        #~ if len(results) > 1:
            #~ num = results[1]
            #~ try:
                #~ n = int(num) - 1
                #~ self.setDocumentTo(docnumber)
                #~ self.txtDocument.ScrollToLine(n)
                #~ self.txtDocument.GotoLine(n)
                #~ self.ShowMessage('tabnanny:\n' + result)
                #~ self.txtDocument.SetSTCFocus(True)
                #~ self.txtDocument.SetFocus()
                #~ return False
            #~ except:
                #~ self.ShowMessage('Line Number Error:\n\n'+result, 'TabNanny Trouble')
#~
        #~ return True

SyntaxDoc = SyntaxDoctor()
