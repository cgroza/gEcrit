
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


#FindReplaceText.py


import wx

class SearchReplace:
    def FindDocText(self,text_id):

        self.min_text_range = 0
        self.max_text_range = wx.FindWindowById(text_id).GetLength()
        FindFrame = wx.Frame(None, -1,"Search", size=(200,200))
        FindData = wx.FindReplaceData()
        FindDialog = wx.FindReplaceDialog(FindFrame, FindData, "Find")
        FindDialog.FindData = FindData  # save a reference to it...
        FindDialog.Bind(wx.EVT_FIND_NEXT, lambda event: self.SearchWord(event, text_id, FindData))
        FindDialog.Bind(wx.EVT_FIND , lambda event: self.SearchWord(event,text_id, FindData))
        FindDialog.Show(True)


    def SearchWord(self,event,text_id, item):

        cur_doc = wx.FindWindowById(text_id)
        search_flags = item.GetFlags()
        word = item.GetFindString()
        max_pos = cur_doc.GetLength()
        if search_flags in [0,2,4,6]:
            text_pos = cur_doc.FindText(self.max_text_range,self.min_text_range,word,search_flags)
            if text_pos != -1:
                start_pos = text_pos
                end_pos=start_pos+len(word)
                self.max_text_range=text_pos-len(word)
                cur_doc.GotoPos(self.max_text_range)
                cur_doc.SetSelection(end_pos,start_pos)
            elif text_pos == -1:
                cur_doc.GotoPos(1)
                self.min_text_range = 0

        else:
            text_pos=cur_doc.FindText(self.min_text_range,max_pos,word,search_flags)
            start_pos = text_pos
            end_pos = text_pos+len(word)

            if text_pos != -1:
                cur_doc.GotoPos(text_pos)
                self.min_text_range =  end_pos
                cur_doc.SetSelection(start_pos, end_pos)
            elif text_pos == -1:
                cur_doc.GotoPos(1)
                self.min_text_range = 0



    def ReplaceDocText(self,text_id ):

        self.max_text_range = wx.FindWindowById(text_id).GetLength()
        self.min_text_range = 1
        FdRpFrame = wx.Frame(None, -1, "Search and Replace", size = (300,300) )
        FdRpData = wx.FindReplaceData()
        ReplaceDialog = wx.FindReplaceDialog(FdRpFrame,FdRpData, "Search and Replace",\
        style = wx.FR_REPLACEDIALOG)
        ReplaceDialog.FdRpData = FdRpData
        ReplaceDialog.Bind(wx.EVT_FIND_NEXT, lambda event: self.SearchWord(event, text_id, FdRpData))
        ReplaceDialog.Bind(wx.EVT_FIND , lambda event: self.SearchWord(event,text_id, FdRpData))

        ReplaceDialog.Bind( wx.EVT_FIND_REPLACE ,lambda event: self.ReplaceWord(event, text_id, FdRpData ))
        ReplaceDialog.Bind(wx.EVT_FIND_REPLACE_ALL, lambda event: self.ReplaceAllWords(event,text_id,FdRpData))
        ReplaceDialog.Show()


    def ReplaceWord(self,event,text_id, item):

        cur_doc = wx.FindWindowById(text_id)
        max_pos = cur_doc.GetLength()
        op_flags= item.GetFlags()

        search_word = item.GetFindString()
        replace_word = item.GetReplaceString()
        if op_flags in [0,2,4,6]:
            to_pos = cur_doc.FindText(self.max_text_range,self.min_text_range,search_word,op_flags)
            from_pos = to_pos+len(search_word)
            cur_doc.SetTargetStart(to_pos)
            cur_doc.SetTargetEnd(from_pos)
            print from_pos
            print to_pos
            if from_pos != -1:
                cur_doc.ReplaceTarget(replace_word)
                self.max_text_range = to_pos
                cur_doc.GotoPos(to_pos)
                cur_doc.SetSelection(to_pos,from_pos)
                return to_pos

            elif from_pos == -1:
                self.max_text_range = cur_doc.GetLength()
                return -1

        else:
            from_pos = cur_doc.FindText(self.min_text_range,max_pos,search_word ,op_flags)
            to_pos = from_pos + len(search_word)
            cur_doc.SetTargetStart(from_pos)
            cur_doc.SetTargetEnd(to_pos)
            if from_pos != -1:
                cur_doc.ReplaceTarget(replace_word)
                self.min_text_range = to_pos
                cur_doc.GotoPos(from_pos)
                cur_doc.SetSelection(to_pos,from_pos)
                return from_pos
            elif from_pos == -1:
                self.min_text_range = 0
                return -1



    def ReplaceAllWords(self,event,text_id,item):
        while self.ReplaceWord(0,text_id,item) != -1:
            self.ReplaceWord(0,text_id,item)
        EndReached = wx.MessageDialog(None,"The end of file was reached!\nNothing to replace.","", style=wx.OK)
        EndReached.ShowModal()


FindRepl = SearchReplace()
