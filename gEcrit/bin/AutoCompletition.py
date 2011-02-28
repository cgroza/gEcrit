
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


#AutoCompletition.py


import wx, keyword, difflib, re

class AutoComplet:
    def __init__(self):
        self.replace_dic = {"\n":" ",".":" ",",":" ",")":" ","(":" ","]":" ","[":" "\
        ,"{": " ", "}":" ","\"":" ", "'":" ",";":" ",":":" "}
        self.pattern = re.compile('\W')


    def CreateCompList(self,text):
        text = re.sub(self.pattern, ' ', text)

        split_text = text.split(" ")

        return list(set(split_text))

    def OnKeyPressed(self,event, text_id):
            cur_doc = wx.FindWindowById(text_id)
            cur_doc.AutoCompSetIgnoreCase(False)
            if cur_doc.CallTipActive():
                cur_doc.CallTipCancel()
            key = event.GetKeyCode()

            if key == 32 and event.ControlDown():
                pos = cur_doc.GetCurrentPos()
                word_start = cur_doc.WordStartPosition(pos, True)
                content = cur_doc.GetText()
                word = cur_doc.GetTextRange(word_start,pos)

                lst = difflib.get_close_matches(word, self.CreateCompList(content), 5)

                try:
                    del lst[0]
                except: pass

                st = " ".join(lst)#.strip(word)

                if st != "":
                    cur_doc.AutoCompShow(pos-word_start, st)

            event.Skip()

AutoComp = AutoComplet()
