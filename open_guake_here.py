#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module adds a menu item to the nautilus right-click menu which allows to
   open the guake terminal with a new tab set on the current directory
"""


from gi.repository import Nautilus, GObject, Gtk, GdkPixbuf
import urllib, os, subprocess
import locale, gettext

APP_NAME = "nautilus-pyextensions"
LOCALE_PATH = "/usr/share/locale/"
ICONPATH = "/usr/share/icons/gnome/48x48/apps/terminal.png"

# internationalization
locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(APP_NAME, LOCALE_PATH)
gettext.textdomain(APP_NAME)
_ = gettext.gettext
# post internationalization code starts here


class OpenTerminalGeometry(GObject.GObject, Nautilus.MenuProvider):
    """Implements the 'Open Guake here' extension to the nautilus right-click menu"""

    def __init__(self):
        """Nautilus crashes if a plugin doesn't implement the __init__ method"""
        try:
            factory = Gtk.IconFactory()
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(ICONPATH)
            iconset = Gtk.IconSet.new_from_pixbuf(pixbuf)
            factory.add("terminal", iconset)
            factory.add_default()
        except: pass

    def run(self, menu, selected):
        """Runs the Open Guake here on the given Directory"""
        uri_raw = selected.get_uri()
        if len(uri_raw) < 7: return
        curr_dir = urllib.unquote(uri_raw[7:])
        if os.path.isfile(curr_dir): curr_dir = os.path.dirname(curr_dir)
        bash_string = "guake -t -n '" + curr_dir + "'"
        subprocess.call(bash_string, shell=True)

    def get_file_items(self, window, sel_items):
        """Adds the 'Open Guake here' menu item to the Nautilus right-click menu,
           connects its 'activate' signal to the 'run' method passing the selected Directory/File"""
        if len(sel_items) != 1 or sel_items[0].get_uri_scheme() != 'file': return
        item = Nautilus.MenuItem(name='NautilusPython::guake',
                                 label=_('Open Guake Here'),
                                 tip=_('Open the Guake terminal on the Current/Selected Directory'),
                                 icon='terminal')
        item.connect('activate', self.run, sel_items[0])
        return [item]

    def get_background_items(self, window, current_directory):
        """Adds the 'Open Guake here' menu item to the Nautilus right-click menu,
           connects its 'activate' signal to the 'run' method passing the current Directory"""
        item = Nautilus.MenuItem(name='NautilusPython::guake',
                                 label=_('Open Guake Here'),
                                 tip=_('Open the Guake terminal on the Current Directory'),
                                 icon='terminal')
        item.connect('activate', self.run, current_directory)
        return [item]
