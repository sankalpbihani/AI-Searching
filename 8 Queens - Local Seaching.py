import random

N = 8
MAX_SCORE = N * (N-1) / 2
MIN_SCORE = 0

def getRandomState():
	state = []

	for i in range(N):
		state.append(random.randrange(N))

	return str(state)

def getObjectiveScore(state):
	state = eval(state)
	score = MAX_SCORE

	for i in range(N):
		for j in range(i+1, N):
			if state[i] == state[j] or abs(state[i] - state[j]) == j - i:
				score -= 1

	return score

assert getObjectiveScore(str([1, 1, 2, 1, 1, 1, 1, 1])) == 5

def getNeighbours(state):
	state = eval(state)
	neighbours = []

	for i in range(N):
		for j in range(N):
			curr = state[i]

			if curr != j:
				state[i] = j
				neighbours.append(str(state))
				state[i] = curr

	return neighbours

assert len(set(getNeighbours(str([1, 2, 3, 4, 4, 0, 1, 2])))) == 56

def hillClimbing(state):
	currScore = None

	while state:
		currScore = getObjectiveScore(state)
		nextState = None

		for neighbour in getNeighbours(state):
			score = getObjectiveScore(neighbour)

			if score > currScore:
				currScore = score
				nextState = neighbour

		state = nextState

	return currScore

assert hillClimbing(str([1, 2, 3, 4, 5, 6, 7, 0])) == 25

def randomRestartHillClimbing(state, maxRestarts = 10):
	cnt = 0
	currScore = getObjectiveScore(state)

	while cnt < maxRestarts and currScore < MAX_SCORE:
		currScore = max(hillClimbing(state), currScore)
		state = getRandomState()
		cnt+=1

	return currScore
