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
		
		res.update({r[0]:{'Количество филиалов':n2,'Количество организаций':n3,'Всего':n1}})
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

def parse():
	x = get_regions()
	koif = summ_koif(x[:4])
	print(dumps(koif, ensure_ascii=0, indent=2))

	przd = summ_przd(x[:4])
	print(dumps(przd, ensure_ascii=0, indent=2))

	krob = summ_krob(x[:4])
	print(dumps(krob, ensure_ascii=0, indent=2))

	frdko = summ_frdko(2013)
	ostb = ostbs_by_month() 
	print(dumps(ostb, ensure_ascii=0, indent=2))
	# 
	# frdk = frdko_by_month() 

	# for x in [crvl]:#[koif,krob,przd,frdk,ostb]:
		# print(dumps(x, ensure_ascii=0, indent=2))

if __name__ == '__main__':
	parse()


