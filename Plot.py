import matplotlib.pyplot as plt

def plotData1(filename = "1v2.txt"):
	f = open(filename)

	lines = f.readlines()
	lines = lines[2:]

	x1, x2, x3, x4, x5 = [], [], [], [], []
	y1, y2, y3, y4, y5 = [], [], [], [], []

	for line in lines:
		line = eval(line)
		state, (opt1, gen1, exp), (opt2, gen2, itr) = line

		x1.append(opt1)
		y1.append(gen1)

		x2.append(opt2)
		y2.append(gen2)

		x3.append(gen1)
		y3.append(gen2)

		x4.append(exp)
		y4.append(gen1)

		x5.append(itr)
		y5.append(gen2)

		state = eval(state)
		print state 

	# plt.plot(x1, y1, 'ro')
	# plt.title("A* optimal solution vs generated nodes")
	# plt.xlabel("Lenght of optimal solution")
	# plt.ylabel("Number of generated nodes")
	# plt.axis([0, 30, 0, 4000])
	# plt.show()

	# plt.plot(x2, y2, 'bo')
	# plt.title("IDA* optimal solution vs generated nodes")
	# plt.xlabel("Lenght of optimal solution")
	# plt.ylabel("Number of generated nodes")
	# plt.axis([0, 30, 0, 6500000])
	# plt.show()

	# plt.plot(x3, y3, 'go')
	# plt.title("A* vs IDA* generated nodes")
	# plt.xlabel("Number of generated nodes by A*")
	# plt.ylabel("Number of generated nodes by IDA*")
	# plt.show()

	plt.plot(x4, y4, 'yo')
	plt.title("A* expanded vs generated nodes")
	plt.xlabel("Number of expanded nodes by A*")
	plt.ylabel("Number of generated nodes by IDA*")
	plt.show()

	plt.plot(x5, y5, 'mo')
	plt.title("IDA* iterations vs generated nodes")
	plt.xlabel("Number of iterations by A*")
	plt.ylabel("Number of generated nodes by IDA*")
	plt.axis([0, 8, 0, 6500000])
	plt.show()

def plotData2(filename = "2a.txt"):
	f = open(filename)

	lines = f.readlines()
	lines = lines[2:]

	x1, x2, x3, x4, x5 = [], [], [], [], []
	y1, y2, y3, y4, y5 = [], [], [], [], []

	for line in lines:
		line = eval(line)
		state, _, (opt1, itr, gen1), (_, opt2, gen2) = line

		x1.append(opt1)
		y1.append(gen1)

		x2.append(opt2)
		y2.append(gen2)

		x3.append(gen1)
		y3.append(gen2)

		

		state = eval(state)
		print state 

	plt.plot(x1, y1, 'ro')
	plt.title("IDA* optimal solution vs generated nodes")
	plt.xlabel("Lenght of optimal solution")
	plt.ylabel("Number of generated nodes")
	# plt.axis([0, 30, 0, 4000])
	plt.show()

	plt.plot(x2, y2, 'bo')
	plt.title("RBFS optimal solution vs generated nodes")
	plt.xlabel("Lenght of optimal solution")
	plt.ylabel("Number of generated nodes")
	# plt.axis([0, 30, 0, 6500000])
	plt.show()

	plt.plot(x3, y3, 'go')
	plt.title("IDA* vs RBFS generated nodes")
	plt.xlabel("Number of generated nodes by IDA*")
	plt.ylabel("Number of generated nodes by RBFS")
	plt.show()

def plotData3a(filename = "3-random-restart-100.txt"):
	f = open(filename)
	lines = f.readlines()
	x = []
	y = []

	for line in lines:
		i, p = eval(line)
		x.append(i)
		y.append(p)

	plt.plot(x, y, '--ro')
	plt.title("Maximum restarts vs accuracy")
	plt.xlabel("Maximum restarts allowed")
	plt.ylabel("Accuracy in percentage")
	plt.show()

def plotData3b(filename = "3-simulated-annealing-100.txt"):
	f = open(filename)
	lines = f.readlines()
	x1, x2, x3 = [], [], []
	y1, y2, y3 = [], [], []

	for line in lines:
		a, e, r, p = eval(line)
		
		if a == 100 and e == 10**-05:
			x1.append(r)
			y1.append(p)

		if a == 100 and r == 0.99:
			x2.append(e)
			y2.append(p)

	plt.plot(x1, y1, '--bo')
	plt.title("Ratio vs accuracy (Initial tempertature = 100, cut off = 10e-05)")
	plt.xlabel("Ratio")
	plt.ylabel("Accuracy in percentage")
	plt.show()

	plt.plot(x2, y2, '--go')
	plt.title("Cut off vs accuracy (Initial tempertature = 100, ratio = 0.99)")
	plt.xlabel("Cut off")
	plt.ylabel("Accuracy in percentage")
	#plt.axis([10**-21, 0, 0, 101])
	ax = plt.subplot()
	ax.set_xscale('log')
	plt.show()

def plotData4(filename = "4-genetic-algorithm-intensive-100.txt"):
	f = open(filename)
	lines = f.readlines()
	x1, x2, x3 = [], [], []
	y1, y2, y3 = [], [], []

	for line in lines:
		n, m, i, p = eval(line)
		
		if n == 200 and m == 0.02:
			x1.append(i)
			y1.append(p)

		if n == 100 and i == 500:
			x2.append(m)
			y2.append(p)

		if m == 0.02 and i == 500:
			x3.append(n)
			y3.append(p)

	plt.plot(x1, y1, '--ro')
	plt.title("Iterations vs accuracy (Population size = 200, mutation probability = 0.02)")
	plt.xlabel("Maximum iterations")
	plt.ylabel("Accuracy in percentage")
	plt.axis([0, 1050, 0, 105])
	plt.show()

	plt.plot(x2, y2, '--bo')
	plt.title("Mutation probability vs accuracy (Population size = 200, iterations = 500)")
	plt.xlabel("Mutation probability")
	plt.ylabel("Accuracy in percentage")
	plt.axis([0, 0.0525, 0, 105])
	plt.show()

	plt.plot(x3, y3, '--go')
	plt.title("Population size vs accuracy (Mutation probability = 0.02, iterations = 500)")
	plt.xlabel("Population size")
	plt.ylabel("Accuracy in percentage")
	plt.axis([0, 210, 0, 105])
	plt.show()

plotData4()