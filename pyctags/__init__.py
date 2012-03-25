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
A ctags file reader and a wrapper to the command line program ctags.  With the extensions that exuberant ctags provides, this could be useful for static code analysis.

This package has been tested against exuberant ctags version 5.7 and SVN revision 686 on Windows XP and Linux with Python 2.5 and 3.0.

B{Security Notes:}
 - This package makes use of the subprocess.Popen() and eval() python constructs.  
 - This package B{does not} filter the parameters for security, instead relying on module users to implement relevant security for their applications.
 
Included in the source distribution are a few examples of usage, the test cases provide a more comprehensive usage reference.

Here's a very small sample to show it in action::

    from pyctags import exuberant_ctags, ctags_file
    from pyctags.harvesters import kind_harvester

    # if you have a list of source files:
    ctags = exuberant_ctags(files=['path/to/source.h', 'path/to/source.c', 'path/to/source.py'])

    # you can generate a ctags_file instance right away
    # ctags_file is what parses lines from the generator or a 
    # tags file and creates a list of ctags_entry instances
    tag_file = ctags.generate_object()

    # override the default run parameters for exuberant ctags, so we get full kind names, say
    tag_file = ctags.generate_object(generator_options={'--fields' : '+iKmn', '-F' : None})

    print len(tagfile.tags) # number of tags
    
    harvester = kind_harvester()
    harvester.process_tag_list(tagfile.tags)
    kinds = harvester.get_data()
    print(kinds['class']) # print list of classes
    
I'm not certain if ctags generators other than Exuberant Ctags are in much use, but wrappers for them can be derived from ctags_base.
Feel free to contact me for or with details.

Pyctags is pretty heavy for large projects.  A 153 MB tag file generated from linux kernel sources takes a while to 
process and consumes over 1.1GB of RAM.  I hope to discover more ways to trim this down without going for a C implementation.
"""

from pyctags.tag_file import ctags_file
from pyctags.tag_entry import ctags_entry
from pyctags.exuberant import exuberant_ctags
import pyctags.harvesters
