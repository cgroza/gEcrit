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

"""
Base class for wrappers around ctags programs.

This module uses the subprocess.Popen function.  Users of this module could pass arbitrary commands to the system.
"""

import subprocess
try:
    # do relative imports for tests
    # try this first in case pyctags is already installed, since we want to be testing the source bundled in the distribution

    from kwargs_validator import the_validator as validator
except ImportError:
    from pyctags.kwargs_validator import the_validator as validator

class ctags_base:
    """
    This class exists to provide a template and some functionality for wrapping command line ctags programs.

    The functions B{_query_tag_generator}, B{generate_tags}, and B{generate_tagfile} should be overriden in child classes.
    """

    def __init__(self, *args, **kwargs):
        """
        Base class to wrap ctags program.
            - B{Keyword Arguments:}
                - B{tag_program:} (str) path to ctags executable, or name of a ctags program in path
                - B{files:} (sequence) files to process with ctags
        """
        valid_kwargs = ['tag_program', 'files']
        validator.validate(kwargs.keys(), valid_kwargs)

        self._file_list = list()
        """ A list of file names to process."""

        self._executable_path = None
        """ The ctags executable."""

        self.command_line = None
        """ The command line generated and used."""

        self.warnings = list()
        """ A place to store warnings from ctags."""

        if 'tag_program' in kwargs:
            if (self.ctags_executable(kwargs['tag_program'])):
                self._executable_path = kwargs['tag_program']
        if 'files' in kwargs:
            self._file_list = list(kwargs['files'])


    def ctags_executable(self, path):
        """
        Sets ctags path and executable.
        @param path: ctags executable name or path to it
        @type path: str
        @return: executable found
        @rtype: boolean
        """
        rval = False
        if type(path) == str:
            # see if exe_file is executable
            try:
                subprocess.Popen(path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                rval = True
            except OSError:
                pass
        if rval:
            self._query_tag_generator(path)

        return rval

    def _query_tag_generator(self, path):
        """
        Abstract method, used to test ctags generator.
        @raise NotImplementedError: Abstract method, must be overridden.
        """
        raise NotImplementedError

    def generate_tags(self, *args, **kwargs):
        """
        Abstract function to parse source files, returns list of tag strings.
        @raise NotImplementedError: Abstract method, must be overridden per
            ctags program
        """
        raise NotImplementedError

    def generate_tagfile(self, *args, **kwargs):
        """
        Abstract method to generate a tags file.
        @raise NotImplementedError: Abstract method, must be overridden per
            ctags program
        """
        raise NotImplementedError

    def input_files(self, files):
        """
        Sets the list of files to process with ctags.
        @param files: sequence of files, relative or absolute path
        @type files: sequence
        """
        self._file_list = list(files)

