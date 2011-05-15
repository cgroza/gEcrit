
class Passive(object):
    """
    Passive

    The plugins that inherit from this interface do not interact
    with the application.

    """
    def __init__():
        self.name = "No Name"

    def Init(self, parent):
        """
        Init

        Build the plugin gui and bind its events.
        """
        pass

    def Stop(self):
        """
        Stop

        This method is called at application exit.

        You are asked to stop your plugin and save the necessary data.
        """
        pass

class General(object):
    """
    Gadget

    Plugins of this class are notified at each event listed below.
    The plugin then takes its action when notified.

    """
    def __init__(self):
        self.name = "No Name"

    def Init(self, parent):
        """
        Init

        Build the plugin gui and bind its events.
        """
        pass

    def NotifyTabChanged(self):
        """
        NotifyTabChanged

        This method is called whenever the current tab is changed.
        """
        pass

    def NotifyDocumentOpened(self):
        """
        NotifyDocumentOpened

        This method is called whenver the user opens a new document.
        """
        pass

    def NotifyNewTabOpened(self):
        """
        NotifyNewTabOpened

        This method is called whenever the user opens an empty tab.
        """
        pass


    def NotifyDocumentSaved(self):
        """
        NotifyDocumentSaved

        This method is called whenever the user saves the current document.
        """
        pass

    def Stop(self):
        """
        Stop

        This method is called at application exit.

        You are asked to stop your plugin and save the necessary data.
        """
        pass
