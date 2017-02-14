from tkinter import *

class PeriodInterface(object):

	years = ['2010','2011','2013','2014','2015','2016']

	def __init__(self, frame):
		self.frame = frame

		self.label = Label(self.frame, text = 'Выберите год для сбора статистики:')
		self.scroll = Scrollbar(self.frame, orient=VERTICAL)
		self.select = Listbox(self.frame, 
			height         = 5,
			selectmode     = SINGLE,
			yscrollcommand = self.scroll.set,
		)
		for y in self.years:
			self.select.insert(END, y)

		for _ in [self.label, ]:
			_.pack()

		self.scroll.config(command = self.select.yview)
		self.label.pack(side=TOP, fill=BOTH, expand=0)
		self.scroll.pack(side=RIGHT, fill=Y)
		self.select.pack(side=LEFT, fill=BOTH, expand=1)

if __name__ == '__main__':
	root = Tk()
	PeriodInterface(root)
	root.mainloop()