import numpy as np
import matplotlib.pyplot as plt
import random
import os, shutil
from plotutils import *
from webgen import *

T = 500000
TU = T # last TU values (around equilibrium) are used for the estimates
S = 50000 # number of samples/estimates (to be averaged)
dT = 0.5
PERT = 0.1 # SD of noise
N = 5 # number of species
SAVEDIR = 'sim'

def plotdata(dataarray, filename):
	fig = plt.figure()
	ax1 = fig.add_subplot(1,1,1)
	for i in range(dataarray.shape[1]):
		ax1.plot(range(dataarray.shape[0]), dataarray[:,i])
	plt.xlabel('Time')
	plt.ylabel('Abundance')
	filename= filename+'.png'
	filepath = os.path.join(SAVEDIR, filename)
	ax1.figure.savefig(filepath)
	plt.close(fig)

def get_timeseries(r_0, ref_A):
	p_0 = np.array([0.1]*N, dtype=np.float)
	p = p_0
	timeseries = [p]
	for t in range(T-1):
		r = r_0 + np.matmul(ref_A,p)
		noise = np.random.randn(N)*PERT*r_0
		r += noise
		p += p*r*dT
		timeseries.append(p.copy())
		if np.min(timeseries[-1])<0.01:
			return None
	return timeseries[-TU:]

try:
	shutil.rmtree(SAVEDIR)
except:
	pass
os.mkdir(SAVEDIR)

print('creating timeseries ...')

timeseries = None
while timeseries is None:
	r_0, ref_A = create_complexweb(N)
	timeseries = get_timeseries(r_0, ref_A)

print('estimating connections from timeseries ...')

# 1 - species abundancia timeseries (TU,N)
p = np.stack(timeseries)
plotdata(p, 'timeseries')

# 2 - dp (abundance changes), r, dr (TU,N)
## dp
dp = np.zeros((TU, N), dtype=np.float)
dp[:TU-1] = p[1:]-p[:TU-1]
dp[TU-1] = np.NAN
## r
r = dp / p
## dr
dr = np.full((TU,N), np.NAN, dtype=np.float)
dr[:TU-1] = r[1:TU]-r[:TU-1]

# 3 - change direction vectors u(T,N) = dp and change absolute values du (T)
u = dp
# length of direction vectors
du = np.sqrt(np.sum(u*u, axis=1))
du_matrix = np.transpose(np.tile(du, (N, 1)))
# normalized direction vectors a(T,N)
a = u / du_matrix

def get_drdp_estimation():
	# 4 - draw a sample of time points (size=N)
	taus = np.random.choice(np.arange(p.shape[0]-2), N, replace=False)
	# 5 - get weights (for base vectors) w(N,TU=N)
	w = []
	m = np.transpose(a[taus]) # rows of m are species, columns are taus
	for n in range(N):
		e = np.zeros(N, dtype=np.float)
		e[n] = 1
		weights = np.linalg.solve(m, e)
		w.append(weights)
	w = np.stack(w)

	# 5 - get partial derivatives dr/dp (N,N)
	drdp = np.full((N,N), np.NAN, dtype=np.float) #drdp[n,m] effect of p[m] on growth rate r[n]
	for n in range(N):
		for m in range(N):
			nominator = np.sum(w[m] * (dr[taus,n] / du[taus])) # summing the contribution of species m in different times
			denominator = np.sqrt(np.sum(w[m]**2)) # normalization
			drdp[n,m] = nominator / denominator
	return drdp

single_estimates = []
for s in range(S):
	if s % int(S/20) == 0:
		print(s, ' / ', S)
	single_estimates.append(get_drdp_estimation())
estimates = np.stack(single_estimates)
est_mean = np.mean(estimates, axis=0)
est_SD = np.std(estimates, axis=0)/(S**0.5)
est_mean = np.where(np.abs(est_mean)>4*est_SD, np.sign(est_mean), np.zeros_like(est_mean))

est_A=est_mean

print('reference connection matrix')
print(np.sign(ref_A))
print('estimated connection matrix')
print(est_A)

print('creating graphs...')

filepath = os.path.join(SAVEDIR, 'refA')
plotgraph(np.sign(ref_A), filepath)

filepath = os.path.join(SAVEDIR, 'estA')
plotgraph(est_A, filepath, np.sign(ref_A))

filepath = os.path.join(SAVEDIR, 'interaction_matrix')
plotmatrix(ref_A, filepath)
