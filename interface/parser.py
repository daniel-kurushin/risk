from tkinter import *
from tkinter import ttk

class ParserInterface(object):
	def __init__(self, frame):
		self.toplevel = frame

		self.label = Label(self.toplevel, text = 'Выберите нужные регионы и проверьте корректность сбора данных:')
		self.label.pack(side=TOP, fill=BOTH, expand=0)
		self.regn_frame = self.set_regn_frame()
		self.data_frame = self.set_data_frame()

		self.regn_frame.pack(side = LEFT, fill = Y)
		self.data_frame.pack(side = RIGHT, expand = 1, fill = BOTH)

	def set_regn_frame(self):
		aframe = Frame(self.toplevel)

		Button(aframe,
			text = 'Получить список\nрегионов',
			command = self.fill_region_list,
		).grid(row = 0, column = 0, columnspan = 2, sticky='ew')

		self.regn_scroll = Scrollbar(aframe, orient=VERTICAL)
		self.regn_select = Listbox(aframe, selectmode = EXTENDED, yscrollcommand = self.regn_scroll.set,)
		self.regn_scroll.config(command = self.regn_select.yview)
		self.regn_scroll.grid(row = 1, column = 1, sticky='ns')
		self.regn_select.grid(row = 1, column = 0, sticky='nsew')

		Button(aframe,
			text = 'Обработать\nвыборанное',
			command = self.fill_region_data,
		).grid(row = 2, column = 0, columnspan = 2, sticky='ew')

		Button(aframe,
			text = 'Обработать\nвсе',
			command = lambda: (self.regn_select.select_set(0, END), self.fill_region_data),
		).grid(row = 3, column = 0, columnspan = 2, sticky='ew')

		aframe.rowconfigure(1, weight = 1)

		return aframe

	def set_data_frame(self):
		aframe = Frame(self.toplevel)

		self.table = ttk.Treeview(aframe)
		hsc = Scrollbar(aframe, orient='hor',  command=self.table.xview)
		vsc = Scrollbar(aframe, orient='vert', command=self.table.yview)
		self.table['yscrollcommand'] = vsc.set
		self.table['xscrollcommand'] = hsc.set

		self.table["columns"]=("A","B","C","D",)
		for c in self.table["columns"]:
			self.table.column(c, width = 100)
			self.table.heading(c, text = c)

		self.table.grid(row=0, column=0, sticky='nsew')
		vsc.grid(row=0, column=1, sticky='ns')
		hsc.grid(row=1, column=0, sticky='ew')
		aframe.rowconfigure(0, weight=1)
		aframe.columnconfigure(0, weight=1)

		return aframe


	def fill_region_list(self):
		self.regn_select.delete(0, END) 
		self.code_list = {}
		for i in self.get_region_list():
			self.code_list.update({i[1]:i[0]})
			self.regn_select.insert(END, i[1])

	def fill_region_data(self):
		self.table.delete(*self.table.get_children())
		for i in self.regn_select.curselection():
			code = self.code_list[self.regn_select.get(i)]
			self.table.insert("" , 0, text = code)

if __name__ == '__main__':
	root = Tk()
	ParserInterface(root)
	root.mainloop()