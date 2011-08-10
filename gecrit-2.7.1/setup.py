from distutils.core import setup

short_description = " gEcrit is a text editor used to write Python source code."

long_descr = """
gEcrit is a text editor used to write Python source code.
You can find all the common features that you may find in other editors.
It features a plugin system that allows the application to be extended
easily.

It it comes with pulgins such as a terminal emulator, a source code refactoirng tool based on Pytidy etc.

"""

setup(
    name = "gEcrit",
    version = "2.7",
    description = short_description,
    long_description = long_descr,
    author = "Groza Cristian",
    author_email = "kristi9524@gmail.com",
    url = "http://sourceforge.net/projects/gecrit/",
    scripts = ["gecrit"],
    license = "GPL3",
    packages = ["gEcrit"],
    package_dir = {"gEcrit" : "."},
    package_data = {"gEcrit" : ["yapsy/*", "pyctags/*" ,"data/__init__.py","data/plugins/*","icons/*", "locale/ro/LC_MESSAGES/*",
                                "locale/es/LC_MESSAGES/*", "locale/pl/LC_MESSAGES/*", "runner.sh"]},

#    py_modules = ["yapsy/*", "pyctags/*"]
    )
