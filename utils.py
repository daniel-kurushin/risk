import sys

def _get_my_name():
	return str(sys._getframe().f_back.f_code.co_name)

def test():
	print(_get_my_name())

if __name__ == '__main__':
	test()
