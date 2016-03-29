import heapq
import random

N = 4
INF = 10**10
FOUND = -10

def getRandomState():
	arr = []
	
	for i in range(N*N):
		arr.append(i)

	random.shuffle(arr)
	state = []

	for i in range(N):
		tmp = []
		
		for j in range(N):
			tmp.append(arr[i*N + j])

		state.append(tmp)

	return str(state)

def getInitialState():
	state = []
	for i in range(N):
		row = []
		for j in range(N):
			row.append(i*N + j)
		state.append(row)
	return str(state)

def getManhattanHeuristic(state):
	state = eval(state)
	heuristic = 0
	n = len(state)

	for i in range(n):
		for j in range(n):
			val = state[i][j]

			if val > 0:
				heuristic += abs(i - val/n) + abs(j - val%n)
	
	return heuristic

assert getManhattanHeuristic(str([[2, 1, 3, 5], [4, 0, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]])) == 6

def isGoal(state, getHeuristic = getManhattanHeuristic):
	return getHeuristic(state) == 0
		
assert isGoal(str([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]))
assert isGoal(getInitialState())

def isValidIndexIndex(i, j):
	return i >= 0 and j >= 0 and i < N and j < N

assert isValidIndexIndex(0, 2)
assert not isValidIndexIndex(4, 0)

def getNeighbours(state):
	neighbours = []
	state = eval(state)
	n = len(state)

	x = y = None

	for i in range(n):
		if 0 in state[i]:
			x = i
			y = state[i].index(0)

	dx = [1, 0, -1, 0]
	dy = [0, 1, 0, -1]

	for i in range(4):
		if isValidIndexIndex(x + dx[i], y + dy[i]):
			state[x][y], state[x + dx[i]][y + dy[i]] = state[x + dx[i]][y + dy[i]], state[x][y]
			neighbours.append(str(state))
			state[x][y], state[x + dx[i]][y + dy[i]] = state[x + dx[i]][y + dy[i]], state[x][y]

	return neighbours

assert len(getNeighbours(str([[2, 1, 3, 5], [4, 0, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]))) == 4

def AStar(state, getHeuristic = getManhattanHeuristic):
	explored = set()
	frontier = []

	heapq.heappush(frontier, (getHeuristic(state), getHeuristic(state), state))
	generatedNodes = 0

	while len(frontier):
		fvalue, hvalue, state = heapq.heappop(frontier)
		gvalue = fvalue - hvalue

		if state in explored:
			continue
		
		explored.add(state)

		if isGoal(state):
			return fvalue, len(explored), generatedNodes

		for neighbour in getNeighbours(state):
			generatedNodes += 1

			if neighbour in explored:
				continue

			nextGvalue = gvalue + 1
			nextFvalue = nextGvalue + getHeuristic(neighbour)

			heapq.heappush(frontier, (nextFvalue, getHeuristic(neighbour), neighbour))

assert AStar(str([[1, 2, 6, 3], [4, 9, 5, 7], [8, 13, 11, 15], [12, 14, 0, 10]])) == (11, 19, 59)
#print AStar(str([[15, 8, 10, 4], [9, 12, 11, 3], [0, 5, 2, 14], [7, 1, 6, 13]]))

def dfs(state, gvalue, flimit, getHeuristic = getManhattanHeuristic):
	generatedNodes = 0
	fvalue = gvalue + getHeuristic(state)

	if fvalue > flimit:
		return fvalue, 0

	if isGoal(state):
		return FOUND, 0

	minVal = INF

	for neighbour in getNeighbours(state):
		val, count = dfs(neighbour, gvalue + 1, flimit)
		generatedNodes += 1 + count

		if val == FOUND:
			return val, generatedNodes

		if val < minVal:
			minVal = val

	return minVal, generatedNodes

def IDAStar(state, getHeuristic = getManhattanHeuristic):
	generatedNodes = 0
	iterations = 1
	flimit = getHeuristic(state)

	while True:
		val, gen = dfs(state, 0, flimit)
		generatedNodes += gen
		
		if val == FOUND:
			return flimit, iterations, generatedNodes
		
		flimit = val
		iterations += 1

assert IDAStar(str([[1, 2, 6, 3], [4, 9, 5, 7], [8, 13, 11, 15], [12, 14, 0, 10]])) == (11, 1, 25)
#print IDAStar(str([[1,2,0,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]]))

def RBFS(state, flimit = INF, gvalue = 0, fvalue = None, getHeuristic = getManhattanHeuristic):
	if fvalue == None:
		fvalue = getHeuristic(state)

	if isGoal(state):
		return True, fvalue, 0

	neighbours = getNeighbours(state)
	fvalues = []

	generatedNodes = len(neighbours)

	for i in range(len(neighbours)):
		neighbour = neighbours[i]
		fvalues.append(((max(gvalue + 1 + getHeuristic(neighbour), fvalue)), i))

	while True:
		fvalues.sort()
		minValue, minState = fvalues[0]
		
		if minValue > flimit:
			return False, minValue, generatedNodes
		
		altValue, altState = fvalues[1]
		result, value, genNodes = RBFS(neighbours[minState], min(flimit, altValue), gvalue + 1, minValue)
		fvalues[0] = (value, minState)
		generatedNodes += genNodes
		
		if result:
			return result, value, generatedNodes

assert RBFS(str([[1, 2, 6, 3], [4, 9, 5, 7], [8, 13, 11, 15], [12, 14, 0, 10]])) == (True, 11, 36)

def getRandomSolvableState(moves):
	state = getInitialState()
	for i in range(moves):
		neighbours = getNeighbours(state)
		state = random.choice(neighbours)
	return state

def compareAStarAndIDAStar(moves = 100):
	state = getRandomSolvableState(random.randint(moves - 9, moves))
	opt1, exp, gen1 = AStar(state)
	if opt1 > 31 or gen1 > 4000:
		return None
	print state
	print opt1, exp, gen1
	opt2, itr, gen2 = IDAStar(state)
	print opt2, itr, gen2
	return state, (opt1, gen1, exp), (opt2, gen2, itr)

# print compareAStarAndIDAStar()

def writeDataToFile1():
	file = open("1.txt", "w")
	file.write("state, (A* opt, A* generated, A* explored), (IDA* opt, IDA* generated, IDA* iterations)\n\n")
	i = 0

	while i < 20:
		line = compareAStarAndIDAStar()
		if line:
			line = str(line)
			print line
			file.write(line + "\n")
			i += 1

	file.close()

# writeDataToFile1()

def compareIDAStarAndRBFS(moves = 100):
	state = getRandomSolvableState(random.randint(moves - 9, moves))
	opt, _, gen = AStar(state)
	
	if opt > 31 or gen > 4000:
		return None

	print state, opt, gen
	opt1, itr, gen1 = IDAStar(state)
	print opt1, itr, gen1
	solved, opt2, gen2 = RBFS(state)
	print solved, opt2, gen2

	return state, opt, (opt1, itr, gen1), (solved, opt2, gen2)

def writeDataToFile2a():
	file = open("2a.txt", "w")
	file.write("state, optimal, (IDA* opt, IDA* generated, IDA* iterations), (RBFS solved, RBFS opt, RBFS generated),\n\n")
	i = 0

	while i < 20:
		line = compareIDAStarAndRBFS()
		if line:
			line = str(line)
			print line
			file.write(line + "\n")
			i += 1

	file.close()

# writeDataToFile2a()

def getMisplacedTilesHeuristic(state):
	state = eval(state)
	heuristic = 0
	n = len(state)

	for i in range(n):
		for j in range(n):
			val = state[i][j]
			heuristic += ((val != 0) and (val != (i*n + j)))

	return heuristic

assert getMisplacedTilesHeuristic(str([[2, 1, 3, 5], [4, 0, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]])) == 3

def getWeightedHeuristic(state, w1 = 0.5, w2 = 0.5):
	return w1 * getManhattanHeuristic(state) + w2 * getMisplacedTilesHeuristic(state)

assert getWeightedHeuristic(str([[2, 1, 3, 5], [4, 0, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]])) == 4.5
