import numpy as np

from testdata import perseptrondata, kohonendata

class Neuron(object):
	a =  0.02
	b = -0.04

	def __learn(self,D):
		"""
		Обучение
		"""
		w = self.w[:]
		f = self.__call__
		for d in D:
			x = d[0]
			y = d[1]
			for j in range(len(x)):
				self.w[j] += self.a * (y - f(x)) * x[j]
				return w != self.w

	def __sigma_s(self,x):
		return x

	def __sigma_l(self,x):
		if x < 0:
			return 0
		if x >= 0 and x <= 1:
			return x
		if x > 1:
			return 1

	def __sigma_p(self,x):
		if x > 0:
			return 1
		else:
			return 0

	def __call__(self,x):
		sigma = self.__sigma_s
		s = self.b
		for i in range(len(x)):
			s += self.w[i] * x[i]
			# w = self.w[:]
			# s += (w[0]*x[0]**2 + w[1]*x[1]**2) * (w[4]*(x[0]-w[2])**2 + w[5]*(x[1]-w[3])**2)
		return sigma(s)

	def __init__(self,D):
		"""
		Создание и обучение
		"""
		self.w = [0]*len(D[0][0])
		self.c = 0
		while self.__learn(D):
			self.c += 1
			if self.c % 100 == 0 : print(self.w)
			if self.c > 10000: return None


def main():
	D = []
	X = np.array(kohonendata)
	Y = np.rot90(np.array(perseptrondata))[0]
	Z = np.array([94,2,76,5,422,177,316,1147,195]) # MAX values
	X = X / Z

	for i in range(len(X)):
		x = X[i]
		y = Y[i]
		if y == [1,0,0]: y = 1
		if y == [0,1,0]: y = 2
		if y == [0,0,1]: y = 3
		D += [[list(x),y]]
	f = Neuron(D)
	print(f.w)
	for x in D:
		print(round(f(x[0]),2),[round(_,2) for _ in x[0]],x[1])

if __name__ == '__main__':
	main()
# [nan, nan, nan, nan, nan, nan, nan, nan, nan]
# nan [94, 1, 0, 2, 11672, 4456, 0, 649, 195] 10
# nan [8, 0, 43, 0, 422, 0, 37, 1147, 0] 20
# nan [78, 0, 0, 5, 1138, 2, 0, 121, 0] 10
# nan [10, 0, 0, 0, 366, 6, 8, 679, 0] 20
# nan [8, 0, 0, 0, 167, 0, 0, 754, 0] 20
# nan [7, 0, 3, 0, 136, 0, 26, 557, 0] 20
# nan [7, 0, 0, 1, 258, 10, 316, 120, 0] 20
# nan [14, 0, 0, 0, 246, 5, 2, 323, 0] 20
# nan [11, 0, 0, 1, 260, 10, 2, 99, 0] 20
# nan [32, 0, 0, 0, 242, 89, 0, 13, 1] 20
