import cPickle
import os
import Exceptions

class gEcritSession:
    """
    gEcritSession
    
    This class represents the saved state of the gEcrit application.
    
    It stores and manages information such as open documents, GUI perspective
    and current selected tab.
    """

    __session_dump_path = os.path.expanduser("~")+"/.gEcrit/session.gecrit"


    def __init__(self):
        """
        __init__
        
        Basic constructor.
        """
        self.opened_files = []

        self.layout_perspective = ""

        self.current_tab = 0


    def RecordAppState(self, app_instance):
        """
        RecordAppState

        Saves the state of the application.
        The data it collects is:
        open documents, GUI perspective, current selected tab.
        """
        self.opened_files = []
        documents = app_instance.GetAllDocuments()
        for d in documents:
            if d is not None:
                self.opened_files.append(d.GetFilePath())

        self.layout_perspective = app_instance.GetAuiManager().SavePerspective()

        self.current_tab = app_instance.GetTabManager().GetSelection()
        if self.current_tab < 0: self.current_tab = 0

    def RestoreAppState(self, app_instance):
        """
        RestoreAppState

        Restores the open documents, the GUI perspective and selected
        document.
        """
        app_instance.OpenFile(self.opened_files)
        app_instance.GetAuiManager().LoadPerspective(self.layout_perspective)
        app_instance.GetTabManager().SetSelection(self.current_tab)

    def SaveToFile(self):
        """
        SaveToFile

        Serializes and saves this object to file.
        """
        dump_file = open(gEcritSession.__session_dump_path, "w")
        cPickle.dump(self, dump_file)

    @staticmethod
    def LoadFromFile():
        """
        LoadFromFile

        Loads the serialized object of this class.
        If it does not exist, throws NoSessionFile exception.
        """
        if os.path.exists(gEcritSession.__session_dump_path):
            session_file = open(gEcritSession.__session_dump_path, "r")
            return cPickle.load(session_file)
        else:
             raise Exceptions.NoSessionFile

    @staticmethod
    def DeleteSessionFile(event):
        """
        DeleteSessionFile

        Deletes the file where this object is serialized.
        """
        if os.path.exists(gEcritSession.__session_dump_path):
            os.remove(gEcritSession.__session_dump_path)

