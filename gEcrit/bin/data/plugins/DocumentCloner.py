from data.plugins.categories import General
import yapsy.IPlugin
import wx


class DocumentCloner(General, yapsy.IPlugin.IPlugin):
    def __init__(self):
        self.name = "Document Cloner"

    def Init(self, parent):
        self.parent = parent

        self.plugins_menu = wx.Menu()
        clone_entry = self.plugins_menu.Append(-1,"Clone Current Document")

        self.menu_item = self.parent.AddToMenuBar("Document Cloner",
                                                      self.plugins_menu)
        self.parent.BindMenubarEvent(clone_entry, self.OnClone)

    def OnClone(self, event):
        origin = self.parent.GetCurrentDocument()
        doc =  self.parent.CreateNewDocument(self.parent.GetCurrentDocument
                                             ().GetFileName()+" -Clone")
        doc.SetText(origin.GetText())
