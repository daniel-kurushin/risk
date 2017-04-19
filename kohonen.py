import pylab
import numpy as np
from scipy import random
from pybrain.structure.modules import KohonenMap
from random import randint

kohonendata = [l.strip().replace(',','.').split('^')[2:4] for l in open('data/banks.dat').readlines()]

som = KohonenMap(len(kohonendata[0]), 66)

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
pylab.savefig('kohonen.png')
# =CONCATENATE("[";C2;",";D2;",";E2;",";F2;",";G2;",";H2;",";I2;",";J2;",";K2;",";"]")
