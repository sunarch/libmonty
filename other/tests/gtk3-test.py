# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gi.repository import Gtk as gtk


class MyWindow(gtk.Window):

    def __init__(self):
        gtk.Window.__init__(self, title="Hello World")

        self.button = gtk.Button(label="Click Here")
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)

    def on_button_clicked(self, widget):
        print("Hello World")


if __name__ == '__main__':
    win = MyWindow()
    win.connect("delete-event", gtk.main_quit)
    win.show_all()
    gtk.main()
