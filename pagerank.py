import numpy as np
import time
import generateGraph

# print G.shape
# print G

# print "Transit to markov matrix"
# G /= G.sum(axis=1)[:,np.newaxis]
# print G

def pageRank_fast():
	start_time = time.time()
	n_states = 3
	n_steps = 50
	alpha = 0.1

	#Loading data
	# print "Loading graph.txt"
	# P = np.genfromtxt("graph.txt",delimiter=None) #P = np.array(graph())
	print "Generating graph"
	P = generateGraph.GenerateGraph()
	print("--- %s seconds ---" % (time.time() - start_time))
	n_states = P.shape[0]

	#Construct Markov Chain
	print "Transitting graph into Markov Chain"
	start_time = time.time()

	for row in np.where(~P.any(axis=1))[0]:
		P[row] = 1.0 / n_states

	P /= P.sum(axis=1)[:,np.newaxis]
	P *= 1 - alpha
	P += alpha / n_states

	print("--- %s seconds ---" % (time.time() - start_time))

	#Compute PageRank by iteration
	print "Computing PageRank"
	start_time = time.time()

	a = np.random.rand(n_states)
	a /= a.sum()

	for k in range(n_steps):
	    a = P.T.dot(a)

	print("--- %s seconds ---" % (time.time() - start_time))

	#Save results to PageRank.txt
	print "Saving results to PageRank.txt"
	start_time = time.time()
	np.savetxt("PageRank.txt", a)

	print("--- %s seconds ---" % (time.time() - start_time))

def pageRank():
	start_time = time.time()
	n_states = 3
	n_steps = 10
	alpha = 0.1

	P = np.random.rand(n_states, n_states)

	P = np.array([
		[0, 1.0, 1.0], 
		[0, 0, 0],
		[1.0, 0, 0]
		])

	P = np.genfromtxt("graph.txt",delimiter=None)
	print "Loading graph.txt"
	print("--- %s seconds ---" % (time.time() - start_time))

	print "Transitting graph into Markov Chain"
	start_time = time.time()

	for row in np.where(~P.any(axis=1))[0]:
		P[row] = 1.0 / n_states

	P /= P.sum(axis=1)[:,np.newaxis]
	P *= 1 - alpha
	P += alpha / n_states

	print("--- %s seconds ---" % (time.time() - start_time))

	print "Computing PageRank"
	start_time = time.time()

	w, v = np.linalg.eig(P.T)

	j_stationary = np.argmin(abs(w - 1.0))
	p_stationary = v[:,j_stationary].real
	p_stationary /= p_stationary.sum()
	#print p_stationary

	print("--- %s seconds ---" % (time.time() - start_time))

	print "Saving results to PageRank.txt"
	start_time = time.time()
	np.savetxt("PageRank.txt", p_stationary)

	print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
	pageRank_fast()

	# P = np.ones((3, 3))
	# P[2][2] = 0
	# print P
