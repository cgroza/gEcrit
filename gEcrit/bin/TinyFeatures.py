
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

#TinyFeatures.py


import wx
from configClass import *


def AutoIndent(event,text_id):
    if Config.GetOption("Autoindentation") == True:
        key = event.GetKeyCode()
        cur_doc = wx.FindWindowById(text_id)
        if key == wx.WXK_NUMPAD_ENTER or key == wx.WXK_RETURN:
            line = cur_doc.GetCurrentLine()
            if cur_doc.GetLine(line-1)[-2] == ":":
                cur_doc.SetLineIndentation(line, cur_doc.GetLineIndentation(line-1)+cur_doc.GetIndent())
                cur_doc.LineEnd()
            else:
                cur_doc.SetLineIndentation(line, cur_doc.GetLineIndentation(line-1))
                cur_doc.LineEnd()

    event.Skip()


def OnUpdateUI(evt,text_id):
    # check for matching braces
    cur_doc = wx.FindWindowById(text_id)

    braceAtCaret = -1
    braceOpposite = -1
    charBefore = None
    caretPos = cur_doc.GetCurrentPos()

    if caretPos > 0:
        charBefore = cur_doc.GetCharAt(caretPos - 1)
        styleBefore = cur_doc.GetStyleAt(caretPos - 1)

    # check before
    if charBefore and chr(charBefore) in "[]{}()" and styleBefore == wx.stc.STC_P_OPERATOR:
        braceAtCaret = caretPos - 1

    # check after
    if braceAtCaret < 0:
        charAfter = cur_doc.GetCharAt(caretPos)
        styleAfter = cur_doc.GetStyleAt(caretPos)

        if charAfter and chr(charAfter) in "[]{}()" and styleAfter == wx.stc.STC_P_OPERATOR:
            braceAtCaret = caretPos

    if braceAtCaret >= 0:
        braceOpposite = cur_doc.BraceMatch(braceAtCaret)

    if braceAtCaret != -1  and braceOpposite == -1:
        cur_doc.BraceBadLight(braceAtCaret)
    else:
        cur_doc.BraceHighlight(braceAtCaret, braceOpposite)
        #pt = cur_doc.PointFromPosition(braceOpposite)
        #cur_doc.Refresh(True, wx.Rect(pt.x, pt.y, 5,5))
        #print pt
        #cur_doc.Refresh(True)

    evt.Skip()




def OnMarginClick(evt, text_id):
    # fold and unfold as needed
    cur_doc = wx.FindWindowById(text_id)
    if evt.GetMargin() == 2:
        if evt.GetShift() and evt.GetControl():
            FoldAll(text_id)
        else:
            lineClicked = cur_doc.LineFromPosition(evt.GetPosition())

            if cur_doc.GetFoldLevel(lineClicked) & wx.stc.STC_FOLDLEVELHEADERFLAG:
                if evt.GetShift():
                    cur_doc.SetFoldExpanded(lineClicked, True)
                    Expand(text_id,lineClicked, True, True, 1)
                elif evt.GetControl():
                    if cur_doc.GetFoldExpanded(lineClicked):
                       cur_doc.SetFoldExpanded(lineClicked, False)
                       Expand(text_id,lineClicked, False, True, 0)
                    else:
                        cur_doc.SetFoldExpanded(lineClicked, True)
                        Expand(text_id,lineClicked, True, True, 100)
                else:
                    cur_doc.ToggleFold(lineClicked)
    evt.Skip()



def FoldAll(text_id):
    cur_doc = wx.FindWindowById(text_id)
    lineCount = cur_doc.GetLineCount()
    expanding = True

    # find out if we are folding or unfolding
    for lineNum in range(lineCount):
         if cur_doc.GetFoldLevel(lineNum) & wx.stc.STC_FOLDLEVELHEADERFLAG:
             expanding = not cur_doc.GetFoldExpanded(lineNum)
             break

    lineNum = 0

    while lineNum < lineCount:
        level = cur_doc.GetFoldLevel(lineNum)
        if level & wx.stc.STC_FOLDLEVELHEADERFLAG and \
           (level & wx.stc.STC_FOLDLEVELNUMBERMASK) == wx.stc.STC_FOLDLEVELBASE:

            if expanding:
                cur_doc.SetFoldExpanded(lineNum, True)
                lineNum = Expand(text_id,lineNum, True)
                lineNum = lineNum - 1
            else:
                lastChild = cur_doc.GetLastChild(lineNum, -1)
                cur_doc.SetFoldExpanded(lineNum, False)

                if lastChild > lineNum:
                    cur_doc.HideLines(lineNum+1, lastChild)

        lineNum = lineNum + 1



def Expand(text_id,line, doExpand, force=False, visLevels=0, level=-1):
    cur_doc = wx.FindWindowById(text_id)
    lastChild = cur_doc.GetLastChild(line, level)
    line = line + 1

    while line <= lastChild:
        if force:
            if visLevels > 0:
                cur_doc.ShowLines(line, line)
            else:
                cur_doc.HideLines(line, line)
        else:
            if doExpand:
                cur_doc.ShowLines(line, line)

        if level == -1:
            level = cur_doc.GetFoldLevel(line)

        if level & wx.stc.STC_FOLDLEVELHEADERFLAG:
            if force:
                if visLevels > 1:
                    cur_doc.SetFoldExpanded(line, True)
                else:
                    cur_doc.SetFoldExpanded(line, False)

                line = Expand(text_id ,line, doExpand, force, visLevels-1)

            else:
                if doExpand and cur_doc.GetFoldExpanded(line):
                    line = Expand(text_id, line, True, force, visLevels-1)
                else:
                    line = Expand(text_id, line, False, force, visLevels-1)
        else:
            line = line + 1

    return line
