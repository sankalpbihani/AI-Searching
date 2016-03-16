import heapq

N = 4

def getHeuristic(state):
	state = eval(state)
	heuristic = 0
	
	for i in range(N):
		for j in range(N):
			val = state[i][j]

			if val > 0:
				heuristic += abs(i - val/N) + abs(j - val%N)
	
	return heuristic

assert(getHeuristic(str([[2, 1, 3, 5], [4, 0, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]])) == 6)

def isGoal(state):
	return getHeuristic(state) == 0
		
assert(isGoal(str([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]])))


def isValidIndexIndex(i, j):
	return i >= 0 and j >= 0 and i < N and j < N

assert(isValidIndexIndex(0, 2))
assert(not isValidIndexIndex(4, 0))

def getMoves(state):
	moves = []
	state = eval(state)

	x = y = None

	for i in range(N):
		if 0 in state[i]:
			x = i
			y = state[i].index(0)

	dx = [1, 0, -1, 0]
	dy = [0, 1, 0, -1]

	for i in range(4):
		if isValidIndexIndex(x + dx[i], y + dy[i]):
			state[x][y], state[x + dx[i]][y + dy[i]] = state[x + dx[i]][y + dy[i]], state[x][y]
			moves.append(str(state))
			state[x][y], state[x + dx[i]][y + dy[i]] = state[x + dx[i]][y + dy[i]], state[x][y]

	return moves

assert(len(getMoves(str([[2, 1, 3, 5], [4, 0, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]))) == 4)

def AStar(start):
	explored = set()
	frontier = []

	heapq.heappush(frontier, (getHeuristic(start), getHeuristic(start), start))
	generatedNodes = 0

	while len(frontier):
		fvalue, hvalue, state = heapq.heappop(frontier)
		gvalue = fvalue - hvalue

		if state in explored:
			continue

		explored.add(state)

		if isGoal(state):
			return fvalue, len(explored), generatedNodes

		for nextState in getMoves(state):
			generatedNodes += 1

			if nextState in explored:
				continue

			nextGvalue = gvalue + 1
			nextFvalue = nextGvalue + getHeuristic(nextState)

			heapq.heappush(frontier, (nextFvalue, getHeuristic(nextState), nextState))

assert(AStar(str([[1, 2, 6, 3],[4, 9, 5, 7], [8, 13, 11, 15],[12, 14, 0, 10]])) == (11, 19, 59))
#print AStar(str([[15, 8, 10, 4], [9, 12, 11, 3], [0, 5, 2, 14], [7, 1, 6, 13]]))

INF = 10**10
FOUND = -10

generatedNodes = 0
def dfs(state, gvalue, flimit):
	generatedNodes = 0
	fvalue = gvalue + getHeuristic(state)

	if fvalue > flimit:
		return fvalue, 0

	if isGoal(state):
		return FOUND, 0

	minVal = INF

	for nextState in getMoves(state):
		val, count = dfs(nextState, gvalue + 1, flimit)
		generatedNodes += 1 + count

		if val == FOUND:
			return val, generatedNodes

		if val < minVal:
			minVal = val

	return minVal, generatedNodes

def IDAStar(start):
	generatedNodes = 0
	flimit = getHeuristic(start)

	while True:
		val, generatedNodes = dfs(start, 0, flimit)
		
		if val == FOUND:
			return flimit, generatedNodes
		
		flimit = val

assert(IDAStar(str([[1, 2, 6, 3],[4, 9, 5, 7], [8, 13, 11, 15],[12, 14, 0, 10]])) == (11, 25))
#print IDAStar(str([[1,2,0,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]]))

