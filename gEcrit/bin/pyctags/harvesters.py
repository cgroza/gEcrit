## Copyright (C) 2008 Ben Smith <benjamin.coder.smith@gmail.com>

##    This file is part of pyctags.

##    pyctags is free software: you can redistribute it and/or modify
##    it under the terms of the GNU Lesser General Public License as published
##    by the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.

##    pyctags is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.

##    You should have received a copy of the GNU Lesser General Public License
##    and the GNU Lesser General Public Licens along with pyctags.  If not,
##    see <http://www.gnu.org/licenses/>.

""" Classes that process tag data to collect information."""
from copy import copy

try:
    # do relative imports for tests
    # try this first in case pyctags is already installed, since we want to be testing the source bundled in the distribution
    from kwargs_validator import the_validator as validator
except ImportError:
    from pyctags.kwargs_validator import the_validator as validator

class base_harvester:
    """ This class definition outlines the basic interface for harvesting classes."""
    def do_before(self):
        """ Called before any entries are processed with self.feed()."""
        pass

    def feed(self, entry):
        """ Called once per ctags_entry.
        @param entry: a tag entry to process.
        @type entry: ctags_entry
        """
        pass

    def do_after(self):
        """ Called after all ctags_entry instances are processed with self.feed()."""
        pass

    def get_data(self):
        """ Used to retrieve derived-class specific harvested data."""
        pass

    def process_tag_list(self, taglist):
        """
        Allows processing of a list of ctags_entry instances without an associated ctags_file.
        @param taglist: list of ctags_entry instances
        @type taglist: list
        """
        self.do_before()
        for tag in taglist:
            self.feed(tag)
        self.do_after()

class kind_harvester(base_harvester):
    """ Harvests exuberant ctags' extended "kind" information, such as class, member, variable, etc."""
    def __init__(self):
        self.kinds = {}

    def feed(self, entry):
        """
        Organizes data into a dict with kind as the keys, values are a list of entries of that kind.
        @param entry: entry to process
        @type entry: ctags_entry
        """
        if 'kind' in entry.extensions:
            # note: case sensitive output from exuberant ctags
            entkey = entry.extensions['kind']
            if entkey not in self.kinds:
                self.kinds[entkey] = list()
            self.kinds[entkey].append(entry)

    def get_data(self):
        """
        Gets the dict built with self.feed().
        Dict keys are tag kinds, values are lists of ctags_entry instances sporting that kind.
        @returns: tag data organized by exuberant ctags kind
        @rtype: dict
        """
        return self.kinds

class by_name_harvester(base_harvester):
    """ Organizes tags by name."""
    def __init__(self):
        self.names = dict()

    def feed(self, entry):
        """
        Builds a ctags_entry.name keyed dict.
        """
        if entry.name not in self.names:
            self.names[entry.name] = list()
        self.names[entry.name].append(entry)

    def get_data(self):
        """
        Gets the name-organized data.
        @returns: entries organized with entry.name as key, value is a list of ctags_entry instances that correspond to entry.name
        @rtype: dict
        """
        return self.names

class name_lookup_harvester(base_harvester):
    """ Builds a sorted list of unique tag names."""
    def __init__(self):
        self.__unique_names = dict()
        self.__sorted_names = list()
        self.__name_index = dict()

    def __len__(self):
        """ Number of unique tag names found."""
        return len(self.__sorted_names)

    def feed(self, entry):
        """ Records unique names.
        @param entry: the entry to collect the name from.
        @type entry: ctags_entry
        """
        # use dict characteristic of unique keys instead of testing if the key is already there
        self.__unique_names[entry.name] = None

    def do_after(self):
        """ Process the unique names into a form easier to query."""
        self.__sorted_names = list(self.__unique_names.keys())
        self.__sorted_names.sort()

        i = 0
        prev_char = self.__sorted_names[0][0]
        self.__name_index[prev_char] = {'first' : 0}
        for f in self.__sorted_names:
            if f[0] not in self.__name_index:
                self.__name_index[prev_char]['last'] = i - 1
                self.__name_index[f[0]] = {'first' : i}
                prev_char = f[0]
            i += 1
        self.__name_index[prev_char]['last'] = i

    def starts_with(self, matchstr, **kwargs):
        """
        Fetches an alphabetical list of unique tag names that begin with matchstr.
            - B{Parameters:}
                - B{matchstr:} (str) string to search for in tags db
            - B{Keyword Arguments:}
                - B{num_results:} (int) maximum number of results to return, 0 for all, default
                - B{case_sensitive:} (bool) whether to match case, default False
        @returns: matching tag names
        @rtype: list
        """

        valid_kwargs = ['num_results', 'case_sensitive']
        validator.validate(kwargs.keys(), valid_kwargs)

        final_list = []
        case_sensitive = False
        num_results = 0

        if 'num_results' in kwargs:
            num_results = int(kwargs['num_results'])

        if len(matchstr) == 0:
            if num_results:
                return self.__sorted_names[0:num_results]
            return self.__sorted_names[:]

        if 'case_sensitive' in kwargs:
            if kwargs['case_sensitive']:
                case_sensitive = True

        tag_names_that_start_with_char = []

        if case_sensitive:
            if matchstr[0] not in self.__name_index:
                return []
        else:
            if matchstr[0].lower() not in self.__name_index and matchstr[0].upper() not in self.__name_index:
                return []

        if case_sensitive:
            idxs = self.__name_index[matchstr[0]]

            if idxs['first'] == idxs['last'] + 1:
                tag_names_that_start_with_char = self.__sorted_names[idxs['first']]
            else:
                tag_names_that_start_with_char = self.__sorted_names[idxs['first']:idxs['last'] + 1]

        else:
            if matchstr[0].lower() in self.__name_index:
                idxs = self.__name_index[matchstr[0].lower()]

                if idxs['first'] == idxs['last'] + 1:
                    tag_names_that_start_with_char = self.__sorted_names[idxs['first']]
                else:
                    tag_names_that_start_with_char = self.__sorted_names[idxs['first']:idxs['last'] + 1]

            if matchstr[0].upper() in self.__name_index:
                idxs = self.__name_index[matchstr[0].upper()]

                if idxs['first'] == idxs['last'] + 1:
                    tag_names_that_start_with_char += [self.__sorted_names[idxs['first']]]
                else:
                    tag_names_that_start_with_char += self.__sorted_names[idxs['first']:idxs['last'] + 1]

        if len(matchstr) == 1:
            if num_results == 0:
                return tag_names_that_start_with_char[:]
            else:
                return tag_names_that_start_with_char[0:num_results]

        if case_sensitive:
            for t in tag_names_that_start_with_char:
                if (t.find(matchstr) == 0):
                    final_list.append(copy(t))
                if num_results > 0 and len(final_list) == num_results:
                    return final_list
        else:
            for t in tag_names_that_start_with_char:
                if (t.lower().find(matchstr.lower()) == 0):
                    final_list.append(copy(t))
                if num_results > 0 and len(final_list) == num_results:
                    return final_list

        return final_list
