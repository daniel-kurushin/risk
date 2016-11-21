# -*- coding: utf-8 -*-
import requests
import re

from bs4 import BeautifulSoup

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
	x = parse('https://www.cbr.ru/region/IndicatorTable?region=BELG&indicator=Table1.2&year=2013')
	print(x)

