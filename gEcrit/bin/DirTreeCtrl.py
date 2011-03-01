#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    DirTreeCtrl

    @summary: A tree control for use in displaying directories
    @author: Collin Green aka Keeyai
    @url: http://keeyai.com
    @license: public domain -- use it how you will, but a link back would be nice
    @version: 0.9.0
    @note:
        behaves just like a TreeCtrl

        Usage:
            set your default and directory images using addIcon -- see the commented
            last two lines of __init__

            initialze the tree then call SetRootDir(directory) with the root
            directory you want the tree to use

        use SetDeleteOnCollapse(bool) to make the tree delete a node's children
        when the node is collapsed. Will (probably) save memory at the cost of
        a bit o' speed

        use addIcon to use your own icons for the given file extensions


    @todo:
        extract ico from exes found in directory
"""

import wx
import os


class Directory:

    """Simple class for using as the data object in the DirTreeCtrl"""

    __name__ = 'Directory'

    def __init__(self, directory=''):
        self.directory = directory


class DirTreeCtrl(wx.TreeCtrl):

    """A wx.TreeCtrl that is used for displaying directory structures.
    Virtually handles paths to help with memory management.
    """

    def __init__(self, parent, id, direct, *args, **kwds):
        """Initializes the tree and binds some events we need for
        making this dynamically load its data."""

        wx.TreeCtrl.__init__(self, parent, *args, **kwds)
        self.parent = parent

        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.TreeItemExpanding)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.TreeItemCollapsing)

        self.DELETEONCOLLAPSE = False

        self.iconentries = {}
        self.imagelist = wx.ImageList(16, 16)

        (self.iconentries)['default'] = -1
        (self.iconentries)['directory'] = -1

        self.SetRootDir(direct)

    def addIcon(self, filepath, wxBitmapType, name):
        """Adds an icon to the imagelist and registers it with the iconentries dict
        using the given name. Use so that you can assign custom icons to the tree
        just by passing in the value stored in self.iconentries[name]
        @param filepath: path to the image
        @param wxBitmapType: wx constant for the file type - eg wx.BITMAP_TYPE_PNG
        @param name: name to use as a key in the self.iconentries dict - get your imagekey by calling
            self.iconentries[name]
        """

        try:
            if os.path.exists(filepath):
                key = self.imagelist.Add(wx.Bitmap(filepath,
                        wxBitmapType))
                (self.iconentries)[name] = key
        except Exception, e:
            print e

    def SetDeleteOnCollapse(self, selection):
        """Sets the tree option to delete leaf items when the node is
        collapsed. Will slow down the tree slightly but will probably save memory."""

        if type(selection) == type(True):
            self.DELETEONCOLLAPSE = selection

    def SetRootDir(self, directory):
        """Sets the root directory for the tree. Throws an exception
        if the directory is invalid.
        @param directory: directory to load
        """

        if not os.path.isdir(directory):
            raise Exception("%s is not a valid directory" % directory)

        self.DeleteAllItems()

        root = self.AddRoot(directory)
        self.SetPyData(root, Directory(directory))
        self.SetItemImage(root, (self.iconentries)['directory'])
        self.Expand(root)

        self._loadDir(root, directory)

    def _loadDir(self, item, directory):
        """Private function that gets called to load the file list
        for the given directory and append the items to the tree.
        Throws an exception if the directory is invalid.

        @note: does not add items if the node already has children"""

        if not os.path.isdir(directory):
            raise Exception("%s is not a valid directory" % directory)

        if self.GetChildrenCount(item) == 0:

            files = os.listdir(directory)

            for f in files:

                if os.path.isdir(os.path.join(directory, f)):

                    child = self.AppendItem(item, f)
                    self.SetItemHasChildren(child, True)

                    self.SetPyData(child, Directory(os.path.join(directory,
                                   f)))
                else:

                    self.AppendItem(item, f)

    def getFileExtension(self, filename):
        """Helper function for getting a file's extension"""

        if not os.path.isdir(filename):

            index = filename.rfind('.')
            if index > -1:
                return filename[index:]
            return ''
        else:
            return 'directory'

    def processFileExtension(self, filename):
        """Helper function. Called for files and collects all the necessary
        icons into in image list which is re-passed into the tree every time
        (imagelists are a lame way to handle images)"""

        ext = self.getFileExtension(filename)
        ext = ext.lower()

        excluded = ['', '.exe', '.ico']

        if ext not in excluded:

            if ext not in self.iconentries.keys():

                try:

                    filetype = wx.TheMimeTypesManager.GetFileTypeFromExtension(ext)

                    if hasattr(filetype, 'GetIconInfo'):
                        info = filetype.GetIconInfo()

                        if info is not None:
                            icon = info[0]
                            if icon.Ok():

                                iconkey = self.imagelist.AddIcon(icon)
                                (self.iconentries)[ext] = iconkey

                                self.SetImageList(self.imagelist)

                                return iconkey
                except:
                    return (self.iconentries)['default']
            else:

                return (self.iconentries)[ext]
        elif ext == '.exe':

            pass
        elif ext == '.ico':

            try:
                icon = wx.Icon(filename, wx.BITMAP_TYPE_ICO)
                if icon.IsOk():
                    return self.imagelist.AddIcon(icon)
            except Exception, e:

                print e
                return (self.iconentries)['default']

        return (self.iconentries)['default']

    def TreeItemExpanding(self, event):
        """Called when a node is about to expand. Loads the node's
        files from the file system."""

        item = event.GetItem()

        if type(self.GetPyData(item)) == type(Directory()):
            d = self.GetPyData(item)
            self._loadDir(item, d.directory)
        else:

            pass

        event.Skip()

    def TreeItemCollapsing(self, event):
        """Called when a node is about to collapse. Removes
        the children from the tree if self.DELETEONCOLLAPSE is
        set - see L{SetDeleteOnCollapse}
        """

        item = event.GetItem()

        if self.DELETEONCOLLAPSE:
            self.DeleteChildren(item)

        event.Skip()

    def GetSelectedPath(self, event):
        item = event.GetItem()

        item_parent = self.GetItemParent(item)

        if not self.ItemHasChildren(item):
            d = self.GetPyData(item_parent)
            return str(d.directory + "/" + self.GetItemText(self.GetSelection()))
        else:

            print 'no data found!'
            return False

        event.Skip()


