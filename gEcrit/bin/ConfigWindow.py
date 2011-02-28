
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


#ConfigWindow.py


import wx
from SyntaxHighlight import *
from configClass import *
from logClass import *
from SyntaxColor import *


def CallChangeOption(event,option, val,IdRange):
    Config.ChangeOption(option, val,IdRange)

def CallChangeColorFile(event, item, newcolor):
    ChangeColorFile(item, newcolor)
    event.Skip()

def DESTROYFrame(event,Frame):
    Frame.Close(True)
    event.Skip()

def ToggleSpinner(event,state,widget):
    if state == True:
        widget.Enable()
    else:
        widget.Disable()
    event.Skip()

class CfgFrame(wx.Frame):
    def __init__(self,IdRange,parent = None):
        wx.Frame.__init__(self,parent,-1,'Settings', size=(300,500))
        self.SetIcon(wx.Icon('icons/gEcrit.png', wx.BITMAP_TYPE_PNG))
        ConfigBook = wx.Notebook(self)

        ConfigPanel=wx.Panel(ConfigBook)
        ConfigPanel2 = wx.Panel(ConfigBook)
    ########First Tab
        ColPal.CollorPaletteWindow(0, IdRange)
        first_sizer = wx.BoxSizer(wx.VERTICAL)


        AutosaveBox = wx.CheckBox(ConfigPanel, -1, "Enable Autosave", (10,10), (160,-1))
        AutosaveBox.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption\
        (event,"Autosave",AutosaveBox.GetValue(),IdRange))
        AutosaveBox.Bind(wx.EVT_CHECKBOX, lambda event: ToggleSpinner\
        (event,AutosaveBox.GetValue(),Interval))

        Inter_Info = wx.StaticText(ConfigPanel, -1, "Save data each # of characters:", (20,35))

        Interval = wx.SpinCtrl(ConfigPanel, -1, "", (20,60), (90,-1))
        Interval.SetRange(1,500)
        Interval.SetValue(Config.GetOption("Autosave Interval"))
        Interval.Bind(wx.EVT_SPINCTRL, lambda event: CallChangeOption(event,\
         "Autosave Interval", Interval.GetValue(),IdRange))


        if not Config.GetOption("Autosave"):
            AutosaveBox.SetValue(False)
            Interval.Disable()
        else:
            AutosaveBox.SetValue(True)

        StatusBarBox = wx.CheckBox(ConfigPanel, -1, "Enable StatusBar", (10,90), (160,-1))
        StatusBarBox.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption\
        (event, "StatusBar",StatusBarBox.GetValue(),IdRange))

        StatusBarBox.SetValue(Config.GetOption("StatusBar"))


        Src_Br_Box = wx.CheckBox(ConfigPanel, -1, "Enable Source Browser", (10,115),(-1,-1))
        Src_Br_Box.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption\
        (event, "SourceBrowser", Src_Br_Box.GetValue(), IdRange))

        Src_Br_Box.SetValue(Config.GetOption("SourceBrowser"))

        FileTreeBox = wx.CheckBox(ConfigPanel, -1, "Enable File Tree Browser",(10,117),(-1,-1))
        FileTreeBox.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption\
        (event, "FileTree", FileTreeBox.GetValue(), IdRange))
        FileTreeBox.SetValue(Config.GetOption("FileTree"))

        SpellBox = wx.CheckBox(ConfigPanel,-1,"Enable Spell Checker",(10,120),(-1,-1))
        SpellBox.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption\
        (event,"SpellCheck",SpellBox.GetValue(),IdRange))
        SpellBox.SetValue(Config.GetOption("SpellCheck"))

        SpellBox.Bind(wx.EVT_CHECKBOX, lambda event: ToggleSpinner\
        (event,SpellBox.GetValue(),SpellSugBox))


        SpellSugBox = wx.CheckBox(ConfigPanel,-1,"Show Spell Suggestions",(10,120),(-1,-1))
        SpellSugBox.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption\
        (event,"SpellSuggestions",SpellSugBox.GetValue(),IdRange))
        SpellSugBox.SetValue(Config.GetOption("SpellSuggestions"))


        LogActBox = wx.CheckBox(ConfigPanel, -1, "Enable Log", (10,140), (160,-1))
        LogActBox.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption\
        (event, "ActLog", LogActBox.GetValue(),IdRange))

        LogActBox.SetValue(Config.GetOption("ActLog"))


        PalleteButton = wx.Button(ConfigPanel,-1, "Colour Palette",pos=(10,220), size=(-1,-1))
        PalleteButton.Bind(wx.EVT_BUTTON, ColPal.ShowMe )

        DefaultsButton =wx.Button(ConfigPanel, -1, "Reset to Defaults", pos = (10,260), size = (-1,-1))
        DefaultsButton.Bind(wx.EVT_BUTTON, lambda event: CallChangeOption(event,"Defaults","Defaults",IdRange))
        DefaultsButton.Bind(wx.EVT_BUTTON, lambda event: CallChangeColorFile(event,"Defaults","Defaults"))

        ViewButton = wx.Button(ConfigPanel,label="View Log",pos=(10,180),size=(-1,-1))
        ViewButton.Bind(wx.EVT_BUTTON, self.viewLog)

        EraseButton = wx.Button(ConfigPanel,label="Erase Log",pos=(50,180),size=(-1,-1))
        EraseButton.Bind(wx.EVT_BUTTON, Log.EraseLog)
        EraseButton.Bind(wx.EVT_BUTTON, lambda event :ToggleSpinner(event, False, EraseButton))

        OKButton = wx.Button(ConfigPanel, -1, "OK", pos = (200,420), size=(80,40))
        OKButton.Bind(wx.EVT_CLOSE, self.HideMe)
        OKButton.Bind(wx.EVT_BUTTON, self.HideMe)

        special_sizer = wx.BoxSizer(wx.HORIZONTAL)
        special_sizer.Add(ViewButton,0)
        special_sizer.Add(EraseButton,0)

        first_sizer.Add(AutosaveBox,0,wx.EXPAND,wx.ALL,5)
        first_sizer.Add(Inter_Info,0,wx.ALL,5)
        first_sizer.Add(Interval,0,wx.LEFT,30 )
        first_sizer.Add(StatusBarBox,0,wx.EXPAND,wx.ALL,5 )
        first_sizer.Add(Src_Br_Box,0,wx.EXPAND,wx.ALL,5 )
        first_sizer.Add(FileTreeBox,0,wx.EXPAND,wx.ALL,5)
        first_sizer.Add(SpellBox,0,wx.EXPAND,wx.ALL,5 )
        first_sizer.Add(SpellSugBox,0,wx.EXPAND,wx.ALL,15)
        first_sizer.Add(LogActBox,0,wx.EXPAND,wx.ALL,5 )
        first_sizer.Add(PalleteButton,0,wx.ALL,5 )
        first_sizer.Add(special_sizer,0,wx.ALL,5 )

        first_sizer.Add(DefaultsButton,0)
        ConfigPanel.SetSizer(first_sizer)

    ################Second Tab

        second_sizer = wx.BoxSizer(wx.VERTICAL)
        LineNrBox = wx.CheckBox(ConfigPanel2, -1, "Show Line Numbers", (10,10), (-1,-1))
        LineNrBox.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption\
        (event, "LineNumbers",LineNrBox.GetValue(),IdRange))
        LineNrBox.SetValue(Config.GetOption("LineNumbers"))


        SyntaxHgBox = wx.CheckBox(ConfigPanel2, -1, "Syntax Highlight ", (10,35), (-1,-1))
        SyntaxHgBox.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption\
        (event, "SyntaxHighlight",SyntaxHgBox.GetValue(),IdRange))
        SyntaxHgBox.SetValue(Config.GetOption("SyntaxHighlight"))


        AutoIdentBox = wx.CheckBox(ConfigPanel2, -1, "Autoindentation", (10,60), (-1,-1))
        AutoIdentBox.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption\
        (event, "Autoindentation",AutoIdentBox.GetValue(),IdRange))
        AutoIdentBox.Bind(wx.EVT_CHECKBOX, lambda event: ToggleSpinner\
        (event,AutoIdentBox.GetValue(),IndentSizeBox))
        AutoIdentBox.SetValue(Config.GetOption("Autoindentation"))



        IndentSizeBox = wx.SpinCtrl(ConfigPanel2, -1,"",(35,85), (90,-1))
        IndentSizeBox.SetRange(1,12)
        IndentSizeBox.SetValue(Config.GetOption("IndentSize"))

        IndentSizeBox.Bind(wx.EVT_SPINCTRL, lambda event: CallChangeOption\
        (event,"IndentSize",IndentSizeBox.GetValue(),IdRange))

        if Config.GetOption("Autoindentation") == True:
            IndentSizeBox.Enable()
        else:
            IndentSizeBox.Disable()


        IndentationGuidesBox = wx.CheckBox(ConfigPanel2, -1, "Indentation Guides", (10,110), (-1,-1))

        IndentationGuidesBox.SetValue(Config.GetOption("IndetationGuides"))


        IndentationGuidesBox.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption\
        (event,"IndetationGuides",IndentationGuidesBox.GetValue(),IdRange))

        BackSpaceUnindentBox = wx.CheckBox(ConfigPanel2, -1, "Backspace to Unindent",(10,135), (-1,-1))
        BackSpaceUnindentBox.SetValue(Config.GetOption("BackSpaceUnindent"))


        BackSpaceUnindentBox.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption\
        (event,"BackSpaceUnindent",BackSpaceUnindentBox.GetValue(),IdRange))

        WhitespaceBox = wx.CheckBox(ConfigPanel2, -1, "Show Whitespace", (10,160), (-1,-1))
        WhitespaceBox.SetValue(Config.GetOption("Whitespace"))


        WhitespaceBox.Bind(wx.EVT_CHECKBOX,lambda event: CallChangeOption\
        (event,"Whitespace",WhitespaceBox.GetValue(),IdRange))

        UseTabsBox = wx.CheckBox(ConfigPanel2, -1, "Use Tabs", (10,185), (160,-1))
        UseTabsBox.SetValue(Config.GetOption("UseTabs"))

        UseTabsBox.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption\
        (event, "UseTabs", UseTabsBox.GetValue(),IdRange))

        CarretInfo = wx.StaticText(ConfigPanel2, -1, 'Carret Width:', (10, 210))


        CarretWidthSpin = wx.SpinCtrl(ConfigPanel2, -1, "", (35,235), (-1,-1))
        CarretWidthSpin.SetRange(1,20)
        CarretWidthSpin.SetValue(Config.GetOption("CarretWidth"))
        CarretWidthSpin.Bind(wx.EVT_SPINCTRL, lambda event: CallChangeOption\
        (event,"CarretWidth",CarretWidthSpin.GetValue(),IdRange))

        FoldMarkBox =  wx.CheckBox(ConfigPanel2, -1, "Fold Marks", (10,265), (160,-1))
        FoldMarkBox.Bind(wx.EVT_CHECKBOX,lambda event: CallChangeOption\
        (event,"FoldMarks",FoldMarkBox.GetValue(),IdRange))
        FoldMarkBox.SetValue(Config.GetOption("FoldMarks"))

        TabInfo = wx.StaticText(ConfigPanel2, -1, "Tab Width:", pos = (10,300), size=(-1,-1))
        TabWidthBox = wx.SpinCtrl(ConfigPanel2, -1,"",pos= (35,320), size=(90,-1))

        TabWidthBox.SetValue(Config.GetOption("TabWidth"))

        TabWidthBox.Bind(wx.EVT_SPINCTRL, lambda event: CallChangeOption\
        (event, "TabWidth", TabWidthBox.GetValue(), IdRange))

        EdgeLineBox = wx.CheckBox(ConfigPanel2,-1,"Edge Line", pos = (10,350), size =(-1,-1))
        EdgeLineBox.SetValue(Config.GetOption("EdgeLine"))
        EdgeLineBox.Bind(wx.EVT_CHECKBOX, lambda event: CallChangeOption\
        (event, "EdgeLine",EdgeLineBox.GetValue(),IdRange))

        EdgeLineBox.Bind(wx.EVT_CHECKBOX, lambda event: ToggleSpinner(event,EdgeLineBox.GetValue()\
        ,EdgeLinePos))

        EdgeInfo = wx.StaticText(ConfigPanel2, -1,"Edge Line Position:", pos = (35, 375), size = (-1,-1))

        EdgeLinePos = wx.SpinCtrl(ConfigPanel2, -1, "", pos = (35,400), size = (-1,-1))
        EdgeLinePos.SetValue(Config.GetOption("EdgeColumn"))

        if Config.GetOption("EdgeLine"):
            EdgeLinePos.Enable()
        else:
            EdgeLinePos.Disable()

        EdgeLinePos.Bind(wx.EVT_SPINCTRL, lambda event: CallChangeOption\
        (event, "EdgeColumn", EdgeLinePos.GetValue(), IdRange))

        second_sizer.Add(LineNrBox,0,wx.EXPAND)
        second_sizer.Add(SyntaxHgBox,0,wx.EXPAND)
        second_sizer.Add(AutoIdentBox,0,wx.EXPAND)
        second_sizer.Add(IndentSizeBox,0,wx.LEFT,30)
        second_sizer.Add(IndentationGuidesBox,0,wx.EXPAND)
        second_sizer.Add(BackSpaceUnindentBox,0,wx.EXPAND)
        second_sizer.Add(WhitespaceBox,0,wx.EXPAND)
        second_sizer.Add(UseTabsBox,0,wx.EXPAND,30)
        second_sizer.Add(CarretInfo,0,wx.EXPAND,)
        second_sizer.Add(CarretWidthSpin,0,wx.LEFT,30)
        second_sizer.Add(FoldMarkBox,0,wx.EXPAND)
        second_sizer.Add(TabInfo,0,wx.EXPAND)
        second_sizer.Add(TabWidthBox,0,wx.LEFT,30)
        second_sizer.Add(EdgeLineBox,0,wx.EXPAND)
        second_sizer.Add(EdgeInfo,0,wx.EXPAND)
        second_sizer.Add(EdgeLinePos,0,wx.LEFT,30)


        ConfigPanel2.SetSizer(second_sizer)


        OKButton2 = wx.Button(ConfigPanel2, -1, "OK", pos = (200,420), size=(80,40))
        OKButton2.Bind(wx.EVT_CLOSE, self.HideMe)
        OKButton2.Bind(wx.EVT_BUTTON, self.HideMe)



    #########Third Tab

        third_sizer = wx.BoxSizer(wx.VERTICAL)

        ConfigPanel3 = wx.Panel(ConfigBook)
        BashBox = wx.CheckBox(ConfigPanel3, -1, "OS Terminal", pos= (10,10), size = (-1,-1))
        BashBox.Bind(wx.EVT_CHECKBOX,lambda event: CallChangeOption(event,"BashShell",BashBox.GetValue(), IdRange))
        BashBox.Bind(wx.EVT_CHECKBOX, lambda event: ToggleSpinner(event, BashBox.GetValue(), OSPath))

        BashBox.SetValue(Config.GetOption("BashShell"))

        OSInfo = wx.StaticText(ConfigPanel3,-1,"OS shell path:", pos=(10,30), size=(-1,-1))

        OSPath = wx.TextCtrl(ConfigPanel3,-1,"", pos = (10,50), size = (250,-1))
        OSPath.SetValue(Config.GetOption("OSPath"))
        OSPath.Enable(BashBox.GetValue())

        OSApply = wx.Button(ConfigPanel3, -1, "Apply", pos=(10,80), size = (-1,-1))
        OSApply.Bind(wx.EVT_BUTTON,lambda event: CallChangeOption(event, "OSPath",OSPath.GetValue(), IdRange))

        PythonBox = wx.CheckBox(ConfigPanel3, -1, "Python Terminal", pos= (10,110), size = (-1,-1))
        PythonBox.Bind(wx.EVT_CHECKBOX,lambda event: CallChangeOption(event,"PythonShell",PythonBox.GetValue(),IdRange))
        PythonBox.Bind(wx.EVT_CHECKBOX, lambda event: ToggleSpinner(event, PythonBox.GetValue(), PyPath))
        PythonBox.SetValue(Config.GetOption("PythonShell"))

        PyInfo = wx.StaticText(ConfigPanel3,-1,"Python shell path:", pos=(10,130), size=(-1,-1))

        PyPath = wx.TextCtrl(ConfigPanel3, -1, "", pos=(10,150), size=(250,-1))
        PyPath.SetValue(Config.GetOption("PyPath"))
        PyPath.Enable(PythonBox.GetValue())

        PyApply = wx.Button(ConfigPanel3, -1, "Apply", pos=(10,180), size = (-1,-1))
        PyApply.Bind(wx.EVT_BUTTON,lambda event: CallChangeOption(event, "PyPath",PyPath.GetValue(), IdRange))

        third_sizer.Add(BashBox,0,wx.EXPAND,5)
        third_sizer.Add(OSInfo,0,wx.EXPAND,5)
        third_sizer.Add(OSPath,0,wx.EXPAND,5)
        third_sizer.Add(OSApply,0,5)
        third_sizer.Add(PythonBox,0,wx.EXPAND,5)
        third_sizer.Add(PyInfo,0,wx.EXPAND,5)
        third_sizer.Add(PyPath,0,wx.EXPAND,5)
        third_sizer.Add(PyApply,0,5)

        ConfigPanel3.SetSizer(third_sizer)

        OKButton4 = wx.Button(ConfigPanel3,-1,"OK", pos = (200,420), size=(80,40))
        OKButton4.Bind(wx.EVT_BUTTON, self.HideMe)

        ConfigBook.AddPage(ConfigPanel, "General")
        ConfigBook.AddPage(ConfigPanel2, "Editor")
        ConfigBook.AddPage(ConfigPanel3, "Terminals")
        self.Bind(wx.EVT_CLOSE, self.HideMe)

        self.Hide()
        self.Centre()

    def ShowMe(self,event):
        self.Show(True)
    def HideMe(self,event):
        self.Hide()

    def viewLog(self,event):
        logcontent = ""
        if Config.GetOption("ActLog") == True:

            logFrame = wx.Frame(None,-1, 'View Log', size=(500, 500))
            panel5 = wx.Panel(logFrame)
            data = wx.richtext.RichTextCtrl(panel5, pos = (0,0),size = (500,500))
            data.AppendText(Log.ReadLog())
            logFrame.Centre()
            logFrame.Show()



        else:
            inform = wx.MessageDialog(None, "The Log is disabled!\
            \nEnable it to view.", "Log Status",wx.OK)
            inform.ShowModal()
