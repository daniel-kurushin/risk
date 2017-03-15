from tkinter import *
from tkinter import ttk

from threading import Thread
from queue import Queue

class LawRecognitionInterface(object):
	data = { "P1": {"ALTAI_KR":0, "NOV-K":0}, "P2": {"ALTAI_KR":0, "NOV-K":0}, "P3": {"ALTAI_KR":0, "NOV-K":0}, "P4": {"ALTAI_KR":0, "NOV-K":0}, "P5": {"ALTAI_KR":0, "NOV-K":0}, "P6": {"ALTAI_KR":0, "NOV-K":0}, "P7": {"ALTAI_KR":0, "NOV-K":0}, "P8": {"ALTAI_KR":0, "NOV-K":0}, "P9": {"ALTAI_KR":0, "NOV-K":0}, "P10": {"ALTAI_KR":0, "NOV-K":0}, }

	def __init__(self, frame):
		self.toplevel = frame

		self.label = Label(self.toplevel, text = 'Определите законы распределения данных по параметрам:')
		self.label.pack(side=TOP, fill=BOTH, expand=0)
		self.data_frame = self.set_data_frame()
		self.data_frame.pack(side = RIGHT, expand = 1, fill = BOTH)

	def set_data_frame(self):
		aframe = Frame(self.toplevel)

		tframe = Frame(aframe)
		bframe = Frame(aframe)

		Label(tframe, text = 'Наименование параметра').grid(row=0, column=0, sticky='nsew')
		Label(tframe, text = 'Гистограмма'           ).grid(row=0, column=1, sticky='nsew')
		Label(tframe, text = 'Выбор закона'          ).grid(row=0, column=2, sticky='nsew')
		Label(tframe, text = 'Результат'             ).grid(row=0, column=3, sticky='nsew')
		i = 1
		for par in self.data.keys():
			Label(tframe, text = par).grid(row=i, column=0, sticky='nsew')
			Button(tframe, text = 'Определить закон').grid(row=i, column=2, sticky='nsew')
			_ = Listbox(tframe)
			for law in ['Нормальный','Логнормальный','Экспоненциальный']:
				_.insert(END, law)
			_.grid(row=i, column=3, sticky='nsew')

			i += 1

		tframe.pack(side = TOP, expand = 1, fill = BOTH)
		bframe.pack(side = BOTTOM, fill = BOTH)

		vsc = Scrollbar(tframe, orient='vert')

		Button(bframe, text = 'Выгрузка в Excel').pack(side = RIGHT)
		Button(bframe, text = 'Печать').pack(side = RIGHT)
		# Выгрузка в эксель (csv)
		# Печать

		vsc.grid(row=0, column=4, rowspan=11, sticky='ns')
		# tframe.rowconfigure(0, weight=1)
		tframe.columnconfigure(0, weight=1)
		tframe.columnconfigure(1, weight=1)
		tframe.columnconfigure(2, weight=1)
		tframe.columnconfigure(3, weight=1)

		return aframe


	def fill_region_list(self):
		self.regn_select.delete(0, END)
		self.code_list = {}
		# Thread(target = self.get_region_list)
		# while que.empty():
		# 	pass
		regn_list = self.get_region_list()#
		regn_list.sort()
		for i in regn_list:
			self.code_list.update({i[1]:i[0]})
			self.regn_select.insert(END, i[1])

	def fill_region_data(self):
		self.table["columns"] = self.get_parameter_list()
		self.table.heading('#0', text = 'Регион')
		self.table.column('#0', width = 200)
		for c in self.table["columns"]:
			self.table.heading(c, text = c)
			self.table.column(c, anchor = 'e', minwidth = 50, width = 120)

		self.table.delete(*self.table.get_children())
		selection = self.regn_select.curselection()

		for i in selection:
			regn = self.regn_select.get(i)
			code = self.code_list[regn]
			values = []
			for x in self.table["columns"]:
				try:
					values += [self.data[code][x]]
				except KeyError:
					values += [0]
			self.table.insert("" , END, text = regn, values = values)

	def get_parameter_list(self):
		return [ "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10",  ]

	def get_region_list(self):
		return [ [ "ALTAI_KR", "Алтайский край" ], [ "NOV-K", "Новосибирская область" ], [ "TOM_O", "Томская область" ], [ "CHIT_O", "Забайкальский край" ] ]

if __name__ == '__main__':
	root = Tk()
	ParserInterface(root)
	root.mainloop()
