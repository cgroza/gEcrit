import os.path
#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import os
import pty
import select
from array import *

import threading
import wx

import fcntl
import termios
import struct
import tty



import wx
import yapsy.IPlugin
from data.plugins.categories import Passive

class V102Terminal:
    """
    Emulator for VT100 terminal programs.

    This module provides terminal emulation for VT100 terminal programs. It handles
    V100 special characters and most important escape sequences. It also handles
    graphics rendition which specifies text style(i.e. bold, italics), foreground color
    and background color. The handled escape sequences are CUU, CUD, CUF, CUB, CHA,
    CUP, ED, EL, VPA and SGR.
    """

    __ASCII_NUL = 0  # Null
    __ASCII_BEL = 7  # Bell
    __ASCII_BS = 8  # Backspace
    __ASCII_HT = 9  # Horizontal Tab
    __ASCII_LF = 10  # Line Feed
    __ASCII_VT = 11  # Vertical Tab
    __ASCII_FF = 12  # Form Feed
    __ASCII_CR = 13  # Carriage Return
    __ASCII_XON = 17  # Resume Transmission
    __ASCII_XOFF = 19  # Stop Transmission or Ignore Characters
    __ASCII_ESC = 27  # Escape
    __ASCII_SPACE = 32  # Space
    __ASCII_CSI = 153  # Control Sequence Introducer

    __ESCSEQ_CUU = 'A'  # n A: Moves the cursor up n(default 1) times.
    __ESCSEQ_CUD = 'B'  # n B: Moves the cursor down n(default 1) times.
    __ESCSEQ_CUF = 'C'  # n C: Moves the cursor forward n(default 1) times.
    __ESCSEQ_CUB = 'D'  # n D: Moves the cursor backward n(default 1) times.

    __ESCSEQ_CHA = 'G'  # n G: Cursor horizontal absolute position. 'n' denotes

    __ESCSEQ_CUP = 'H'  # n ; m H: Moves the cursor to row n, column m.

    __ESCSEQ_ED = 'J'  # n J: Clears part of the screen. If n is zero

    __ESCSEQ_EL = 'K'  # n K: Erases part of the line. If n is zero

    __ESCSEQ_VPA = 'd'  # n d: Cursor vertical absolute position. 'n' denotes

    __ESCSEQ_SGR = 'm'  # n [;k] m: Sets SGR (Select Graphic Rendition)

    RENDITION_STYLE_BOLD = 1
    RENDITION_STYLE_DIM = 2
    RENDITION_STYLE_ITALIC = 4
    RENDITION_STYLE_UNDERLINE = 8
    RENDITION_STYLE_SLOW_BLINK = 16
    RENDITION_STYLE_FAST_BLINK = 32
    RENDITION_STYLE_INVERSE = 64
    RENDITION_STYLE_HIDDEN = 128

    CALLBACK_SCROLL_UP_SCREEN = 1
    CALLBACK_UPDATE_LINES = 2
    CALLBACK_UPDATE_CURSOR_POS = 3
    CALLBACK_UPDATE_WINDOW_TITLE = 4
    CALLBACK_UNHANDLED_ESC_SEQ = 5

    def __init__(self, rows, cols):
        """
        Initializes the terminal with specified rows and columns. User can
        resize the terminal any time using Resize method. By default the screen
        is cleared(filled with blank spaces) and cursor positioned in the first
        row and first column.
        """

        self.cols = cols
        self.rows = rows
        self.curX = 0
        self.curY = 0
        self.ignoreChars = False

        self.charHandlers = {
            self.__ASCII_NUL: self.__OnCharIgnore,
            self.__ASCII_BEL: self.__OnCharIgnore,
            self.__ASCII_BS: self.__OnCharBS,
            self.__ASCII_HT: self.__OnCharHT,
            self.__ASCII_LF: self.__OnCharLF,
            self.__ASCII_VT: self.__OnCharLF,
            self.__ASCII_FF: self.__OnCharLF,
            self.__ASCII_CR: self.__OnCharCR,
            self.__ASCII_XON: self.__OnCharXON,
            self.__ASCII_XOFF: self.__OnCharXOFF,
            self.__ASCII_ESC: self.__OnCharESC,
            self.__ASCII_CSI: self.__OnCharCSI,
            }

        self.escSeqHandlers = {
            self.__ESCSEQ_CUU: self.__OnEscSeqCUU,
            self.__ESCSEQ_CUD: self.__OnEscSeqCUD,
            self.__ESCSEQ_CUF: self.__OnEscSeqCUF,
            self.__ESCSEQ_CUB: self.__OnEscSeqCUB,
            self.__ESCSEQ_CHA: self.__OnEscSeqCHA,
            self.__ESCSEQ_CUP: self.__OnEscSeqCUP,
            self.__ESCSEQ_ED: self.__OnEscSeqED,
            self.__ESCSEQ_EL: self.__OnEscSeqEL,
            self.__ESCSEQ_VPA: self.__OnEscSeqVPA,
            self.__ESCSEQ_SGR: self.__OnEscSeqSGR,
            }

        self.printableChars = "0123456789"
        self.printableChars += "abcdefghijklmnopqrstuvwxyz"
        self.printableChars += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.printableChars += """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ """
        self.printableChars += "\t"

        self.screen = []

        self.scrRendition = []

        self.curRendition = 0L

        self.isLineDirty = []

        for i in range(rows):
            line = array('c')
            rendition = array('L')

            for j in range(cols):
                line.append(' ')
                rendition.append(0)

            self.screen.append(line)
            self.scrRendition.append(rendition)
            self.isLineDirty.append(False)

        self.callbacks = {self.CALLBACK_SCROLL_UP_SCREEN: None, self.CALLBACK_UPDATE_LINES: None,
                          self.CALLBACK_UPDATE_CURSOR_POS: None, self.CALLBACK_UNHANDLED_ESC_SEQ: None,
                          self.CALLBACK_UPDATE_WINDOW_TITLE: None}

        self.unparsedInput = None

    def GetRawScreen(self):
        """
        Returns the screen as a list of strings. The list will have rows no. of
        strings and each string will have columns no. of characters. Blank space
        used represents no character.
        """

        return self.screen

    def GetRawScreenRendition(self):
        """
        Returns the screen as a list of array of long. The list will have rows
        no. of array and each array will have columns no. of longs. The first
        8 bits of long represents rendition style like bold, italics and etc.
        The next 4 bits represents foreground color and next 4 bits for
        background color.
        """

        return self.scrRendition

    def GetRows(self):
        """
        Returns no. rows in the terminal
        """

        return self.rows

    def GetCols(self):
        """
        Returns no. cols in the terminal
        """

        return self.cols

    def GetSize(self):
        """
        Returns terminal rows and cols as tuple
        """

        return (self.rows, self.cols)

    def Resize(self, rows, cols):
        """
        Resizes the terminal to specified rows and cols.
        - If the new no. rows is less than existing no. rows then existing rows
          are deleted at top.
        - If the new no. rows is greater than existing no. rows then
          blank rows are added at bottom.
        - If the new no. cols is less than existing no. cols then existing cols
          are deleted at right.
        - If the new no. cols is greater than existing no. cols then new cols
          are added at right.
        """

        if rows < self.rows:

            for i in range(self.rows - rows):
                self.isLineDirty.pop(0)
                self.screen.pop(0)
                self.scrRendition.pop(0)
        elif rows > self.rows:

            for i in range(rows - self.rows):
                line = array('c')
                rendition = array('L')

                for j in range(self.cols):
                    line.append(' ')
                    rendition.append(0)

                self.screen.append(line)
                self.scrRendition.append(rendition)
                self.isLineDirty.append(False)

        if cols < self.cols:

            for i in range(self.rows):
                (self.screen)[i] = ((self.screen)[i])[:cols - self.cols]
                for j in range(self.cols - cols):
                    (self.scrRendition)[i].pop(len((self.scrRendition)[i]) -
                            1)
        elif cols > self.cols:

            for i in range(self.rows):
                for j in range(cols - self.cols):
                    (self.screen)[i].append(' ')
                    (self.scrRendition)[i].append(0)

        self.rows = rows
        self.cols = cols

    def GetCursorPos(self):
        """
        Returns cursor position as tuple
        """

        return (self.curY, self.curX)

    def Clear(self):
        """
        Clears the entire terminal screen
        """

        ClearRect(0, 0, self.rows - 1, self.cols - 1)

    def ClearRect(self, startRow, startCol, endRow, endCol):
        """
        Clears the terminal screen starting from startRow and startCol to
        endRow and EndCol.
        """

        if startRow < 0:
            startRow = 0
        elif startRow >= self.rows:
            startRow = self.rows - 1

        if startCol < 0:
            startCol = 0
        elif startCol >= self.cols:
            startCol = self.cols - 1

        if endRow < 0:
            endRow = 0
        elif endRow >= self.rows:
            endRow = self.rows - 1

        if endCol < 0:
            endCol = 0
        elif endCol >= self.cols:
            endCol = self.cols - 1

        if startRow > endRow:
            (startRow, endRow) = (endRow, startRow)

        if startCol > endCol:
            (startCol, endCol) = (endCol, startCol)

        for i in range(startRow, endRow + 1):
            start = 0
            end = self.cols - 1

            if i == startRow:
                start = startCol
            elif i == endRow:
                end = endCol

            for j in range(start, end + 1):
                (self.screen)[i][j] = ' '
                (self.scrRendition)[i][j] = 0

            if end + 1 > start:
                (self.isLineDirty)[i] = True

    def GetChar(self, row, col):
        '''
        Returns the character at the location specified by row and col. The
        row and col should be in the range 0..rows - 1 and 0..cols - 1."
        '''

        if row < 0 or row >= self.rows:
            return None

        if cols < 0 or col >= self.cols:
            return None

        return (self.screen)[row][col]

    def GetRendition(self, row, col):
        """
        Returns the screen rendition at the location specified by row and col.
        The returned value is a long, the first 8 bits specifies the rendition
        style and next 4 bits for foreground and another 4 bits for background
        color.
        """

        if row < 0 or row >= self.rows:
            return None

        if col < 0 or col >= self.cols:
            return None

        style = (self.scrRendition)[row][col] & 0x000000ff
        fgcolor = ((self.scrRendition)[row][col] & 0x00000f00) >> 8
        bgcolor = ((self.scrRendition)[row][col] & 0x0000f000) >> 12

        return (style, fgcolor, bgcolor)

    def GetLine(self, lineno):
        """
        Returns the terminal screen line specified by lineno. The line is
        returned as string, blank space represents empty character. The lineno
        should be in the range 0..rows - 1
        """

        if lineno < 0 or lineno >= self.rows:
            return None

        return (self.screen)[lineno].tostring()

    def GetLines(self):
        """
        Returns terminal screen lines as a list, same as GetScreen
        """

        lines = []

        for i in range(self.rows):
            lines.append((self.screen)[i].tostring())

        return lines

    def GetLinesAsText(self):
        """
        Returns the entire terminal screen as a single big string. Each row
        is seperated by \\n and blank space represents empty character.
        """

        text = ""

        for i in range(self.rows):
            text += (self.screen)[i].tostring()
            text += "\n"

        text = text.rstrip("\n")  # removes leading new lines

        return text

    def GetDirtyLines(self):
        """
        Returns list of dirty lines(line nos) since last call to GetDirtyLines.
        The line no will be 0..rows - 1.
        """

        dirtyLines = []

        for i in range(self.rows):
            if (self.isLineDirty)[i]:
                dirtyLines.append(i)
                (self.isLineDirty)[i] = False

        return dirtyLines

    def SetCallback(self, event, func):
        """
        Sets callback function for the specified event. The event should be
        any one of the following. None can be passed as callback function to
        reset the callback.

        CALLBACK_SCROLL_UP_SCREEN
            Called before scrolling up the terminal screen.

        CALLBACK_UPDATE_LINES
            Called when ever some lines need to be updated. Usually called
            before leaving ProcessInput and before scrolling up the
            terminal screen.

        CALLBACK_UPDATE_CURSOR_POS
            Called to update the cursor position. Usually called before leaving
            ProcessInput.

        CALLBACK_UPDATE_WINDOW_TITLE
            Called when ever a window title escape sequence encountered. The
            terminal window title will be passed as a string.

        CALLBACK_UNHANDLED_ESC_SEQ
            Called when ever a unsupported escape sequence encountered. The
            unhandled escape sequence(escape sequence character and it
            parameters) will be passed as a string.
        """

        (self.callbacks)[event] = func

    def ProcessInput(self, text):
        """
        Processes the given input text. It detects V100 escape sequences and
        handles it. Any partial unparsed escape sequences are stored internally
        and processed along with next input text. Before leaving, the function
        calls the callbacks CALLBACK_UPDATE_LINE and CALLBACK_UPDATE_CURSOR_POS
        to update the changed lines and cursor position respectively.
        """

        if text == None:
            return

        if self.unparsedInput != None:
            text = self.unparsedInput + text
            self.unparsedInput = None

        textlen = len(text)
        index = 0
        while index < textlen:
            ch = text[index]
            ascii = ord(ch)

            if self.ignoreChars:
                index += 1
                continue

            if ascii in self.charHandlers.keys():
                index = (self.charHandlers)[ascii](text, index)
            else:
                if ch in self.printableChars:
                    self.__PushChar(ch)
                else:
                    print "WARNING: Unsupported character %s:%d" % (ch,
                            ascii)
                index += 1

        if (self.callbacks)[self.CALLBACK_UPDATE_LINES] != None:
            (self.callbacks)[self.CALLBACK_UPDATE_LINES]()

        if (self.callbacks)[self.CALLBACK_UPDATE_CURSOR_POS] != None:
            (self.callbacks)[self.CALLBACK_UPDATE_CURSOR_POS]()

    def ScrollUp(self):
        """
        Scrolls up the terminal screen by one line. The callbacks
        CALLBACK_UPDATE_LINES and CALLBACK_SCROLL_UP_SCREEN are called before
        scrolling the screen.
        """

        if (self.callbacks)[self.CALLBACK_UPDATE_LINES] != None:
            (self.callbacks)[self.CALLBACK_UPDATE_LINES]()

        if (self.callbacks)[self.CALLBACK_SCROLL_UP_SCREEN] != None:
            (self.callbacks)[self.CALLBACK_SCROLL_UP_SCREEN]()

        line = self.screen.pop(0)
        for i in range(self.cols):
            line[i] = ' '
        self.screen.append(line)

        rendition = self.scrRendition.pop(0)
        for i in range(self.cols):
            rendition[i] = 0
        self.scrRendition.append(rendition)

    def Dump(self, file=sys.stdout):
        """
        Dumps the entire terminal screen into the given file/stdout
        """

        for i in range(self.rows):
            file.write((self.screen)[i].tostring())
            file.write("\n")

    def __NewLine(self):
        """
        Moves the cursor to the next line, if the cursor is already at the
        bottom row then scrolls up the screen.
        """

        self.curX = 0
        if self.curY + 1 < self.rows:
            self.curY += 1
        else:
            self.ScrollUp()

    def __PushChar(self, ch):
        """
        Writes the character(ch) into current cursor position and advances
        cursor position.
        """

        if self.curX >= self.cols:
            self.__NewLine()

        (self.screen)[self.curY][self.curX] = ch
        (self.scrRendition)[self.curY][self.curX] = self.curRendition
        self.curX += 1

        (self.isLineDirty)[self.curY] = True

    def __ParseEscSeq(self, text, index):
        """
        Parses escape sequence from the input and returns the index after escape
        sequence, the escape sequence character and parameter for the escape
        sequence
        """

        textlen = len(text)
        interChars = None
        while index < textlen:
            ch = text[index]
            ascii = ord(ch)

            if ascii >= 32 and ascii <= 63:

                if interChars == None:
                    interChars = ch
                else:
                    interChars += ch
            elif ascii >= 64 and ascii <= 125:

                return (index + 1, chr(ascii), interChars)
            else:
                print "Unexpected characters in escape sequence ", ch

            index += 1

        return (index, '?', interChars)

    def __HandleEscSeq(self, text, index):
        """
        Tries to parse escape sequence from input and if its not complete then
        puts it in unparsedInput and process it when the ProcessInput called
        next time.
        """

        if text[index] == '[':
            index += 1
            (index, finalChar, interChars) = self.__ParseEscSeq(text,
                    index)

            if finalChar == '?':
                self.unparsedInput = "\033["
                if interChars != None:
                    self.unparsedInput += interChars
            elif finalChar in self.escSeqHandlers.keys():
                (self.escSeqHandlers)[finalChar](interChars)
            else:
                escSeq = ""
                if interChars != None:
                    escSeq += interChars

                escSeq += finalChar

                if (self.callbacks)[self.CALLBACK_UNHANDLED_ESC_SEQ] != \
                    None:
                    (self.callbacks)[self.CALLBACK_UNHANDLED_ESC_SEQ](escSeq)
        elif text[index] == ']':

            textlen = len(text)
            if index + 2 < textlen:
                if text[index + 1] == '0' and text[index + 2] == ';':

                    index += 3  # ignore '0' and ';'
                    start = index
                    while index < textlen:
                        if ord(text[index]) == self.__ASCII_BEL:
                            break

                        index += 1

                    self.__OnEscSeqTitle(text[start:index])

        return index

    def __OnCharBS(self, text, index):
        """
        Handler for backspace character
        """

        if self.curX > 0:
            self.curX -= 1

        return index + 1

    def __OnCharHT(self, text, index):
        """
        Handler for horizontal tab character
        """

        while True:
            self.curX += 1
            if self.curX % 8 == 0:
                break
        return index + 1

    def __OnCharLF(self, text, index):
        """
        Handler for line feed character
        """

        self.__NewLine()
        return index + 1

    def __OnCharCR(self, text, index):
        """
        Handler for carriage return character
        """

        self.curX = 0
        return index + 1

    def __OnCharXON(self, text, index):
        """
        Handler for XON character
        """

        self.ignoreChars = False
        return index + 1

    def __OnCharXOFF(self, text, index):
        """
        Handler for XOFF character
        """

        self.ignoreChars = True
        return index + 1

    def __OnCharESC(self, text, index):
        """
        Handler for escape character
        """

        index += 1
        if index < len(text):
            index = self.__HandleEscSeq(text, index)

        return index

    def __OnCharCSI(self, text, index):
        """
        Handler for control sequence intruducer(CSI) character
        """

        index += 1
        index = self.__HandleEscSeq(text, index)
        return index

    def __OnCharIgnore(self, text, index):
        """
        Dummy handler for unhandler characters
        """

        return index + 1

    def __OnEscSeqTitle(self, params):
        """
        Handler for window title escape sequence
        """

        if (self.callbacks)[self.CALLBACK_UPDATE_WINDOW_TITLE] != None:
            (self.callbacks)[self.CALLBACK_UPDATE_WINDOW_TITLE](params)

    def __OnEscSeqCUU(self, params):
        """
        Handler for escape sequence CUU
        """

        n = 1
        if params != None:
            n = int(params)

        self.curY -= n
        None
        if self.curY < 0:
            self.curY = 0

    def __OnEscSeqCUD(self, params):
        """
        Handler for escape sequence CUD
        """

        n = 1
        if params != None:
            n = int(params)

        self.curY += n
        None
        if self.curY >= self.rows:
            self.curY = self.rows - 1

    def __OnEscSeqCUF(self, params):
        """
        Handler for escape sequence CUF
        """

        n = 1
        if params != None:
            n = int(params)

        self.curX += n
        None
        if self.curX >= self.cols:
            self.curX = self.cols - 1

    def __OnEscSeqCUB(self, params):
        """
        Handler for escape sequence CUB
        """

        n = 1
        if params != None:
            n = int(params)

        self.curX -= n
        None
        if self.curX < 0:
            self.curX = 0

    def __OnEscSeqCHA(self, params):
        """
        Handler for escape sequence CHA
        """

        if params == None:
            print "WARNING: CHA without parameter"
            return

        col = int(params)

        col -= 1
        if col >= 0 and col < self.cols:
            self.curX = col
        else:
            print "WARNING: CHA column out of boundary"

    def __OnEscSeqCUP(self, params):
        """
        Handler for escape sequence CUP
        """

        y = 0
        x = 0

        if params != None:
            values = params.split(';')
            if len(values) == 2:
                y = int(values[0]) - 1
                x = int(values[1]) - 1
            else:
                print "WARNING: escape sequence CUP has invalid parameters"
                return

        if x < 0:
            x = 0
        elif x >= self.cols:
            x = self.cols - 1

        if y < 0:
            y = 0
        elif y >= self.rows:
            y = self.rows - 1

        self.curX = x
        self.curY = y

    def __OnEscSeqED(self, params):
        """
        Handler for escape sequence ED
        """

        n = 0
        if params != None:
            n = int(params)

        if n == 0:
            self.ClearRect(self.curY, self.curX, self.rows - 1, self.cols -
                           1)
        elif n == 1:
            self.ClearRect(0, 0, self.curY, self.curX)
        elif n == 2:
            self.ClearRect(0, 0, self.rows - 1, self.cols - 1)
        else:
            print "WARNING: escape sequence ED has invalid parameter"

    def __OnEscSeqEL(self, params):
        """
        Handler for escape sequence EL
        """

        n = 0
        if params != None:
            n = int(params)

        if n == 0:
            self.ClearRect(self.curY, self.curX, self.curY, self.cols -
                           1)
        elif n == 1:
            self.ClearRect(self.curY, 0, self.curY, self.curX)
        elif n == 2:
            self.ClearRect(self.curY, 0, self.curY, self.cols - 1)
        else:
            print "WARNING: escape sequence EL has invalid parameter"

    def __OnEscSeqVPA(self, params):
        """
        Handler for escape sequence VPA
        """

        if params == None:
            print "WARNING: VPA without parameter"
            return

        row = int(params)

        row -= 1
        if row >= 0 and row < self.rows:
            self.curY = row
        else:
            print "WARNING: VPA line no. out of boundary"

    def __OnEscSeqSGR(self, params):
        """
        Handler for escape sequence SGR
        """

        if params != None:
            renditions = params.split(';')
            for rendition in renditions:
                irendition = int(rendition)
                if irendition == 0:

                    self.curRendition = 0L
                elif irendition > 0 and irendition < 9:

                    self.curRendition |= 1 << irendition - 1
                elif irendition >= 30 and irendition <= 37:

                    self.curRendition |= irendition - 29 << 8 & \
                        0x00000f00
                elif irendition >= 40 and irendition <= 47:

                    self.curRendition |= irendition - 39 << 12 & \
                        0x0000f000
                elif irendition == 27:

                    self.curRendition &= 0xffffffbf
                elif irendition == 39:

                    self.curRendition &= 0xfffff0ff
                elif irendition == 49:

                    self.curRendition &= 0xffff0fff
                else:
                    print "WARNING: Unsupported rendition", irendition
        else:

            self.curRendition = 0L





class ShellEmulator(wx.TextCtrl):

    def __init__(self, parent, path_to_shell):
        self.parent = parent
        self.path_to_shell = path_to_shell

        wx.TextCtrl.__init__(self, parent, -1, pos=(0, 0), size=
                             (100, 100), style=wx.TE_MULTILINE | wx.RESIZE_BORDER)
        ID_TERMINAL = self.GetId()

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

        self.termEmulator = V102Terminal(self.termRows,
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

    def OnRun(self):
        path = self.path_to_shell  #self.tc1.GetValue()
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

    def OnClose(self):
        if self.isRunning:
            self.stopOutputNotifier = True
            self.processOutputNotifierThread.join(None)
            self.UpdateUI()





class Terminator(wx.Frame, Passive, yapsy.IPlugin.IPlugin):

    def __init__(self):
        self.name = "Terminator"
        self.terminal_index = { #name : path
                              }
        self.active_shells = { #name : instance
                             }

    def Init(self, parent):
        self.parent = parent

        self.__config_path = self.parent.HOMEDIR + "/.gEcrit/Terminator.conf"

        wx.Frame.__init__(self, self.parent, size = (400,400))

        self.main_panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.add_shell_bt = wx.Button(self.main_panel, -1, "Add Shell")
        self.add_shell_bt.Bind(wx.EVT_BUTTON, self.OnAddNewTerm)

        self.remove_shell_bt = wx.Button(self.main_panel, -1, "Remove Shell")
        self.remove_shell_bt.Bind(wx.EVT_BUTTON, self.OnRemoveTerm)

        self.restart_shell_bt = wx.Button(self.main_panel, -1, "Restart Shell")
        self.restart_shell_bt.Bind(wx.EVT_BUTTON, self.OnRestartTerm)

        self.close_bt = wx.Button(self.main_panel, -1, "Close")
        self.close_bt.Bind(wx.EVT_BUTTON, self.HideMe)

        self.button_sizer.Add(self.add_shell_bt, 0, wx.EXPAND)
        self.button_sizer.AddSpacer(10)
        self.button_sizer.Add(self.remove_shell_bt, 0, wx.EXPAND)
        self.button_sizer.AddSpacer(10)
        self.button_sizer.Add(self.restart_shell_bt, 0, wx.EXPAND)
        self.button_sizer.AddSpacer(10)
        self.button_sizer.Add(self.close_bt, 0, wx.EXPAND)

        self.shell_list = wx.ListCtrl(self.main_panel, style = wx.LC_REPORT|wx.LC_SINGLE_SEL )
        self.shell_list.InsertColumn(0, "Shell")
        self.shell_list.SetColumnWidth(0,100)

        self.shell_list.InsertColumn(1, "Path")
        self.shell_list.SetColumnWidth(1,300)

        self.shell_name_txt = wx.TextCtrl(self.main_panel, -1, "[Name]")
        self.path_txt = wx.TextCtrl(self.main_panel, -1, "[Path]")

        self.main_sizer.Add(self.shell_list, 1, wx.EXPAND)
        self.main_sizer.Add(self.shell_name_txt, 0, wx.EXPAND)
        self.main_sizer.Add(self.path_txt, 0, wx.EXPAND)
        self.main_sizer.Add(self.button_sizer, 0, wx.EXPAND)



        self.main_panel.SetSizerAndFit(self.main_sizer)

        self.plugins_menu = wx.Menu()
        manage_entry = self.plugins_menu.Append(-1,"Manage Terminals")


        self.menu_item = self.parent.AddToMenuBar("Terminator",
                                                      self.plugins_menu)

        self.parent.BindMenubarEvent(manage_entry, self.ShowMe)

        self.Bind(wx.EVT_CLOSE, self.HideMe)

        self.ReadConfigFile()
        self.InitShells()
        self.PopulateShellList()


    def AddTerminal(self, term_name):
        #taking bottom panel, it will the parent of the panel
        panel = wx.Panel(self.parent.GetBottomPanel()) #the shell parent
        #creating shell
        terminal = ShellEmulator(panel, self.terminal_index[term_name])
        #sizer to keep it proprelly sized
        panel_sz = wx.BoxSizer(wx.HORIZONTAL)
        panel_sz.Add(terminal, 1, wx.EXPAND)
        terminal.OnRun() #starting shell
        panel.SetSizerAndFit(panel_sz)
        self.parent.AddToBottomPanel(panel, term_name) #add it to app bottom panel
        self.active_shells[term_name] = terminal #adding it to the active shells

    def RemoveTerminal(self, term_name):
        self.active_shells[term_name].OnClose() #closing shell
        self.parent.DeleteBottomPage(term_name) #removing from app bottom panel
        del self.active_shells[term_name] #delete it's entry from active shells
        del self.terminal_index[term_name]

    def ReadConfigFile(self):
        if os.path.exists(self.__config_path):
            #reading nd evaluating string
            conf = open(self.__config_path, "r")
            self.terminal_index = eval(conf.read())
            conf.close()
        else:
            #create default conf if it does not exists
            conf = open(self.__config_path, "w")
            conf.write('{"Python":"/usr/bin/python","Bash":"/bin/bash"}\n')
            conf.close()

    def SaveConfig(self):
        conf = open(self.__config_path, "w")
        conf.write(str(self.terminal_index)) #writing the terminal index to file
        conf.close()

    def Stop(self):
        for i in self.active_shells:
            self.active_shells[i].OnClose()

    def InitShells(self):
        for i in self.terminal_index:
            self.AddTerminal(i)

    def OnAddNewTerm(self, event):
        path = self.path_txt.GetValue().rstrip() #striping whitespace
        name = self.shell_name_txt.GetValue().rstrip()
        if os.path.exists(path):
            if not name in self.terminal_index:
                self.terminal_index[name] = path
                self.shell_list.Append([name, path])
                self.AddTerminal(name)
                self.SaveConfig() #updating config
            #shell name already exists
            else:
                wx.MessageDialog(self, "The entered name is already assigned.\n Please enter a valid name.", "Invalid Input", style = wx.OK).ShowModal()

        else:
            wx.MessageDialog(self, "The entered path does not exists.\n Please enter a valid path.", "Invalid Input", style = wx.OK).ShowModal()
        event.Skip()

    def OnRemoveTerm(self, event):
        start = -1
        selected_item = self.shell_list.GetNextSelected(start)
        if selected_item != -1:
            term_name = self.shell_list.GetItemText(selected_item) #getting selected terminal name
            self.RemoveTerminal(term_name) #removing from app bottom panel
            self.shell_list.DeleteItem(selected_item) #removing from shell_list
            self.SaveConfig() #updatig config
        event.Skip()

    def OnRestartTerm(self, event):
        start = -1
        selected_item = self.shell_list.GetNextSelected(start)
        if selected_item != -1:
            term_name = self.shell_list.GetItemText(selected_item)
            self.active_shells[term_name].OnClose()
            self.active_shells[term_name].OnRun()
        event.Skip()


    def ShowMe(self, event):
        self.Show()

    def HideMe(self, event):
        self.Hide()

    def PopulateShellList(self):
        #add all terminals to the shell_list
        for i in self.terminal_index:
            self.shell_list.Append([i, self.terminal_index[i]])

