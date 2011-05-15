import wx
import yapsy.IPlugin
from data.plugins.categories import General

class TaskKeeper(wx.Panel ,General , yapsy.IPlugin.IPlugin):
    def __init__(self):
        self.name = "Task Keeper"

    def Init(self, parent):
        self.parent = parent
        self.documents = None
        self.documents_tasks = {}
        self.key_words = ["#TODO","#FIXME","#HACK","#BUG"]

        wx.Panel.__init__(self, self.parent.GetBottomPanel())
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.tasks = wx.ListCtrl(self, style = wx.LC_REPORT)
        self.tasks.InsertColumn(0, "File")
        self.tasks.InsertColumn(1, "Line")
        self.tasks.InsertColumn(2, "Type")
        self.tasks.InsertColumn(3, "Task")
        self.tasks.SetColumnWidth(3, 400)
        self.sizer.Add(self.tasks, 1 ,wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()
        self.parent.AddToBottomPanel(self, "Task Keeper")
        #self.PopulateList()

    def PopulateList(self):
        self.tasks.DeleteAllItems()

        try:
            for d in self.documents:
                lst = self.CollectTasks(d.GetFileName(), d.GetText())
                self.documents_tasks[d] = lst
        except:
            pass

        garbage = [] # quick hack
        for i in self.documents:
            for j in self.documents_tasks:
                for k in self.documents_tasks[j]:
                    for l in k:
                        if l not in garbage:
                            self.tasks.Append(l)
                            garbage.append(l)

    def CollectTasks(self, doc_name ,text):
        lines = text.splitlines()
        tasks = []
        lnr = 1
        for line in lines:
            z = 0
            for t in self.key_words:
                task = []
                if t in line:
                    task.append([doc_name, lnr, self.key_words[z],
                                     line.split(self.key_words[z])[-1]])
                if task:
                    tasks.append(task)
                z += 1

            lnr += 1

        return tasks

    def NotifyDocumentOpened(self):
        self.Notify()

    def NotifyDocumentSaved(self):
        self.Notify()

    def Notify(self):
        self.documents = self.parent.GetAllDocuments()

        cur_doc = self.parent.GetCurrentDocument()
        try:
            self.documents_tasks[cur_doc]
        except:
            self.documents_tasks[cur_doc] = []

        self.PopulateList()

    def Stop(self):
        self.parent.DeleteBottomPage(self.name)
