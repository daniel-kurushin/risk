from cbrparser import *
from gksparser import *
from json import dumps

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

def get_regions1():
	return [
		"Республика Марий Эл",
		"Республика Алтай",
		"Магаданская область",
		"г. Санкт-Петербург",
		"Челябинская область",
		"Удмуртская Республика",
		"Тамбовская область",
		"Астраханская область",
		"Новосибирская область",
		"Псковская область",
		"Костромская область",
		"Оренбургская область",
		"Республика Бурятия",
		"Кабардино-Балкарская Республика",
		"Кемеровская область",
		"Республика Ингушетия",
		"Алтайский край",
		"Тюменская область",
		"Саратовская область",
		"Самарская область",
		"Ярославская область",
		"г. Москва",
		"Мурманская область",
		"Ульяновская область",
		"Владимирская область",
		"Брянская область",
		"Республика Тыва",
		"Пензенская область",
		"Краснодарский край",
		"Еврейская автономная область",
		"Ленинградская область",
		"в том числе Ненецкий автономный округ",
		"Республика Мордовия",
		"Забайкальский край",
		"Курганская область",
		"Липецкая область",
		"Калужская область",
		"Сахалинская область",
		"Республика Адыгея (Адыгея)",
		"Калининградская область",
		"Вологодская область",
		"Курская область",
		"Республика Татарстан (Татарстан)",
		"Ивановская область",
		"Республика Саха (Якутия)",
		"Белгородская область",
		"Республика Северная Осетия - Алания",
		"Омская область",
		"Приморский край",
		"Тульская область",
		"Чукотский автономный округ",
		"Смоленская область",
		"Республика Коми",
		"Карачаево-Черкесская Республика",
		"Тверская область",
		"в том числе Ямало-Ненецкий автономный округ",
		"Пермский край",
		"Республика Башкортостан",
		"Красноярский край",
		"Ставропольский край",
		"Орловская область",
		"Волгоградская область",
		"Республика Карелия",
		"Амурская область",
		"Чувашская Республика - Чувашия",
		"Архангельская область",
		"Свердловская область",
		"Рязанская область",
		"Кировская область",
		"Воронежская область",
		"Камчатский край",
		"Московская область",
		"Ростовская область",
		"Томская область",
		"Республика Калмыкия",
		"Иркутская область",
		"Республика Дагестан",
		"Республика Хакасия",
		"Новгородская область",
		"Чеченская Республика",
		"в том числе Ханты-Мансийский автономный округ - Югра",
		"Нижегородская область",
		"Хабаровский край",
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
		if compare_names(region[1], name) >= 6/7:
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
		_ = frdko_by_month(year = year + 1, region = r[0])
		try:
			__ = _['01.01.%s' % (year + 1)]
			oo = _filter(__['Общий объем прибыли/убытков, полученных действующими кредитными организациями'])
		except KeyError:
			oo = 0
		
		res.update({r[0]:{"Общий объем прибыли/убытков":oo}})

	return res

def summ_osts(regions, year):
	ostb = ostbs_by_month()
	res = {} 
	for ost in ostb.keys():
		print(ost)
		res.update(
			{get_code_by_name(regions, ost):ostb[ost]}
		)
	return res

def parse():
	print(compare_names('Ненецкий автономный округ', 'в том числе Ямало-Ненецкий автономный округ'))
	print(compare_names('в том числе (Ямало-Ненецкий) автономный г. округ', 'Ненецкий автономный округ'))
	x = get_regions()
	y = get_regions1()
	for r1 in x:
		l = {}
		for r2 in y:
			k = compare_names(r1[1],r2)
			l.update({k:(r1[1],r2)})
		m = max(list(l.keys()))
		print(l[m], m, flush = 1)

	exit(1)
	print(dumps(x, ensure_ascii=0, indent=2))
	# koif = summ_koif(x[:4])
	# print(dumps(koif, ensure_ascii=0, indent=2))

	# przd = summ_przd(x[:4])
	# print(dumps(przd, ensure_ascii=0, indent=2))

	# krob = summ_krob(x[:4])
	# print(dumps(krob, ensure_ascii=0, indent=2))

	# frdko = summ_frdko(2013)
	# print(dumps(frdko, ensure_ascii=0, indent=2))

	# ostb = summ_osts(x, 2013)
	# print(dumps(ostb, ensure_ascii=0, indent=2))


	# 
	# frdk = frdko_by_month() 

	# for x in [crvl]:#[koif,krob,przd,frdk,ostb]:
		# print(dumps(x, ensure_ascii=0, indent=2))

if __name__ == '__main__':
	parse()


