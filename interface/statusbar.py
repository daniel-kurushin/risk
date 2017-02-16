from tkinter import *

class StatusBar(Frame):

    def __init__(self, root, parts = ['one', 'two', 'three']):
        super(StatusBar, self).__init__(root, height = 20)
        p = 0
        for part in parts:
            Label(self, text = part, bd = 2, relief=RIDGE).grid(row = 0, column = p, sticky = 'we')
            self.columnconfigure(p, weight = 1)
            p += 1

    def pack(self):
        super(StatusBar, self).pack(side=BOTTOM, fill=BOTH, expand=0)


if __name__ == '__main__':
    root = Tk()
    root.geometry('300x100')
    bar = StatusBar(root)
    bar.pack()
    root.mainloop()
