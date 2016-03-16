import heapq
import copy

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
			newState = copy.deepcopy(state)
			newState[x][y] = newState[x + dx[i]][y + dy[i]]
			newState[x + dx[i]][y + dy[i]] = 0
			moves.append(str(newState))

	return moves

assert(len(getMoves(str([[2, 1, 3, 5], [4, 0, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]))) == 4)

def AStar(start):
	explored = set()
	frontier = []
	inFrontier = dict()

	heapq.heappush(frontier, (getHeuristic(start), 0, start))
	inFrontier[start] = getHeuristic(start)
	generatedNodes = 0

	while len(frontier):
		fvalue, gvalue, state = heapq.heappop(frontier)

		if isGoal(state):
			explored.add(state)
			return fvalue, len(explored), generatedNodes
		
		if state in explored:
			continue

		del inFrontier[state]
		explored.add(state)

		for nextState in getMoves(state):
			generatedNodes += 1

			if nextState in explored:
				continue

			nextGvalue = gvalue + 1
			nextFvalue = nextGvalue + getHeuristic(nextState)

			if (nextState in inFrontier) and (inFrontier[nextState] < nextFvalue):
				continue

			heapq.heappush(frontier, (nextFvalue, nextGvalue, nextState))
			inFrontier[nextState] = nextFvalue

assert(AStar(str([[1, 2, 6, 3],[4, 9, 5, 7], [8, 13, 11, 15],[12, 14, 0, 10]])) == (11, 19, 59))
print AStar(str([[15, 8, 10, 4], [9, 12, 11, 3], [0, 5, 2, 14], [7, 1, 6, 13]]))