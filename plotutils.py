import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import random
import string
import os
from graphviz import Digraph

def plotgraph(a, filepath, ref_a=None):
	N_sp = a.shape[0]
	sp_names = list(string.ascii_uppercase[0:N_sp])
	# (directed) connectedness numpy array: [i,j] element is True if j eats i, else False 
	connected = np.logical_and(a>0,np.transpose(a)<0)
	if ref_a is None:
		ref_connected = connected
	else:
		ref_connected = np.logical_and(ref_a>0,np.transpose(ref_a)<0)

	# preferred edge lengths = 1 for all edges
	preflengths = np.where(connected, np.ones_like(a), np.zeros_like(a))

	# connection weights numpy array: product of mutual effect strengths for directed edges
	w = np.where(connected, np.abs(a*np.transpose(a)), np.zeros_like(a))
	w = w/np.max(w)

	# colors array
	vectorized_to_hex= np.vectorize(mpl.colors.to_hex)
	edgecolors = vectorized_to_hex((1-w).astype(str))
	edgecolors = np.where(connected, edgecolors, np.NAN)
	
	foodwebgraph = Digraph()
	foodwebgraph.rankdir = 'BT'
	#foodwebgraph.engine = 'neato'
	#foodwebgraph.engine = 'fdp'
	#foodwebgraph.engine = 'circo'
	foodwebgraph.engine = 'dot'
	foodwebgraph.format = "pdf"

	# add nodes
	for idx, sp_name in enumerate(sp_names):
		if  np.array_equal(connected[idx], ref_connected[idx]) and np.array_equal(connected[:,idx], ref_connected[:,idx]):
			mistake = False
		else:
			mistake = True
		if mistake:
			nodecolor = '#ff0000'
		else:
			nodecolor = '#000000'
		foodwebgraph.node(sp_name,  style="filled", color=nodecolor, fillcolor=nodecolor, fontcolor='#ffffff')
	# add edges
	for idx_j, sp_j in enumerate(sp_names):
		for idx_i, sp_i in enumerate(sp_names):
			mycolor = edgecolors[idx_i,idx_j]
			preflength = str(preflengths[idx_i,idx_j])
			if connected[idx_i, idx_j]:
				foodwebgraph.edge(sp_i, sp_j, color = mycolor, len=preflength)	

	foodwebgraph.render(filepath+'_graph', cleanup=True)

def plotmatrix(a, filepath):
	fig = plt.figure()
	ax1 = fig.add_subplot(1,1,1)
	imgplot = plt.imshow(a, cmap=plt.cm.RdBu, vmin=-1, vmax=1)
	plt.colorbar(ticks=[-1, 0, 1])
	ax1.figure.savefig(filepath+'.pdf')
	
