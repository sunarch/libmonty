# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there['text'] = 'Hello World\n(click me)'
        self.hi_there['command'] = self.say_hi
        self.hi_there.pack(side='top')

        self.QUIT = tk.Button(self, text='QUIT', fg='red', command=root.destroy)
        self.QUIT.pack(side='bottom')

    def say_hi(self):
        print('hi there, everyone!')
        self.hi_there2 = tk.Button(self)
        self.hi_there2['text'] = 'Hello World\n(click me)'
        self.hi_there2['command'] = self.say_hi
        self.hi_there2.pack(side='bottom')


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
