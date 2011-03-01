#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import pty
import threading
import select
import wx

import fcntl
import termios
import struct
import tty

import TermEmulator


class ShellEmulator(wx.TextCtrl):

    def __init__(self, parent, path_to_shell, ID_TERMINAL):
        self.parent = parent
        wx.TextCtrl.__init__(self, parent, ID_TERMINAL, pos=(0, 0), size=
                             (100, 100), style=wx.TE_MULTILINE | wx.RESIZE_BORDER)

        font = wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,
                       wx.FONTSTYLE_NORMAL, False)
        self.SetFont(font)

        self.Bind(wx.EVT_CHAR, self.OnTerminalChar, id=ID_TERMINAL)

        self.Bind(wx.EVT_KEY_DOWN, self.OnTerminalKeyDown, id=
                  ID_TERMINAL)

        self.Bind(wx.EVT_KEY_UP, self.OnTerminalKeyUp, id=ID_TERMINAL)

        self.termRows = 24
        self.termCols = 80

        self.FillScreen()

        self.linesScrolledUp = 0
        self.scrolledUpLinesLen = 0

        self.termEmulator = TermEmulator.V102Terminal(self.termRows,
                self.termCols)
        self.termEmulator.SetCallback(self.termEmulator.CALLBACK_SCROLL_UP_SCREEN,
                self.OnTermEmulatorScrollUpScreen)
        self.termEmulator.SetCallback(self.termEmulator.CALLBACK_UPDATE_LINES,
                self.OnTermEmulatorUpdateLines)
        self.termEmulator.SetCallback(self.termEmulator.CALLBACK_UPDATE_CURSOR_POS,
                self.OnTermEmulatorUpdateCursorPos)
        self.termEmulator.SetCallback(self.termEmulator.CALLBACK_UPDATE_WINDOW_TITLE,
                self.OnTermEmulatorUpdateWindowTitle)
        self.termEmulator.SetCallback(self.termEmulator.CALLBACK_UNHANDLED_ESC_SEQ,
                self.OnTermEmulatorUnhandledEscSeq)

        self.isRunning = False

        self.UpdateUI()

    def OnTerminalKeyDown(self, event):

        event.Skip()

    def OnTerminalKeyUp(self, event):

        event.Skip()

    def OnTerminalChar(self, event):
        if not self.isRunning:
            return

        ascii = event.GetKeyCode()

        keystrokes = None

        if ascii < 256:
            keystrokes = chr(ascii)
        elif ascii == wx.WXK_UP:
            keystrokes = "\033[A"
        elif ascii == wx.WXK_DOWN:
            keystrokes = "\033[B"
        elif ascii == wx.WXK_RIGHT:
            keystrokes = "\033[C"
        elif ascii == wx.WXK_LEFT:
            keystrokes = "\033[D"

        if keystrokes != None:

            os.write(self.processIO, keystrokes)

    def OnTermEmulatorScrollUpScreen(self):
        blankLine = "\n"

        for i in range(self.termEmulator.GetCols()):
            blankLine += ' '

        lineLen = self.termCols
        self.AppendText(blankLine)
        self.linesScrolledUp += 1
        self.scrolledUpLinesLen += lineLen + 1

    def OnTermEmulatorUpdateLines(self):
        self.UpdateDirtyLines()
        wx.YieldIfNeeded()

    def OnTermEmulatorUpdateCursorPos(self):
        self.UpdateCursorPos()

    def OnTermEmulatorUpdateWindowTitle(self, title):

        pass

    def OnTermEmulatorUnhandledEscSeq(self, escSeq):
        print "Unhandled escape sequence: [" + escSeq

    def FillScreen(self):
        """
        Fills the screen with blank lines so that we can update terminal
        dirty lines quickly.
        """

        text = ""
        for i in range(self.termRows):
            for j in range(self.termCols):
                text += ' '
            text += "\n"

        text = text.rstrip("\n")
        self.SetValue(text)

    def UpdateUI(self):

        self.Enable(self.isRunning)

    def OnRun(self, event, path_to_shell):
        path = path_to_shell  #self.tc1.GetValue()
        basename = os.path.expanduser('~')
        arglist = [basename]

        arguments = ""  #self.tc2.GetValue()
        if arguments != "":
            for arg in arguments.split(' '):
                arglist.append(arg)

        self.termRows = 24  #int(self.tc3.GetValue())
        self.termCols = 80  #int(self.tc4.GetValue())

        (rows, cols) = self.termEmulator.GetSize()
        if rows != self.termRows or cols != self.termCols:
            self.termEmulator.Resize(self.termRows, self.termCols)

        (processPid, processIO) = pty.fork()
        if processPid == 0:  # child process
            os.execl(path, basename)

        print "Child process pid", processPid

        fcntl.ioctl(processIO, termios.TIOCSWINSZ, struct.pack("hhhh",
                    self.termRows, self.termCols, 0, 0))

        tcattrib = termios.tcgetattr(processIO)
        tcattrib[3] = tcattrib[3] & ~termios.ICANON
        termios.tcsetattr(processIO, termios.TCSAFLUSH, tcattrib)

        self.processPid = processPid
        self.processIO = processIO
        self.processOutputNotifierThread = threading.Thread(target=self.__ProcessOuputNotifierRun)
        self.waitingForOutput = True
        self.stopOutputNotifier = False
        self.processOutputNotifierThread.start()
        self.isRunning = True
        self.UpdateUI()

    def __ProcessOuputNotifierRun(self):
        inpSet = [self.processIO]
        while not self.stopOutputNotifier and self.__ProcessIsAlive():
            if self.waitingForOutput:
                (inpReady, outReady, errReady) = select.select(inpSet, [],
                        [], 1)
                if self.processIO in inpReady:
                    self.waitingForOutput = False
                    wx.CallAfter(self.ReadProcessOutput)

        if not self.__ProcessIsAlive():
            self.isRunning = False
            wx.CallAfter(self.ReadProcessOutput)
            wx.CallAfter(self.UpdateUI)
            print "Process exited"

        print "Notifier thread exited"

    def __ProcessIsAlive(self):
        try:
            (pid, status) = os.waitpid(self.processPid, os.WNOHANG)
            if pid == self.processPid and os.WIFEXITED(status):
                return False
        except:
            return False

        return True

    def ReadProcessOutput(self):
        output = ""

        try:
            while True:
                data = os.read(self.processIO, 512)
                datalen = len(data)
                output += data

                if datalen < 512:
                    break
        except:
            output = ""

        self.termEmulator.ProcessInput(output)

        self.SetForegroundColour((0, 0, 0))
        self.SetBackgroundColour((255, 255, 255))

        self.waitingForOutput = True

    def UpdateDirtyLines(self, dirtyLines=None):
        text = ""
        curStyle = 0
        curFgColor = 0
        curBgColor = 0

        self.SetTerminalRenditionForeground(curFgColor)
        self.SetTerminalRenditionBackground(curBgColor)

        screen = self.termEmulator.GetRawScreen()
        screenRows = self.termEmulator.GetRows()
        screenCols = self.termEmulator.GetCols()
        if dirtyLines == None:
            dirtyLines = self.termEmulator.GetDirtyLines()

        disableTextColoring = False  #self.cb1.IsChecked()

        for row in dirtyLines:
            text = ""

            lineNo = self.linesScrolledUp + row
            lineStart = self.GetTextCtrlLineStart(lineNo)

            lineEnd = lineStart + self.termCols

            self.Replace(lineStart, lineEnd, "")
            self.SetInsertionPoint(lineStart)

            for col in range(screenCols):
                (style, fgcolor, bgcolor) = self.termEmulator.GetRendition(row,
                        col)

                if not disableTextColoring and (curStyle != style or
                        curFgColor != fgcolor or curBgColor != bgcolor):

                    if text != "":
                        self.WriteText(text)
                        text = ""

                    if curStyle != style:
                        curStyle = style

                        if style == 0:
                            self.SetForegroundColour((0, 0, 0))
                            self.SetBackgroundColour((255, 255, 255))
                        elif style & self.termEmulator.RENDITION_STYLE_INVERSE:
                            self.SetForegroundColour((255, 255, 255))
                            self.SetBackgroundColour((0, 0, 0))
                        else:

                            pass

                    if curFgColor != fgcolor:
                        curFgColor = fgcolor

                        self.SetTerminalRenditionForeground(curFgColor)

                    if curBgColor != bgcolor:
                        curBgColor = bgcolor

                        self.SetTerminalRenditionBackground(curBgColor)

                text += screen[row][col]

            self.WriteText(text)

    def SetTerminalRenditionForeground(self, fgcolor):
        if fgcolor != 0:
            if fgcolor == 1:
                self.SetForegroundColour((0, 0, 0))
            elif fgcolor == 2:
                self.SetForegroundColour((255, 0, 0))
            elif fgcolor == 3:
                self.SetForegroundColour((0, 255, 0))
            elif fgcolor == 4:
                self.SetForegroundColour((255, 255, 0))
            elif fgcolor == 5:
                self.SetForegroundColour((0, 0, 255))
            elif fgcolor == 6:
                self.SetForegroundColour((255, 0, 255))
            elif fgcolor == 7:
                self.SetForegroundColour((0, 255, 255))
            elif fgcolor == 8:
                self.SetForegroundColour((255, 255, 255))
        else:
            self.SetForegroundColour((0, 0, 0))

    def SetTerminalRenditionBackground(self, bgcolor):
        if bgcolor != 0:
            if bgcolor == 1:
                self.SetBackgroundColour((0, 0, 0))
            elif bgcolor == 2:
                self.SetBackgroundColour((255, 0, 0))
            elif bgcolor == 3:
                self.SetBackgroundColour((0, 255, 0))
            elif bgcolor == 4:
                self.SetBackgroundColour((255, 255, 0))
            elif bgcolor == 5:
                self.SetBackgroundColour((0, 0, 255))
            elif bgcolor == 6:
                self.SetBackgroundColour((255, 0, 255))
            elif bgcolor == 7:
                self.SetBackgroundColour((0, 255, 255))
            elif bgcolor == 8:
                self.SetBackgroundColour((255, 255, 255))
        else:
            self.SetBackgroundColour((255, 255, 255))

    def GetTextCtrlLineStart(self, lineNo):
        lineStart = self.scrolledUpLinesLen
        lineStart += (self.termCols + 1) * (lineNo - self.linesScrolledUp)
        return lineStart

    def UpdateCursorPos(self):
        (row, col) = self.termEmulator.GetCursorPos()

        lineNo = self.linesScrolledUp + row
        insertionPoint = self.GetTextCtrlLineStart(lineNo)
        insertionPoint += col
        self.SetInsertionPoint(insertionPoint)

    def OnClose(self, event):
        if self.isRunning:
            self.stopOutputNotifier = True
            self.processOutputNotifierThread.join(None)
            self.UpdateUI()
        try:
            event.Skip()
        except:
            pass


