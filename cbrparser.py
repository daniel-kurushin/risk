# -*- coding: utf-8 -*-
import requests
import re
import sys

from bs4 import BeautifulSoup
from json import dumps

from utils import _get_my_name

percent_done = 0

def progress(value = 'reset'):
	global percent_done
	if value == 'reset':
		percent_done = 0
	else:
		percent_done += value

def crowl(url = 'https://www.cbr.ru/region/'):
	""" коды регионов """

	def get_reg_name_code_from_ahref(a):
		_name = a.contents[0]
		try:
			_code = re.search('region=(?P<code>.*?)($|&)',a['href']).group('code')
		except AttributeError:
			_code = ''
		return(_name, _code)

	progress()
	res = dict()
	soup = BeautifulSoup(requests.get(url).content)
	progress(10)

	_ = soup.find('ul', {"class" : "nodash without_dash regions_okrug"}).findAll('li',recursive=False)
	step = 90 / len(_)
	for li in _:
		regres = dict()
		try:
			for a in li.ul.findAll('a'):
				_name, _code = get_reg_name_code_from_ahref(a)
				# print("         ", _name, file=sys.stderr)
				regres.update({_code:{'name':_name}})
			_name, _code = get_reg_name_code_from_ahref(li.a)
			# print(_name, file=sys.stderr)
			res.update({_code:{'name':_name,'subs':regres}})
		except AttributeError as e:
			print("Exception '%s' in function '%s'" % (e,_get_my_name()), file=sys.stderr)

		progress(step)

	return res

def koif_by_month(year = 2013, region = 'VORO'):
	""" Kоличество действующих кредитных организаций и их филиалов """
	url = 'https://www.cbr.ru/region/IndicatorTable?region=%s&indicator=Table1.2&year=%s' % (region, year)

	res = dict()
	soup = BeautifulSoup(requests.get(url).content)
	for td in soup.findAll('td'):
		if td.text == '01.01.%s' % (year):
			break

	try:
		table = td.parent.parent
	except UnboundLocalError:
		table = lambda x: []
	for tr in table('tr'):
		try:
			_date = tr('td')[0].contents[0]
			n1 = tr('td')[1].nobr.contents[0]
			n2 = tr('td')[2].nobr.contents[0]
			n3 = tr('td')[3].nobr.contents[0]
			n4 = tr('td')[4].nobr.contents[0]
			try:
				n2 = int(n2)
			except ValueError:
				n2 = int(n3) + int(n4)
			res.update({
			_date:{
			'Kоличество кредитных органзаций в регионе': n1,
			'Kоличество филиалов в регионe':{
				'всего': n2,
				'кредитных организаций, головная организация которых находится в данном регионе': n3,
				'кредитных организаций, головная организация которых находится в другом регионе': n4,}
			}})
		except Exception as e:
			print("Exception '%s' in function '%s'" % (e,_get_my_name()), file=sys.stderr)
	return res


def krob_by_month(year = 2013, region = 'VORO'):
	""" Данные об объеме кредитов, депозитов и прочих размещенных средств в рублях """
	url = 'https://www.cbr.ru/region/IndicatorTable?region=%s&indicator=Tab28.2&year=%s' % (region, year)

	res = dict()
	soup = BeautifulSoup(requests.get(url).content)
	for td in soup.findAll('td'):
		if td.text == '01.01.%s' % (year):
			break

	try:
		table = td.parent.parent
	except UnboundLocalError:
		table = lambda x: []
	for tr in table('tr'):
		try:
			_date = tr('td')[0].contents[0]
			n1 = int(tr('td')[1].nobr.contents[0].replace(' ','')) * 1000
			n2 = int(tr('td')[2].nobr.contents[0].replace(' ','')) * 1000
			n3 = int(tr('td')[3].nobr.contents[0].replace(' ','')) * 1000
			n4 = int(tr('td')[4].nobr.contents[0].replace(' ','')) * 1000
			res.update({
			_date:{
			'Объем кредитов': n1,
			'Кредиты нефинансовым организациям': n2,
			'Кредиты кредитным организациям': n3,
			'Кредиты физическим лицам': n4,
			}})
		except Exception as e:
			print("Exception '%s' in function '%s'" % (e,_get_my_name()), file=sys.stderr)
	return res

def przd_by_month(year = 2013, region = 'VORO'):
	""" Данные о просроченной задолженности по кредитам, депозитам и прочим размещенным средствам """
	url = 'https://www.cbr.ru/region/IndicatorTable?region=%s&indicator=Tab30.2&year=%s' % (region, year)

	res = dict()
	soup = BeautifulSoup(requests.get(url).content)
	for td in soup.findAll('td'):
		if td.text == '01.01.%s' % (year):
			break

	try:
		table = td.parent.parent
	except UnboundLocalError:
		table = lambda x: []
	for tr in table('tr'):
		try:
			_date = tr('td')[0].contents[0]
			n1 = int(tr('td')[1].nobr.contents[0].replace(' ','')) * 1000
			n2 = int(tr('td')[3].nobr.contents[0].replace(' ','')) * 1000
			n3 = int(tr('td')[5].nobr.contents[0].replace(' ','')) * 1000
			n4 = n1 + n2 + n3
			res.update({
			_date:{
			'Просроченная задолженность нефинансовых организаций': n1,
			'Просроченная задолженность кредитных организаций': n2,
			'Просроченная задолженность физических лиц': n3,
			'Всего просроченная задолженность': n4,
			}})
		except Exception as e:
			print("Exception '%s' in function '%s'" % (e,_get_my_name()), file=sys.stderr)
	return res

def frdko_by_month(year = 2013, region = 'VORO'):
	""" Финансовые результаты деятельности кредитных организаций """
	url = 'https://www.cbr.ru/region/IndicatorTable?region=%s&indicator=Table1.12&year=%s' % (region, year)

	res = dict()
	soup = BeautifulSoup(requests.get(url).content)
	for td in soup.findAll('td'):
		if td.text == '01.01.%s' % (year):
			break
	try:
		table = td.parent.parent
	except UnboundLocalError:
		table = lambda x: []

	for tr in table('tr'):
		try:
			_date = tr('td')[0].contents[0]
			n1 = int(float(tr('td')[1].nobr.contents[0].replace(' ','').replace(',','.')) * 1000000)
			res.update({
			_date:{
			'Общий объем прибыли/убытков, полученных действующими кредитными организациями': n1,
			}})
		except Exception as e:
			print("Exception '%s' in function '%s'" % (e,_get_my_name()), file=sys.stderr)
	return res

def ostbs_by_month(year=2013):
	from time import sleep
	""" Сведения об остатках бюджетных средств на счетах кредитных организаций """
	res = dict()

	for month in range(1,13):
		sleep(1)
		url = 'https://www.cbr.ru/statistics/UDStat.aspx?Month=%s&Year=%s&TblID=302-25' % (month, year)
		soup = BeautifulSoup(requests.get(url).content)
		for td in soup.findAll('td'):
			if td.text == 'РОССИЙСКАЯ ФЕДЕРАЦИЯ':
				break

		table = td.parent.parent
		for tr in table('tr'):
			try:
				region = tr('td')[0].contents[0]
				if region.upper() != region:
					ostat  = int(
						float(tr('td')[1].contents[0].replace(',','.').replace(' ','')) +
						float(tr('td')[2].contents[0].replace(',','.').replace(' ','')) +
						float(tr('td')[3].contents[0].replace(',','.').replace(' ','')) +
						float(tr('td')[4].contents[0].replace(',','.').replace(' ',''))
					) * 1000000
					_date = '01.%s.%s' % (month, year)
					res.update({
						region:{_date:ostat}
					})
			except Exception as e:
				print("Exception '%s' in function '%s'" % (e,_get_my_name()), file=sys.stderr)
	return res


if __name__ == '__main__':
	x = crowl('https://www.cbr.ru/region/')
	print(dumps(x, ensure_ascii=0, indent=2))
	exit(1)
	# x = koif_by_month(region='BELG', year='2013')
	# x = krob_by_month(region='BELG', year='2013')
	# x = przd_by_month(region='BELG', year='2013')
	x = frdko_by_month(region='MOSK', year='2014')
	# x = ostbs_by_month(2013)
	print(dumps(x, ensure_ascii=0, indent=2))

	# Регион / Показатель / Показатель / Показатель
	# Дырки показать красным
	# дать выбор месяца

	# Потом объединить
	# Показать дедубликацию регионов.

	#
