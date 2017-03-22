"""
Определение параметров кредитного риска
модуль подбора вида распределения
Курушин Д.С.
Васильева Е.Е.
Долгова Е.В.
"""

import math
import scipy.stats as ss
import scipy as sp
import numpy as np
from matplotlib.pyplot import *

def test_student(row = []):
	bn = round(10+math.sqrt(len(row)))
	rn = len(row)
	x = np.linspace(np.min(row), np.max(row) + 10, n * 2)
	a, b, c = ss.t.fit(row,3)
	dd = ss.t.pdf(x, 3, loc = b, scale = c)

	cn, bs = np.histogram(row, bins = bn)
	p_o = np.array(cn, dtype=float)

	tmp = ss.t.cdf(bs, 1.3, loc = b - 0.6, scale = c)
	p_e = []
	for idx, p in enumerate(tmp):
    	if idx == len(tmp) - 1: break
    	p_e.append(tmp[idx+1] - tmp[idx])

	p_e = n*np.array(p_e)

	ctv, pf = ss.chisquare(p_o, np.array(p_e, dtype = float))
	print('Вероятность того, что распределение T подходит к полученным данным: {0:f}'.format(p_f))
	chi_star = np.sum((p_o - p_e) ** 2 / p_e)
	print("chi_star = {}".format(chi_star))
	conf_interval = 0.95
	df = len(bs) - 3
	chi = ss.chi2.ppf(conf_interval, df)
	print("chi = {}".format(chi))

def tes():
	pass

def test_(row = [0,1,2,3,4,5,6,7,8,9,]):
	xs = test_student(row)
	xe = test_expon(row)
	print(xs, xe)

if __name__ == '__main__':
	row = []
	for _ in range(-5,5):
    	row += [_]*int(((5-abs(_))*10)**3)
	test_(row)
