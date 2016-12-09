class FuzzyVar(object):
	"""элемент нечеткого множества"""
	def __init__(self, varName = "Семь", 
					   varSem  = {1:0,3:0.4,7:1}):
		self._name = varName
		self._sem = varSem

	def __eq__(self, val):
		return self.varName == val.varName and
			   self.varSem == val.varSem

	def __ne__(self, val):
		return ! self.__eq__(val)

def test():
	pass

if __name__ == '__main__':
	test()