import pylab
import numpy as np
from scipy import random
from pybrain.structure.modules import KohonenMap
from testdata import kohonendata
from random import randint

x = np.array(kohonendata)
y = np.array([94,2,76,5,422,177,316,1147,195]) # MAX values
kohonendata = x / y

som = KohonenMap(len(kohonendata[0]), 3)

pylab.ion()
p = pylab.plot(som.neurons[:,:,0].flatten(), som.neurons[:,:,1].flatten(), 's')
l = len(kohonendata)

for i in range(250000):
	# one forward and one backward (training) pass
	k = randint(0,l-1)
	som.activate(kohonendata[k])
	som.backward()

	# plot every 100th step
	if i % 100 == 0:
		p[0].set_data(som.neurons[:,:,0].flatten(), som.neurons[:,:,1].flatten())
		pylab.draw()
# =CONCATENATE("[";C2;",";D2;",";E2;",";F2;",";G2;",";H2;",";I2;",";J2;",";K2;",";"]")
