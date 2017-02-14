from tkinter import ttk
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import *
from interface.period import PeriodInterface
from interface.parser import ParserInterface

from main import get_regions

class MainWindow(tk.Tk):
	pages = {}
	nb = None

	def __init__(self):
		super(MainWindow, self).__init__()
		self.title("Определение параметров кредитного риска")
		self.nb = ttk.Notebook(self)
		self.create_pages()
		self.fill_pages() # ["Определение периода", "Извлечение данных", "Дедубликация данных"

		self.nb.pack(expand=1, fill="both")


	def create_pages(self, titles = ["Определение периода", "Извлечение данных"]):
		for t in titles:
			_ = ttk.Frame(self.nb)
			self.nb.add(_, text = t)
			self.pages.update({t:_})

	def fill_pages(self):
		for t in self.pages.keys():
			p = self.pages[t]
			if t == "Определение периода": PeriodInterface(p)
			if t == 'Извлечение данных': 
				_ = ParserInterface(p)
				_.get_region_list = get_regions
			if t == '_Дедубликация данных': ParserInterface(p)

def demo():
	root = MainWindow()
	root.mainloop()

if __name__ == "__main__":
	demo()