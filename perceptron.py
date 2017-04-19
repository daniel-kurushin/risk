import numpy as np
from pybrain.structure import SoftmaxLayer
from pybrain.datasets import *
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.customxml.networkreader import NetworkReader
from pybrain.tools.customxml.networkwriter import NetworkWriter
from pybrain.tools.shortcuts import *

MAX_EPOCHS = 10000
MIN_EPOCHS =  0

def create_training_set(x,y):
	dataset = ClassificationDataSet(2, 3)
	for i in range(0, len(x)):
		dataset.addSample(x[i][1:3], y[i])
	return dataset


if __name__ == "__main__":
	X = [l.strip().replace(',','.').split('^')[1:4] for l in open('data/banks.dat').readlines()]
	Y = [l.strip().replace(',','.').split('^')[4:7] for l in open('data/banks.dat').readlines()]
	dataset = create_training_set(X,Y)

	net = buildNetwork(2, 2, 3)# , hiddenclass=SoftmaxLayer)
	net.sortModules()

	trainer = BackpropTrainer(net, dataset)
	epochs = 0
	result = trainer.train()
	while (result > 0.001) or (epochs < MIN_EPOCHS):
		try:
			if epochs % 100 == 0:
				t = '▁'
				if result > 0.001: t = '▂'
				if result > 0.002: t = '▃'
				if result > 0.003: t = '▄'
				if result > 0.004: t = '▅'
				if result > 0.005: t = '▆'
				if result > 0.050: t = '▇'
				if result > 0.100: t = '█'
				print(t, end='', flush=1)
			epochs += 1
			if epochs > MAX_EPOCHS:
				print('error while traininig %s' % (result))
				break
			result = trainer.train()
		except KeyboardInterrupt:
			break
	print(' ', result)
	for i in range(len(X)):
		print("%s -> [%s, %s, %s]" %
			tuple([X[i][0]] + [round(y,2) for y in net.activate(X[i][1:3])]), Y[i])
