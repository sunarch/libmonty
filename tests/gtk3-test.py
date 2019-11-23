#!/usr/bin/env python3

from gi.repository import Gtk as gtk


class MyWindow(gtk.Window):

    def __init__(self):
        gtk.Window.__init__(self, title="Hello World")

        self.button = gtk.Button(label="Click Here")
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)

    def on_button_clicked(self, widget):
        print("Hello World")

win = MyWindow()
win.connect("delete-event", gtk.main_quit)
win.show_all()
gtk.main()
