"""
Определение параметров кредитного риска
модуль обработки данных по регионам
Курушин Д.С.
Васильева Е.Е.
Долгова Е.В.
"""

from cbrparser import *
from gksparser import *
from json import dumps
from student import Student

import math
import scipy.stats as ss
import scipy as sp
import numpy as np
from matplotlib.pyplot import *	

def _filter(x):
	try:
		return int(x)
	except ValueError:
		return 0

def get_regions():
	crvl = crowl()
	res = []
	for x in crvl.keys():
		for y in crvl[x]['subs'].keys():
			try:
				res += [(y, crvl[x]['subs'][y]['name'])]
			except:
				pass

	return res

def enum_parameters():
	return [
		"Количество филиалов",
		"Объем кредитов",
		"Просроченная задолженность"	,
		"Остатки бюджета",
		"Валовый региональный продукт",
		"Количество организаций",
		"Среднедушевые денежные расходы населения",
		"Общий объем прибыли/убытков",
		"Численность населения",
		"Среднедушевые денежные доходы населения",
		"Среднемесячная заработная плата",
		"Всего организаций",
	]


def compare_names(n1, n2):
	import nltk
	import pymorphy2
	import re

	low = ["область", "край", "округ", "республика", "год", "тот"]

	morph = pymorphy2.MorphAnalyzer()

	def word_to_tokens(words):
		res = []
		for word in words:
			t = morph.parse(word)[0]
			if (t.tag.POS in ['COMP', 'PREP', 'PRED', 'NPRO', 'CONJ', 'PRCL', 'INTJ']) or \
			   (t.tag.POS == None):
				continue
			res += [t.normal_form]

		return res

	tkn = nltk.tokenize.WordPunctTokenizer()
	w1 = tkn.tokenize(n1)
	w2 = tkn.tokenize(n2)


	t1 = word_to_tokens(tkn.tokenize(n1))
	t2 = word_to_tokens(tkn.tokenize(n2))

	if len(t1) < len(t2): t1, t2 = t2, t1
	
	n, m, k = 0.0, 0.0, 0.0

	for token in t1:
		if low.count(token) > 0:
			k = 0.3
		else:
			k = 1.0
		if t2.count(token) > 0:
			n += k
		m += k

	return n / m

def get_code_by_name(regions, name):
	for region in regions:
		_ = compare_names(region[1], name)
		if _ >= 1/2:
			return region[0]
	raise ValueError('Name %s not found' % name)

def get_name_by_code(regions, code):
	for region in regions:
		if region[0] == code:
			return region[1]
	raise ValueError('Code %s not found' % code)



def summ_koif(year = 2013, regions = [('VORO',''),('MARI','')]):
	res = dict()
	for r in regions:
		_ = koif_by_month(year = year, region = r[0])
		kf = 0
		ko = 0
		n  = 0
		for _date in _.keys():
			__ = _[_date]
			kf += _filter(__["Kоличество филиалов в регионe"]["всего"])
			ko += _filter(__["Kоличество кредитных органзаций в регионе"])
			n += 1
		try:
			n1 = round((kf + ko)/n)
			n2 = round(kf/n)
			n3 = round(ko/n)
		except ZeroDivisionError:
			n1 = 0
			n2 = 0
			n3 = 0
		
		res.update({r[0]:{'Количество филиалов':n2,'Количество организаций':n3,'Всего организаций':n1}})
	return res

def summ_przd(year = 2013, regions = [('VORO',''),('MARI','')]):
	res = dict()
	for r in regions:
		_ = przd_by_month(year = year, region = r[0])
		pz = 0
		n  = 0
		for _date in _.keys():
			__ = _[_date]
			pz += _filter(__['Всего просроченная задолженность'])
			n += 1
		try:
			n1 = round(pz/n)
		except ZeroDivisionError:
			n1 = 0
		
		res.update({r[0]:{"Просроченная задолженность":n1}})

	return res

def summ_krob(year = 2013, regions = [('VORO',''),('MARI','')]):
	res = dict()
	for r in regions:
		_ = krob_by_month(year = year, region = r[0])
		ko = 0
		n  = 0
		for _date in _.keys():
			__ = _[_date]
			ko += _filter(__['Объем кредитов'])
			n += 1
		try:
			n1 = round(ko/n)
		except ZeroDivisionError:
			n1 = 0
		
		res.update({r[0]:{"Объем кредитов":n1}})

	return res

def summ_frdko(year = 2013, regions = [('VORO',''),('MARI','')]):
	res = dict()

	for r in regions:
		_ = frdko_by_month(year = year, region = r[0])
		try:
			__ = _['01.01.%s' % (year)]
			oo = _filter(__['Общий объем прибыли/убытков, полученных действующими кредитными организациями'])
		except KeyError:
			for month in range(12,4,-1):
				try:
					__ = _['01.%02d.%s' % (month, year)]
					oo = _filter(__['Общий объем прибыли/убытков, полученных действующими кредитными организациями'])
					break
				except KeyError:
					continue
		
		try:
			res.update({r[0]:{"Общий объем прибыли/убытков":oo}})
		except NameError:
			res.update({r[0]:{"Общий объем прибыли/убытков":0}})

	return res

def summ_osts(year, regions):
	ostb = ostbs_by_month()
	res = {} 
	for ost in ostb.keys():
		try:
			res.update(
				{get_code_by_name(regions, ost):{'Остатки бюджета':ostb[ost]['01.12.%s' % year]}}
			)
		except ValueError:
			pass
	return res

def filter_vrp(regions, year, vrp):
	res = {}
	for reg in vrp:
		try:
			code = get_code_by_name(regions, reg)
			value = vrp[reg]['31.12.%s' % year]
			res.update({code:{'Валовый региональный продукт': value}})
		except ValueError:
			pass
	return res

def filter_salary(regions, year, salary):
	res = {}
	for reg in salary:
		try:
			code = get_code_by_name(regions, reg)
			value = salary[reg]['31.12.%s' % year]
			res.update({code:{'Среднемесячная заработная плата': value}})
		except ValueError:
			pass
	return res

def filter_income(regions, year, income):
	res = {}
	for reg in income:
		try:
			code = get_code_by_name(regions, reg)
			value = income[reg]['31.12.%s' % year]
			res.update({code:{'Среднедушевые денежные доходы населения': value}})
		except ValueError:
			pass
	return res

def filter_population(regions, year, population):
	res = {}
	for reg in population:
		try:
			code = get_code_by_name(regions, reg)
			value = population[reg]['31.12.%s' % year]
			res.update({code:{'Численность населения': value}})
		except ValueError:
			pass
	return res

def filter_rasxod(regions, year, rasxod):
	res = {}
	for reg in rasxod:
		try:
			code = get_code_by_name(regions, reg)
			value = rasxod[reg]['31.12.%s' % year]
			res.update({code:{'Среднедушевые денежные расходы населения': value}})
		except ValueError:
			pass
	return res

def parse():
	x = get_regions()
	# print(dumps(x, ensure_ascii=0, indent=2))
	frdko = summ_frdko(2013,x)
	print(dumps(frdko, ensure_ascii=0, indent=2))

	popl = filter_population(regions = x, population = get_region_population(), year = 2013)
	print(dumps(popl, ensure_ascii=0, indent=2))

	vrp = filter_vrp(regions = x, vrp = get_region_vrp(), year = 2013)
	print(dumps(vrp, ensure_ascii=0, indent=2))

	salary = filter_salary(regions = x, salary = get_region_salary(), year = 2013)
	print(dumps(salary, ensure_ascii=0, indent=2))

	income = filter_income(regions = x, income = get_region_income(), year = 2013)
	print(dumps(income, ensure_ascii=0, indent=2))

	rasxod = filter_rasxod(regions = x, rasxod = get_region_rasxod(), year = 2013)
	print(dumps(rasxod, ensure_ascii=0, indent=2))

	koif = summ_koif(2013,x)
	print(dumps(koif, ensure_ascii=0, indent=2))

	przd = summ_przd(2013,x)
	print(dumps(przd, ensure_ascii=0, indent=2))

	krob = summ_krob(2013,x)
	print(dumps(krob, ensure_ascii=0, indent=2))

	ostb = summ_osts(2013,x)
	print(dumps(ostb, ensure_ascii=0, indent=2))

	res = {}
	for _reg in x:
		reg = _reg[0]
		resres = {}
		for data in [popl,vrp,salary,income,rasxod,koif,przd,krob,frdko,ostb]:
			try:
				for k in data[reg]:
					resres.update({k:data[reg][k]})
			except KeyError:
				print("Exception %s" % reg)
		res.update(
			{reg: resres}
		)
	print(dumps(res, ensure_ascii=0, indent=2))

def calcP(data = {}):
	res = {}
	for reg in data.keys():
		x = data[reg]
		try:
			P = [0,x["Объем кредитов"] / x["Валовый региональный продукт"],
				   x["Объем кредитов"] / x["Всего организаций"],
				   x["Объем кредитов"] / (x["Общий объем прибыли/убытков"] / 12),
				  (x["Остатки бюджета"] / 12) / (x["Численность населения"] / 1000),
				  (x["Среднедушевые денежные доходы населения"] - x["Среднедушевые денежные расходы населения"]) / x["Среднемесячная заработная плата"],
				   x["Просроченная задолженность"] / x["Объем кредитов"],
				   x["Просроченная задолженность"] / x["Валовый региональный продукт"],
				   x["Просроченная задолженность"] / x["Всего организаций"],
				   x["Просроченная задолженность"] / (x["Численность населения"] / 1000),
				   x["Общий объем прибыли/убытков"] / x["Всего организаций"],]
		except KeyError as e:
			P = [0, 'KeyError %s' % e]
		except ZeroDivisionError as e:
			P = [0, 'ZeroDivisionError %s' % e]
		res.update({reg:P})

	return res

def get_best_distr(data, dist_list):

	s = Student(data)
	x = np.array([_ for _ in data if abs(s.X - _) < s.Dx * 3 and abs(_) > 1])
	s = Student(data)
	nx = (x - s.X)/s.Dx
	
	h_obs = np.histogram(nx, 14)[0]
	h_obs = h_obs / np.mean(h_obs)

	res = {}
	for dist in dist_list:
		if dist == 'norm':     _ = ss.norm.rvs(s.Dx, size = 10000)
		if dist == 'lognorm':  _ = ss.lognorm.rvs(s.Dx, size = 10000)
		if dist == 'expon':    _ = ss.expon.rvs(s.Dx, size = 10000)
		if dist == 'uniform':  _ = ss.uniform.rvs(s.Dx, size = 10000)
		if dist == 'halfnorm': _ = ss.halfnorm.rvs(s.Dx, size = 10000)
		h_exp = np.histogram(_, 14)[0]
		h_exp = h_exp / np.mean(h_exp)
		print(dist, h_exp, h_obs)
		res.update({dist:{'X':ss.chisquare(h_obs,h_exp), 'K':ss.kstest(nx, dist, [s.Dx])}})

	print(len(nx))
	hist(nx, 14)
	show()
	
	return res

if __name__ == '__main__':
	# parse()
	from testdata import testdata
	d = []
	P = calcP(testdata)
	for reg in P.keys():
		try:
			d += [float(P[reg][4])]
		except ValueError: 
			d += [0]
		except IndexError: 
			d += [0]

	r = get_best_distr(d, ['norm', 'expon', 'uniform', 'lognorm', 'halfnorm'])
	print(r, d)

	# Результат усреднения
	# Регион / Показатель / Показатель
	# За год.

	# Результат расчета Параметров
	# Регион / Параметр / Параметр
	# За год.

	# Определение закона распределения параметров
	# Показать графики и выбрать закон
	
	# Результат нечеткого преобразования
	# Регион В ВС С НС Н

	# Результат расчета оценки 
	# Регион / CL / BL / R
	# За год

	# 3D

  # "TIV_R": {
  #   "Среднемесячная заработная плата": 25087,
  #   "Объем кредитов": 12290867750,
  #   "Количество филиалов": 3,
  #   "Остатки бюджета": 15000000,
  #   "Общий объем прибыли/убытков": 3500000,
  #   "Количество организаций": 1,
  #   "Валовый региональный продукт": 41298700000,
  #   "Всего организаций": 4,
  #   "Просроченная задолженность": 375304333
  # },
  # "RZ": {
  #   "Среднемесячная заработная плата": 21796,
  #   "Объем кредитов": 58710456833,
  #   "Количество филиалов": 14,
  #   "Остатки бюджета": 8000000,
  #   "Общий объем прибыли/убытков": 293300000,
  #   "Количество организаций": 4,
  #   "Валовый региональный продукт": 279286500000,
  #   "Всего организаций": 18,
  #   "Просроченная задолженность": 2652958083
  # },