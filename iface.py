from tkinter import ttk
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import *
from interface.riskparam import RiskParamInterface
from interface.lawrec import LawRecognitionInterface
from interface.period import PeriodInterface
from interface.parser import ParserInterface
from interface.statusbar import StatusBar
from integrate import get_regions, enum_parameters

from testdata import testdata

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
		self.create_pages(titles = ["Определение периода", "Извлечение данных", "Параметры риска", "3акон распределения параметров", "Hечеткоe преобразованиe", "Результат расчета оценки", "Модель оценки риска", "Сырые данные"])
		self.fill_pages() # ["Определение периода", "Извлечение данных", "Параметры риска", "Определение закона распределения параметров", "Результат нечеткого преобразования", "Результат расчета оценки", "Модель оценки риска","-->Сырые данные",
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
		for t in self.pages.keys():
			p = self.pages[t]
			if t == "Определение периода":
				_ = PeriodInterface(p)
				_.set_period_value = self.__set_period_value
			if t == 'Извлечение данных':
				_ = ParserInterface(p)
				_.get_region_list = get_regions
				_.get_parameter_list = enum_parameters
				_.data = testdata
			if t == "Параметры риска":
				_ = RiskParamInterface(p)
			if t == "3акон распределения параметров":
				_ = LawRecognitionInterface(p)
			if t == '_Дедубликация данных': ParserInterface(p)

def demo():
	root = MainWindow()
	root.mainloop()

if __name__ == "__main__":
	demo()
