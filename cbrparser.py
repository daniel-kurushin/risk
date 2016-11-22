# -*- coding: utf-8 -*-
import requests
import re
import sys

from bs4 import BeautifulSoup
from json import dumps

def crowl(url = 'https://www.cbr.ru/region/'):

	def get_reg_name_code_from_ahref(a):
		_name = a.contents[0]
		try:
			_code = re.search('region=(?P<code>.*?)($|&)',a['href']).group('code')
		except AttributeError:
			_code = ''
		return(_name, _code)

	res = dict()
	soup = BeautifulSoup(requests.get(url).content)

	for li in soup.find('ul', {"class" : "nodash without_dash regions_okrug"}).findAll('li',recursive=False):
		regres = dict()
		try:
			for a in li.ul.findAll('a'):
				_name, _code = get_reg_name_code_from_ahref(a)
				print("         ", _name, file=sys.stderr)
				regres.update({_code:{'name':_name}})
			_name, _code = get_reg_name_code_from_ahref(li.a)
			print(_name, file=sys.stderr)
			res.update({_code:{'name':_name,'subs':regres}})
		except AttributeError:
			pass

	return res

def koif_by_month(year = 2013, region = 'VORO'):
	""" Kоличество действующих кредитных организаций и их филиалов """
	url = 'https://www.cbr.ru/region/IndicatorTable?region=%s&indicator=Table1.2&year=%s' % (region, year)

	res = dict()
	soup = BeautifulSoup(requests.get(url).content)
	for td in soup.findAll('td'):
		if td.text == '01.01.%s' % (year):
			break

	table = td.parent.parent
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
			print(e)
	return res


def krob_by_month(year = 2013, region = 'VORO'):
	""" Данные об объеме кредитов, депозитов и прочих размещенных средств в рублях """
	url = 'https://www.cbr.ru/region/IndicatorTable?region=%s&indicator=Tab28.2&year=%s' % (region, year)

	res = dict()
	soup = BeautifulSoup(requests.get(url).content)
	for td in soup.findAll('td'):
		if td.text == '01.01.%s' % (year):
			break

	table = td.parent.parent
	for tr in table('tr'):
		try:
			_date = tr('td')[0].contents[0]
			n1 = int(tr('td')[1].nobr.contents[0].replace(' ',''))
			n2 = int(tr('td')[2].nobr.contents[0].replace(' ',''))
			n3 = int(tr('td')[3].nobr.contents[0].replace(' ',''))
			n4 = int(tr('td')[4].nobr.contents[0].replace(' ',''))
			res.update({
			_date:{
			'Объем кредитов': n1,
			'Кредиты нефинансовым организациям': n2,
			'Кредиты кредитным организациям': n3,
			'Кредиты физическим лицам': n4,
			}})
		except Exception as e:
			print(e)
	return res

def przd_by_month(year = 2013, region = 'VORO'):
	""" Данные о просроченной задолженности по кредитам, депозитам и прочим размещенным средствам """
	url = 'https://www.cbr.ru/region/IndicatorTable?region=%s&indicator=Tab30.2&year=%s' % (region, year)
           
	res = dict()
	soup = BeautifulSoup(requests.get(url).content)
	for td in soup.findAll('td'):
		if td.text == '01.01.%s' % (year):
			break

	table = td.parent.parent
	for tr in table('tr'):
		try:
			_date = tr('td')[0].contents[0]
			n1 = int(tr('td')[1].nobr.contents[0].replace(' ',''))
			n2 = int(tr('td')[3].nobr.contents[0].replace(' ',''))
			n3 = int(tr('td')[5].nobr.contents[0].replace(' ',''))
			n4 = n1 + n2 + n3
			res.update({
			_date:{
			'Просроченная задолженность нефинансовых организаций': n1,
			'Просроченная задолженность кредитных организаций': n2,
			'Просроченная задолженность физических лиц': n3,
			'Всего просроченная задолженность': n4,
			}})
		except Exception as e:
			print(e)
	return res


if __name__ == '__main__':
	# x = crowl('https://www.cbr.ru/region/')
	# x = koif_by_month(region='BELG', year='2013')
	# x = krob_by_month(region='BELG', year='2013')
	x = przd_by_month(region='BELG', year='2013')
	print(dumps(x, ensure_ascii=0, indent=2))


