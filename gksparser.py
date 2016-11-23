from openpyxl import load_workbook
from json import dumps

def test():
	wb = load_workbook('data/vrp98-14.xlsx')
	print(wb.get_sheet_names())
	years = get_years(wb.get_sheet_by_name('Лист1'))
	x = get_region_data(wb.get_sheet_by_name('Лист1'), years)
	print(dumps(x, ensure_ascii=0, indent=2))

def get_years(worksheet):
	res = dict()

	for x in [chr(x) for x in range(66,91)]:
		try:
			year = worksheet['%s6' % (x)].value.strip(' г.')
			res.update({x:year})
		except AttributeError:
			break
	return res

def get_region_data(worksheet, years):
	_min = 9
	_max = int(str(worksheet.dimensions).split(':')[1][1:])

	res = dict()

	for row in range(_min, _max):
		region = worksheet['A%s' % (row)]
		if region.fill.bgColor.rgb == '00000000':
			resres = dict()
			for col in years.keys():
				_date = '31.12.%s' % (years[col])
				try:
					n1   = int(worksheet['%s%s' % (col,row)].value)
				except ValueError:
					n1   = 0
				except TypeError:					
					n1   = 0
				resres.update({_date:int(n1 * 1000000)})
			res.update({str(region.value).strip():resres})
	return res

if __name__ == '__main__':
	test()