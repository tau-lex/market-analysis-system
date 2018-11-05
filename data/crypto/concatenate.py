import numpy as np

fn = 'BNBETH'
nb = 9

data = []

for i in range(nb):
	idx = i + 1
	fname = fn + str(idx) + '.csv'
	data.append(np.genfromtxt(fname, delimiter=';', dtype=np.float))
	
data = np.vstack(data)

np.savetxt(fn+'0.csv', data, fmt='%.8f', delimiter=';')
