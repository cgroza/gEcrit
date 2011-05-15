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
A simple validator to make sure keyword arguments are valid.
"""

class ParameterError(Exception):
    """
    Raised if an invalid argument is passed to kwargs_validator.
    """
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)

class kwargs_validator:
    """
    Used to validate arguments.
    """
    def validate(self, args, allowed_args):
        """
        @param args: arguments to check for validity.
        @type args: iterable
        @param allowed_args: list of valid arguments.
        @type allowed_args: list
        @raises ParameterError: if an element of args is not in allowed_args.
        """
        for arg in args:
            if arg not in allowed_args:
                raise ParameterError("Parameter " + arg + " is not accepted by calling function.")

the_validator = kwargs_validator()