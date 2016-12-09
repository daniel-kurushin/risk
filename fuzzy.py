import numpy as np

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

def test():
for p in Ps:
	l = []
	for k in L.keys():
		l += [abs(p-k)]    
	print(p, l)

if __name__ == '__main__':
	test()

"""
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



"""