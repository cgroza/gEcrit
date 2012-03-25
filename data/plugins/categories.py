#  Copyright (C) 2011  Groza Cristian
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

#!/usr/bin/python
# -*- coding: utf-8 -*-


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
