import random

def print_rand_graph(n,m):
	print('%s %s' % (n,m))
	edges = []
	for i in range(1,n+1):
		for j in range(i+1,n+1):
			edges.append((i,j))
	random.shuffle(edges)
	for i in range(m):
		print('%s %s' % (edges[i][0], edges[i][1]))

NUM_TESTS = 500
print(NUM_TESTS)
for test in range(NUM_TESTS):
	print('polytope-test %s' % (test+1))
	## insert custom test-printing code here
print('polytope-test end')

