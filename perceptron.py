import numpy as np
from pybrain.structure import SoftmaxLayer
from pybrain.datasets import *
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.customxml.networkreader import NetworkReader
from pybrain.tools.customxml.networkwriter import NetworkWriter
from pybrain.tools.shortcuts import *

from testdata import perseptrondata, kohonendata

MAX_EPOCHS = 10000
MIN_EPOCHS =  0

def create_training_set():
	dataset = ClassificationDataSet(9, 3)
	x = np.array(kohonendata)
	y = np.rot90(np.array(perseptrondata))[0]
	z = np.array([94,2,76,5,422,177,316,1147,195]) # MAX values
	x = x / z
	for i in range(0, len(kohonendata)):
		dataset.addSample(x[i], y[i])
	return dataset


if __name__ == "__main__":
	dataset = create_training_set()

	net = buildNetwork(9, 5, 3)# , hiddenclass=SoftmaxLayer) # получено эмпирическим путем тыканья и руганья, без Софтмакса не работает
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
	for bank in perseptrondata:
		print("[%s, %s, %s]" % tuple([round(i,2) for i in net.activate(bank[0])]), bank[1])
