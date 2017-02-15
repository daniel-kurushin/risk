from tkinter import *
from tkinter import ttk

class ParserInterface(object):
	data = {
		'ALTAI_KR': {
			"ВРП": 0,
			"Численность населения": 0,
			"Объем кредитов": 0,
			"Просроченная зад-ть": 0,
			"КО + фил.": 0,
			"Общий объем П/У": 0,
			"Остатки бюджета на р/с": 0,
			"Среднедуш. доходы": 0,
			"Среднедуш. расходы": 0,
			"Среднемес. з/п": 0,
		},
		'NOV-K': {
			"ВРП": 0,
			"Численность населения": 0,
			"Объем кредитов": 0,
			"Просроченная зад-ть": 0,
			"КО + фил.": 0,
			"Общий объем П/У": 0,
			"Остатки бюджета на р/с": 0,
			"Среднедуш. доходы": 0,
			"Среднедуш. расходы": 0,
			"Среднемес. з/п": 0,
		},
		'TOM_O': {
			"ВРП": 0,
			"Численность населения": 0,
			"Объем кредитов": 0,
			"Просроченная зад-ть": 0,
			"КО + фил.": 0,
			"Общий объем П/У": 0,
			"Остатки бюджета на р/с": 0,
			"Среднедуш. доходы": 0,
			"Среднедуш. расходы": 0,
			"Среднемес. з/п": 0,
		},
		'CHIT_O': {
			"ВРП": 0,
			"Численность населения": 0,
			"Объем кредитов": 0,
			"Просроченная зад-ть": 0,
			"КО + фил.": 0,
			"Общий объем П/У": 0,
			"Остатки бюджета на р/с": 0,
			"Среднедуш. доходы": 0,
			"Среднедуш. расходы": 0,
			"Среднемес. з/п": 0,
		},
	}

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

		tframe = Frame(aframe)
		bframe = Frame(aframe)

		tframe.pack(side = TOP, expand = 1, fill = BOTH)
		bframe.pack(side = BOTTOM, fill = BOTH)

		self.table = ttk.Treeview(tframe)
		hsc = Scrollbar(tframe, orient='hor',  command=self.table.xview)
		vsc = Scrollbar(tframe, orient='vert', command=self.table.yview)
		self.table['yscrollcommand'] = vsc.set
		self.table['xscrollcommand'] = hsc.set

		Button(bframe, text = 'Выгрузка в эксель').pack(side = RIGHT)
		Button(bframe, text = 'Печать').pack(side = RIGHT)
		# Выгрузка в эксель (csv)
		# Печать

		self.table.grid(row=0, column=0, sticky='nsew')
		vsc.grid(row=0, column=1, sticky='ns')
		hsc.grid(row=1, column=0, sticky='ew')
		tframe.rowconfigure(0, weight=1)
		tframe.columnconfigure(0, weight=1)

		return aframe


	def fill_region_list(self):
		self.regn_select.delete(0, END) 
		self.code_list = {}
		regn_list = self.get_region_list()
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
		return [
		"ВРП",
		"Численность населения",
		"Объем кредитов",
		"Просроченная зад-ть",
		"КО + фил.",
		"Общий объем П/У",
		"Остатки бюджета на р/с",
		"Среднедуш. доходы",
		"Среднедуш. расходы",
		"Среднемес. з/п",
		]

	def get_region_list(self):
		return [
			[
			"ALTAI_KR",
			"Алтайский край"
			],
			[
			"NOV-K",
			"Новосибирская область"
			],
			[
			"TOM_O",
			"Томская область"
			],
			[
			"CHIT_O",
			"Забайкальский край"
			]
		]

if __name__ == '__main__':
	root = Tk()
	ParserInterface(root)
	root.mainloop()