import numpy as np

def create_chainweb(N):
	r_0 = np.ones(N, dtype=np.float)
	A = np.zeros((N,N), dtype=np.float)
	for n in range(N):
		r_0[n] = 1
		A[n,n] = -1
		if n==0:
			continue
		food = n-1
		A[food,n] = -1
		A[n,food] = 1

	return r_0, A

def create_simpleweb(N):
	r_0 = np.ones(N, dtype=np.float)
	A = np.zeros((N,N), dtype=np.float)
	for n in range(N):
		r_0[n] = 1
		A[n,n] = -1
		if n==0:
			continue
		food = np.random.randint(n)
		A[food,n] = -1
		A[n,food] = 1

	return r_0, A

def create_complexweb(N):
	roots = max(int(N/5),1)
	r_0 = np.random.rand(N)*0.9+0.1
	A = np.zeros((N,N), dtype=np.float)
	subchains = [[] for n in range(N)] # species below in the chain
	placed = []
	for n in range(N):
		r_0[n] = 0.1+0.9*np.random.rand()
		A[n,n] = -(0.1+0.9*np.random.rand())
		if n<roots:
			placed.append(n)
			continue
		# 1 or maybe 2 food species from anywhere
		if len(placed)>=2:
			potentialfoods = list(np.random.choice(placed, 2, replace=False))
		else:
			potentialfoods = [placed[0]]
		foods = [potentialfoods[0]]
		if np.random.rand()<0.5 and len(placed)>=2:
			foods.append(potentialfoods[1])
		# maybe one more food species from subchains
		additionalfoods = []
		for food in foods:
			if np.random.rand()<0.5 and len(subchains[food])>0:
				additionalfoods += list(np.random.choice(subchains[food],1))
		foods += additionalfoods
		# set interaction terms and subchains
		for food in foods:
			A[food,n] = -(0.1+0.9*np.random.rand())
			A[n,food] = abs(A[food,n])*(0.1+0.9*np.random.rand())
			subchains[n] += [food]+subchains[food]
		subchains[n] = list(set(subchains[n]))
		placed.append(n)

	return r_0, A
