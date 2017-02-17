from tkinter import *

class StatusBar(Frame):
    _parts = {}

    def __init__(self, root, parts = [('one',0), ('two',2), ('three',3)]):
        super(StatusBar, self).__init__(root, height = 20)
        p = 0
        for part in parts:
            _ = Label(self, text = part[0], bd = 2, relief=RIDGE)
            _.grid(row = 0, column = p, sticky = 'we')
            self._parts.update({part[0]:_})
            self.columnconfigure(p, weight = part[1])
            p += 1

    def pack(self):
        super(StatusBar, self).pack(side=BOTTOM, fill=BOTH, expand=0)

    def set_value(self, **kwargs):
        for key in kwargs:
            try:
                self._parts[key].configure(text = kwargs[key])
            except KeyError:
                raise KeyError('Part "%s" not found in statusbar' % key)


if __name__ == '__main__':
    root = Tk()
    root.geometry('300x100')
    bar = StatusBar(root)
    bar.pack()
    root.bind('<a>', lambda e: bar.set_value(one = '11111'))
    root.bind('<b>', lambda e: bar.set_value(help = '11111'))
    root.mainloop()
