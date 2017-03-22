from tkinter import ttk
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import *
from interface.riskparam import RiskParamInterface
from interface.lawrec import LawRecognitionInterface
from interface.period import PeriodInterface
from interface.parser import ParserInterface
from interface.graph import GraphInterface
from interface.statusbar import StatusBar
from integrate import get_regions, enum_parameters

from testdata import testdata

from parameters import parameters

class MySB(StatusBar):

	def __init__(self, root):
		super(MySB, self).__init__(root, parts = [('year',0), ('empty',3), ('progress',0)])
		self.set_value(year = 'Год: не выбран', empty = '', progress = 'Выполнено: 0 %')
		self.pack()

class MainWindow(tk.Tk):
	pages = {}
	nb = None

	def __init__(self):
		super(MainWindow, self).__init__()
		self.title("Определение параметров кредитного риска")
		self.nb = ttk.Notebook(self)
		self.create_pages(titles = ["Определение периода",
									"Извлечение данных",
									"Параметры риска",
									"3акон распределения параметров",
									"Hечеткоe преобразованиe",
									"Результат расчета оценки",
									"Графическое представление",
									"Сырые данные"])
		self.fill_pages()
		self.sb = MySB(self)
		self.nb.pack(expand=1, fill="both")

	def __set_period_value(self, year):
		self.current_year = year
		self.sb.set_value(year = 'Год: %s' % year)

	def create_pages(self, titles = ["Определение периода", "Извлечение данных"]):
		for t in titles:
			_ = ttk.Frame(self.nb)
			self.nb.add(_, text = t)
			self.pages.update({t:_})

	def fill_pages(self):
		period_interface = PeriodInterface(self.pages["Определение периода"])
		period_interface.set_period_value = self.__set_period_value

		parser_interface = ParserInterface(self.pages['Извлечение данных'])
		parser_interface.get_region_list = get_regions
		parser_interface.get_parameter_list = enum_parameters
		parser_interface.data = testdata

		risk_interface = RiskParamInterface(self.pages['Параметры риска'])
		risk_interface.region_list = parser_interface.selected_list
		risk_interface.data = testdata
		risk_interface.parameters = parameters

		graph_interface = GraphInterface(self.pages["Графическое представление"])

		law_interface = LawRecognitionInterface(self.pages["3акон распределения параметров"])

def callback():
	root.destroy()
	import sys
	sys.exit(0)

def demo():
	root = MainWindow()
	root.protocol("WM_DELETE_WINDOW", callback)
	root.mainloop()

if __name__ == "__main__":
	demo()
