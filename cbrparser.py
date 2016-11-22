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

def parse(url):
	res = dict()
	soup = BeautifulSoup(requests.get(url).content)
	for td in soup.findAll('td'):
		if td.text == '01.01.2013': # TODO : get from URL
			break

	table = td.parent.parent
	for tr in table('tr'):
		try:
			_date = tr('td')[0].contents[0]
			n1 = tr('td')[1].nobr.contents[0]
			n2 = tr('td')[2].nobr.contents[0]
			n3 = tr('td')[3].nobr.contents[0]
			n4 = tr('td')[4].nobr.contents[0]
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

if __name__ == '__main__':
	x = crowl('https://www.cbr.ru/region/')
	# x = parse('https://www.cbr.ru/region/IndicatorTable?region=BELG&indicator=Table1.2&year=2013')
	print(dumps(x, ensure_ascii=0, indent=2))

