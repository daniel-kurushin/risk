import sys

def main(x):
	lines = [i.strip() for i in open(x).readlines()]
	count = 0
	for line in lines:
		try:
			v1, v2 = line.split('] [')
			a = [round(float(v)) for v in v1.strip('[').split(',')]
			b = [int(v) for v in v2.strip(']').split(',')]
			if a == b:
				count += 1
		except ValueError:
			pass
	print(x, count)
	
if __name__ == '__main__':
	try:
		main(sys.argv[1])
	except IndexError:
		print('file name!')
