"""
Определение параметров кредитного риска
модуль реализации нечеткой логики
Курушин Д.С.
Васильева Е.Е.
Долгова Е.В.
"""

import numpy as np
import scipy.stats as ss
from math import log

class FuzzyVar(object):
	"""элемент нечеткого множества"""
	def __init__(self, varName = "Семь", 
						 varSem  = {1:0,3:0.4,7:1}):
		self._name = varName
		self._sem = varSem
		x, y = [], []
		for k in self._sem.keys():
			x += [k]
			y += [self._sem[k]]
		self._k = np.polyfit(x,y,20)

	def f(self,x):
		n = len(self._k)-1
		y = 0
		for k in self._k:
			y += k*x**n
			n -= 1
		y += self._k[-1]

		# return y
		if y < 0: 
			return 0
		elif y > 1: 
			return 1
		else: 
			return y

	def __eq__(self, val):
		return self._name == val._name and \
				 self._sem  == val._sem

	def __ne__(self, val):
		return not self.__eq__(val)

def fuzzification(X = np.zeros(79), dist = 'norm'):
	def get_diapason(x, points):
		n = 0
		for p in points:
			if p[0] <= x < p[1]:
				return n
			n += 1

	L = ('H','HC', 'C','BC', 'B')
	K = (0.1, 0.3, 0.5, 0.7, 0.9)
	Y = (
		(0.9,1.0),#0
		(1.0,0.5),#1
		(0.5,1.0),#2
		(1.0,0.5),#3
		(0.5,1.0),#4
		(1.0,0.5),#5
		(0.5,1.0),#6
		(1.0,0.5),#7
		(0.5,1.0),#8
		(1.0,0.9),#9
	)
	if dist == 'norm':
		points = (
			(-10000,-1.645),#0
			(-1.645,-1.122),#1
			(-1.122,-0.598),#2
			(-0.598,-0.299),#3
			(-0.299, 0.000),#4
			( 0.000, 0.299),#5
			( 0.299, 0.598),#6
			( 0.598, 1.122),#7
			( 1.122, 1.645),#8
			( 1.645, 10000),#9
			)
	if dist == 'lognorm':
		points = (
			(-1.645,-1.122),#забить
			(-1.122,-0.598),
			(-0.598,-0.299),
			(-0.299, 0.000),
			( 0.000, 0.299),
			( 0.299, 0.598),
			( 0.598, 1.122),
			( 1.122, 1.645),
			)
	if dist == 'expon':
		points = (
			(-1.645,-1.122),
			(-1.122,-0.598),
			(-0.598,-0.299),
			(-0.299, 0.000),
			( 0.000, 0.299),
			( 0.299, 0.598),
			( 0.598, 1.122),
			( 1.122, 1.645),
			)

	res = []
	for x in X:
		n = get_diapason(x, points)
		x1, x2 = points[n]
		y1, y2 = Y[n]
		l = L[int(n/2)]
		k = K[int(n/2)]
		a, b = np.polyfit([x1,x2],[y1,y2],1)
		res += [((a * x + b) * k, l)]
		
	return res

def CL_BL_rangin(X = np.array([(0.5, 'C'),])):
	_ = np.array(np.rot90(X)[1],dtype=float)
	X_ = np.mean(_)
	X__ = np.std(_)
	r = (X__) * (-2 * log(1 - 0.33))**0.5
	res = []
	for x in X:
		if -10000 <= x[0] < X_ - r : l = 'H'
		if X_ - r <= x[0] < X_ + r : l = 'C'
		if X_ + r <= x[0] < +10000 : l = 'B'
		res += [(x[0], l)]

	return res

def R(cl_i = (0.3,'H'), bl_i = (0.3,'H')):
	r = None
	if cl_i[1] == 'H':
		if bl_i[1] == 'H': r = 'C'
		if bl_i[1] == 'C': r = 'HC'
		if bl_i[1] == 'B': r = 'H'
	if cl_i[1] == 'C':
		if bl_i[1] == 'H': r = 'BC'
		if bl_i[1] == 'C': r = 'C'
		if bl_i[1] == 'B': r = 'HC'
	if cl_i[1] == 'B':
		if bl_i[1] == 'H': r = 'B'
		if bl_i[1] == 'C': r = 'BC'
		if bl_i[1] == 'B': r = 'C'

	p = (cl_i[0], 
		 bl_i[0], 
		 0.5 * cl_i[0] - 0.5 * bl_i[0] + 0.5)

	return (p, r)


if __name__ == '__main__':
	print(fuzzification(ss.norm.rvs(size=79)))

"""
		 P N Mu
P1 [(1,a,0.1),(2,b,0.1),(3...),(4...),(5...)]
P2 [(1,b,0.3),(2,b,0.1),(3...),(4...),(5...)]
P2 [(1,f,0.3),(2,b,0.1),(3...),(4...),(5...)]
P4 [(1,a,0.3),(2,b,0.1),(3...),(4...),(5...)]

P6 [(1,a,0.3),(2,b,0.1),(3...),(4...),(5...)]
P7 [(1,a,0.3),(2,b,0.1),(3...),(4...),(5...)]
P8 [(1,a,0.3),(2,b,0.1),(3...),(4...),(5...)]
P9 [(1,a,0.3),(2,b,0.1),(3...),(4...),(5...)]

+++ Neuron
abs(w)
sort w
w(i) = 2(n(P) - i + 1)/(n(P) + 1)n(P)


In [1]: P = [0.46, 0.59, 0.71, 0.76, 0.61]

In [2]: P1 = [0.46, 0.59, 0.71, 0.76, 0.61]

In [3]: import numpy as np

In [4]: import matplotlib.pyplot as plt

In [5]: import scipy.stats as ss

In [6]: np.histogram(P)
Out[6]: 
(array([1, 0, 0, 0, 1, 1, 0, 0, 1, 1]),
 array([ 0.46,  0.49,  0.52,  0.55,  0.58,  0.61,  0.64,  0.67,  0.7 ,
				 0.73,  0.76]))

In [7]: np.histogram(P,4)
Out[7]: (array([1, 1, 1, 2]), array([ 0.46 ,  0.535,  0.61 ,  0.685,  0.76 ]))

In [8]: H = np.histogram(P,4)

In [9]: h[1]
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
<ipython-input-9-af64c243f603> in <module>()
----> 1 h[1]

NameError: name 'h' is not defined

In [10]: H = np.histogram(P,4)[0]

In [11]: H
Out[11]: array([1, 1, 1, 2])

In [12]: H[1]
Out[12]: 1

In [13]: H[-1]
Out[13]: 2

In [14]: Pi = H / 5

In [15]: Pi
Out[15]: array([ 0.2,  0.2,  0.2,  0.4])

In [16]: P1 = [0.46, 0.59, 0.71, 0.76, 0.61]

In [17]: from student import *

In [18]: p = Student(P1)

In [19]: p.X
Out[19]: 0.63

In [20]: p.Dx
Out[20]: 0.14

In [21]: p1 = Student(P1)

In [22]: (P1 - pX)/p.Dx
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
<ipython-input-22-91488182183e> in <module>()
----> 1 (P1 - pX)/p.Dx

NameError: name 'pX' is not defined

In [23]: (P1 - p.X)/p.Dx
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-23-17217526f0c0> in <module>()
----> 1 (P1 - p.X)/p.Dx

TypeError: unsupported operand type(s) for -: 'list' and 'float'

In [24]: (np.array(P1) - p.X)/p.Dx
Out[24]: array([-1.21428571, -0.28571429,  0.57142857,  0.92857143, -0.14285714])

In [25]: Ps = (np.array(P1) - p.X)/p.Dx

In [26]: Ps
Out[26]: array([-1.21428571, -0.28571429,  0.57142857,  0.92857143, -0.14285714])

In [27]: P1
Out[27]: [0.46, 0.59, 0.71, 0.76, 0.61]

In [28]: np.histogram(Ps,4)
Out[28]: 
(array([1, 2, 0, 2]),
 array([-1.21428571, -0.67857143, -0.14285714,  0.39285714,  0.92857143]))

In [29]: H = np.histogram(Ps,4)[1]

In [30]: H
Out[30]: array([-1.21428571, -0.67857143, -0.14285714,  0.39285714,  0.92857143])

In [31]: H = np.histogram(Ps,4)[0]

In [32]: H
Out[32]: array([1, 2, 0, 2])

In [33]: H = np.histogram(Ps,4)[0]/5

In [34]: H
Out[34]: array([ 0.2,  0.4,  0. ,  0.4])

In [35]: np.histogram(Ps,4)
Out[35]: 
(array([1, 2, 0, 2]),
 array([-1.21428571, -0.67857143, -0.14285714,  0.39285714,  0.92857143]))

In [36]: P2 = ss.norm.rvs(size=1000)

In [37]: p2 = Student(P2)

In [38]: P2s = (P2 - p2.X)/p2.Dx

In [39]: P2s


In [40]: np.histogram(P2s,14)
Out[40]: 
(array([  6,  13,  23,  71, 108, 163, 171, 158, 134,  81,  50,  20,   0,   2]),
 array([-41.80914779, -35.55964274, -29.31013769, -23.06063264,
				-16.81112759, -10.56162254,  -4.31211749,   1.93738757,
					8.18689262,  14.43639767,  20.68590272,  26.93540777,
				 33.18491282,  39.43441787,  45.68392292]))

In [41]: H2 = np.histogram(P2s,14)[0]

In [42]: H2 /1000
Out[42]: 
array([ 0.006,  0.013,  0.023,  0.071,  0.108,  0.163,  0.171,  0.158,
				0.134,  0.081,  0.05 ,  0.02 ,  0.   ,  0.002])

In [43]: x = H2/1000

In [44]: y = np.histogram(P2s,14)[1][1:]

In [45]: len(x)
Out[45]: 14

In [46]: len(y)
Out[46]: 14

In [47]: plt.plot(x,y)
Out[47]: [<matplotlib.lines.Line2D at 0x7fe9170b0be0>]

In [48]: plt.show()

In [49]: Ps
Out[49]: array([-1.21428571, -0.28571429,  0.57142857,  0.92857143, -0.14285714])

In [50]: P1
Out[50]: [0.46, 0.59, 0.71, 0.76, 0.61]

In [51]: L = {-0.59:'low', 0:'mid', 0.59:'hig'}

In [52]: for p in P1:
		...:     l = []
		...:     for k in L.keys():
		...:         l += abs(p-k)
		...:     
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-52-755dd0b36d07> in <module>()
			2     l = []
			3     for k in L.keys():
----> 4         l += abs(p-k)
			5 

TypeError: 'float' object is not iterable

In [53]: for p in P1:
		...:     l = []
		...:     for k in L.keys():
		...:         l += [abs(p-k)]    
		...:         

In [54]: l
Out[54]: [1.2, 0.61, 0.020000000000000018]

In [55]: for p in P1:
		...:     l = []
		...:     for k in L.keys():
		...:         l += [abs(p-k)]    
		...:     print(p, l)
		...:     
0.46 [1.05, 0.46, 0.12999999999999995]
0.59 [1.18, 0.59, 0.0]
0.71 [1.2999999999999998, 0.71, 0.12]
0.76 [1.35, 0.76, 0.17000000000000004]
0.61 [1.2, 0.61, 0.020000000000000018]

In [56]: for p in Ps:
		...:     l = []
		...:     for k in L.keys():
		...:         l += [abs(p-k)]    
		...:     print(p, l)
		...:     
-1.21428571429 [0.624285714285714, 1.214285714285714, 1.8042857142857138]
-0.285714285714 [0.30428571428571405, 0.28571428571428592, 0.87571428571428589]
0.571428571429 [1.161428571428571, 0.57142857142857106, 0.018571428571428905]
0.928571428571 [1.5185714285714285, 0.92857142857142849, 0.33857142857142852]
-0.142857142857 [0.44714285714285701, 0.14285714285714296, 0.73285714285714287]

In [57]: -1.2*0.1
Out[57]: -0.12

In [58]: -0.2*0.1
Out[58]: -0.020000000000000004

In [59]: 0.57*0.9
Out[59]: 0.513

In [60]: Pss = [-0.12, -0.02, 0.51, 0.90, -0.14*0.5]

In [61]: Pss
Out[61]: [-0.12, -0.02, 0.51, 0.9, -0.07]

In [62]: P1
Out[62]: [0.46, 0.59, 0.71, 0.76, 0.61]

In [63]: [-1.12,-0,598]
Out[63]: [-1.12, 0, 598]

In [64]: x = [-1.12,-0,598]

In [65]: y = [0.5, 1]

In [66]: np.polyfit(x,y,1)
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-66-5b35a4021fda> in <module>()
----> 1 np.polyfit(x,y,1)

/usr/lib/python3/dist-packages/numpy/lib/polynomial.py in polyfit(x, y, deg, rcond, full, w, cov)
		553         raise TypeError("expected 1D or 2D array for y")
		554     if x.shape[0] != y.shape[0] :
--> 555         raise TypeError("expected x and y to have same length")
		556 
		557     # set rcond

TypeError: expected x and y to have same length

In [67]: x = [-1.12,-0.598]

In [68]: np.polyfit(x,y,1)
Out[68]: array([ 0.95785441,  1.57279693])

In [69]: Pss = [0.62, 0.30, 0.01, 0.33, 0.14]

In [70]: P1
Out[70]: [0.46, 0.59, 0.71, 0.76, 0.61]


[([float(p1),[float(p2),float(p3),float(p4),float(p5)]],[float(p6),[float(p7),float(p8),float(p9),float(p10)]])]

[[0.2883,	0.2674,	0.2302,	0.0611][0.2632,	0.2832,	0.4936,	0.3534]]
[0.2418,0.1535]In [18]: 

from sklearn import linear_model    

In [18]: from sklearn import linear_model

In [19]: data = open('data/aaa.csv').readlines()

In [20]: for p1,p2,p3,p4,p5,p6,p7,p8,p9,p10 in [_.strip('\n').replace(',','.').split('^') for _ i
		...: n data]:
		...:     P += [([float(p1),[float(p2),float(p3),float(p4),float(p5)]],[float(p6),[float(p7),f
		...: loat(p8),float(p9),float(p10)]])]
		...:     
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
<ipython-input-20-33d9dec61a3c> in <module>()
			1 for p1,p2,p3,p4,p5,p6,p7,p8,p9,p10 in [_.strip('\n').replace(',','.').split('^') for _ in data]:
----> 2     P += [([float(p1),[float(p2),float(p3),float(p4),float(p5)]],[float(p6),[float(p7),float(p8),float(p9),float(p10)]])]
			3 

NameError: name 'P' is not defined

In [21]: P = []

In [22]: for p1,p2,p3,p4,p5,p6,p7,p8,p9,p10 in [_.strip('\n').replace(',','.').split('^') for _ i
		...: n data]:
		...:     P += [([float(p1),[float(p2),float(p3),float(p4),float(p5)]],[float(p6),[float(p7),f
		...: loat(p8),float(p9),float(p10)]])]
		...:     

In [23]: x1 = np.array([p[0][0] for p in P])

In [24]: y1 = np.array([p[0][1] for p in P])

In [25]: x1[:10]
Out[25]: 
array([ 0.2418,  0.1535,  0.3854,  0.2573,  0.4138,  0.2836,  0.3716,
				0.3159,  0.2877,  0.9   ])

In [26]: y1[:10]
Out[26]: 
array([[ 0.2883,  0.2674,  0.2302,  0.0611],
			 [ 0.2632,  0.2832,  0.4936,  0.3534],
			 [ 0.2841,  0.1915,  0.1552,  0.3534],
			 [ 0.1844,  0.2769,  0.4896,  0.2596],
			 [ 0.1894,  0.0514,  0.2759,  0.5   ],
			 [ 0.5283,  0.2787,  0.6299,  0.4405],
			 [ 0.2287,  0.281 ,  0.2802,  0.4039],
			 [ 0.4345,  0.4128,  0.0729,  0.2667],
			 [ 0.209 ,  0.2266,  0.2612,  0.2875],
			 [ 0.209 ,  0.3793,  0.3507,  0.2625]])

In [27]: clf.fit(y1, x1)
Out[27]: LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)

In [28]: clf.coef_
Out[28]: array([ 0.25716542,  0.40238967,  0.00830494,  0.21902738])

In [29]: help(linear_model.LinearRegression)


In [30]: clf = linear_model.LinearRegression(normalize=1)

In [31]: clf.fit(y1, x1)
Out[31]: LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=1)

In [32]: clf.coef_
Out[32]: array([ 0.25716542,  0.40238967,  0.00830494,  0.21902738])

In [33]: clf = linear_model.LinearRegression(normalize=0)

In [34]: clf.fit(y1, x1)
Out[34]: LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=0)

In [35]: clf.coef_
Out[35]: array([ 0.25716542,  0.40238967,  0.00830494,  0.21902738])

In [36]: clf = linear_model.LinearRegression(normalize=)
	File "<ipython-input-36-855d04ff8f4d>", line 1
		clf = linear_model.LinearRegression(normalize=)
																									^
SyntaxError: invalid syntax


In [37]: clf = linear_model.LinearRegression(normalize=False)

In [38]: clf.fit(y1, x1)
Out[38]: LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)

In [39]: clf.coef_
Out[39]: array([ 0.25716542,  0.40238967,  0.00830494,  0.21902738])

In [40]: help(linear_model.LinearRegression)


In [41]: clf = linear_model.LinearRegression(normalize=False, fit_intercept=False)\
		...: 

In [42]: clf.fit(y1, x1)
Out[42]: LinearRegression(copy_X=True, fit_intercept=False, n_jobs=1, normalize=False)

In [43]: clf.coef_
Out[43]: array([ 0.27417606,  0.43545207,  0.03455458,  0.2600535 ])

In [44]: clf = linear_model.LinearRegression(normalize=True, fit_intercept=False)

In [45]: clf.fit(y1, x1)
Out[45]: LinearRegression(copy_X=True, fit_intercept=False, n_jobs=1, normalize=True)

In [46]: clf.coef_
Out[46]: array([ 0.27417606,  0.43545207,  0.03455458,  0.2600535 ])

In [47]: help(linear_model.LinearRegression)


In [48]: x1 = np.array([p[1][0] for p in P])

In [49]: y1 = np.array([p[1][1] for p in P])

In [50]: clf.fit(y1, x1)
Out[50]: LinearRegression(copy_X=True, fit_intercept=False, n_jobs=1, normalize=True)

In [51]: clf.coef_
Out[51]: array([ 0.53422726,  0.4026561 , -0.00910951,  0.05515987])

In [52]: clf = linear_model.LinearRegression()

In [53]: clf.fit(y1, x1)
Out[53]: LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)

In [54]: clf.coef_
Out[54]: array([ 0.47258108,  0.38747025, -0.08080565,  0.01457216])

In [55]: help(linear_model.LinearRegression)

CL = [0.2331,0.2594,0.2467,0.2638,0.2744,0.3753,0.3170,0.3427,0.2538,0.4594,0.4313,0.2569,0.4986,0.2250,0.2302,0.7736,0.3708,0.6593,0.1761,0.3325,0.2977,0.4611,0.5438,0.2038,0.3470,0.2479,0.4915,0.3303,0.4514,0.6289,0.1363,0.3300,0.5347,0.1342,0.1515,0.1790,0.3564,0.2205,0.2366,0.4440,0.4841,0.4618,0.5132,0.4392,0.4587,0.3142,0.4918,0.3269,0.6515,0.2803,0.2586,0.3942,0.2610,0.4157,0.3585,0.6262,0.7256,0.5375,0.4183,0.5371,0.4107,0.3681,0.4119,0.2310,0.4364,0.4554,0.5675,0.6609,0.4894,0.3125,0.3848,0.2995,0.5012,0.5816,0.3213,0.3120,0.2754,0.1437,0.2081]
BL = [0.2662,0.2571,0.2909,0.2460,0.4271,0.2710,0.4720,0.4476,0.5983,0.5591,0.3611,0.3277,0.5198,0.3242,0.3943,0.3582,0.4380,0.7783,0.4213,0.5093,0.4727,0.7346,0.3486,0.3846,0.4911,0.2825,0.4100,0.5029,0.3492,0.4261,0.2814,0.4835,0.3811,0.1893,0.6237,0.4505,0.5554,0.6490,0.1445,0.3078,0.2534,0.7748,0.1564,0.3204,0.3568,0.4406,0.3205,0.4189,0.2594,0.4114,0.2357,0.4911,0.3596,0.2246,0.2194,0.5219,0.2592,0.4591,0.6126,0.3991,0.4075,0.2889,0.6841,0.1510,0.3563,0.3161,0.3710,0.3549,0.4120,0.3212,0.1661,0.2211,0.2799,0.4480,0.1731,0.1347,0.2208,0.4356,0.0933]

In [132]: ss.chisquare(np.histogram(CL,11)[0],[ 2,  2,  6, 10, 12, 15, 12, 10,  6,  2,  2])
Out[132]: (54.216666666666661, 4.4215716103331017e-08)

In [133]: ss.chisquare(np.histogram(CL,11)[0],[ 2,  2,  6, 10, 12, 15, 12, 10,  6,  2,  2])
Out[133]: (54.216666666666661, 4.4215716103331017e-08)

In [134]: ss.chisquare(np.histogram(CL,11)[0],[ 2,  2,  6, 10, 12, 15, 12, 10,  6,  2,  2])
Out[134]: (54.216666666666661, 4.4215716103331017e-08)

In [135]: ss.chisquare(np.histogram(CL,11)[0],[ 6, 10, 11, 13,  9, 10, 10,  3,  3,  2,  2])
Out[135]: (0.0, 1.0)

In [136]: ss.chisquare(np.histogram(CL,11)[0],[ 6,  9, 11, 13, 10, 10, 10,  3,  3,  2,  2])
Out[136]: (0.21111111111111111, 0.99999989998372141)

In [137]: ss.chisquare(np.histogram(CL,11)[0],[ 5,  9, 11, 10, 10, 12, 10,  3,  3,  2,  2])
Out[137]: (1.6444444444444446, 0.99841056671114792)

In [138]: ss.chisquare(np.histogram(CL,11)[0],[ 5,  9, 11, 10, 12, 12, 10,  3,  3,  2,  2])
Out[138]: (2.2944444444444447, 0.99354480619995644)

In [139]: ss.chisquare(np.histogram(CL,11)[0],[ 5,  8, 11, 10, 12, 12, 10,  3,  3,  2,  2])
Out[139]: (2.6833333333333336, 0.98792639120043713)

In [140]: ss.chisquare(np.histogram(CL,11)[0],[ 5,  8, 11, 10, 12, 12, 10,  5,  3,  2,  2])
Out[140]: (3.4833333333333334, 0.96766125701047045)

In [141]: ss.chisquare(np.histogram(BL,11)[0],[ 5,  8, 11, 10, 12, 12, 10,  5,  3,  2,  2])
Out[141]: (6.7303030303030305, 0.75063702787118525)

In [157]: np.std(CL)
Out[157]: 0.14507307608326964

In [158]: np.mean(CL)
Out[158]: 0.38015569620253165

In [159]: np.std(BL)
Out[159]: 0.14760374080826291

In [160]: np.mean(BL)
Out[160]: 0.38058860759493673

In [161]: 0.145 * (-2 * log(1 - 0.5))**0.5
Out[161]: 0.1707244532647438

In [162]: 0.14507307608326964 * (-2 * log(1 - 0.5))**0.5
Out[162]: 0.17081049377759167

In [163]: 0.1424 * (-2 * log(1 - 0.5))**0.5
Out[163]: 0.1676631872062036

In [164]: 0.1424 * (-2 * log(1 - 0.7))**0.5
Out[164]: 0.22097000508054612

In [165]: 0.1424 * (-2 * log(1 - 0.6))**0.5
Out[165]: 0.19277097059032755

In [166]: 0.1424 * (-2 * log(1 - 0.5))**0.5
Out[166]: 0.1676631872062036

In [167]: 0.1424 * (-2 * log(1 - 0.3333))**0.5
Out[167]: 0.12822566270398267

In [172]: np.mean(BL)
Out[172]: 0.38058860759493673

In [173]: M = np.mean(BL)

In [174]: M - 0.128
Out[174]: 0.25258860759493673

In [175]: M + 0.128
Out[175]: 0.50858860759493674

In [176]: [0.0933, 0.2525, 0.5085, 0.7783]
Out[176]: [0.0933, 0.2525, 0.5085, 0.7783]

In [177]: BL[59]
Out[177]: 0.3991

In [178]: 0.5085 - 0.2525
Out[178]: 0.25599999999999995

In [179]: 0.5085 - 0.2525 + 0.2525
Out[179]: 0.5085

In [180]: (0.5085 - 0.2525) / 2 + 0.2525
Out[180]: 0.38049999999999995

In [181]: np.polyfit([0.3805, 0.5085], [1, 0],1)
Out[181]: array([-7.8125    ,  3.97265625])

In [182]: -7.8125 * BL[59] + 3.97265625
Out[182]: 0.8546874999999998

In [183]: [BL[59], CL[59], -7.8125 * BL[59] + 3.97265625]
Out[183]: [0.3991, 0.5371, 0.8546874999999998]

In [184]: [BL[59], CL[59], (-7.8125 * BL[59] + 3.97265625) * 0.5]
Out[184]: [0.3991, 0.5371, 0.4273437499999999]

"""



