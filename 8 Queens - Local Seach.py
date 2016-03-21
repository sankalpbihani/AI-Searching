import random
import math
import bisect

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
	n = len(state)

	for i in range(n):
		for j in range(i+1, n):
			if state[i] == state[j] or abs(state[i] - state[j]) == j - i:
				score -= 1

	return score

assert getObjectiveScore(str([1, 1, 2, 1, 1, 1, 1, 1])) == 5

def getNeighbours(state):
	state = eval(state)
	neighbours = []
	n = len(state)

	for i in range(n):
		for j in range(n):
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

def getGeometricTemperature(a = 100, r = 0.999):
	def _getGeometricTemperature(term):
		return a * pow(r, term)

	return _getGeometricTemperature

def simulatedAnnealing(state, getTemperature = getGeometricTemperature(), epsilon = 0.1):
	i = 0
	currScore = getObjectiveScore(state)
	temperature = getTemperature(i)

	while temperature > epsilon and currScore < MAX_SCORE:
		neighbours = getNeighbours(state)
		idx = random.randrange(len(neighbours))
		neighbour = neighbours[idx]
		diff = getObjectiveScore(neighbour) - currScore

		if diff > 0:
			state = neighbour
		else:
			p = math.exp(float(diff)/temperature)
			x = random.random()
			if x < p:
				state = neighbour

		i += 1
		temperature = getTemperature(i)
		currScore = getObjectiveScore(state)

	return currScore

def getNormalizedCumulativeScore(population):
	ncf = []
	currSum = 0
	currScore = MIN_SCORE

	for state in population:
		score = getObjectiveScore(state)
		currSum += score
		ncf.append(currSum)

		if currScore < score:
			currScore = score

	last = ncf[-1]
	for i in range(len(ncf)):
		ncf[i] = float(ncf[i]) / last

	return currScore, ncf

def getRouletteSelection(population, ncf):
	selected = []

	for i in range(len(population)):
		roulette = random.random()
		idx = bisect.bisect_right(ncf, roulette)
		selected.append(population[idx])

	return selected

def getCrossover(selected):
	nextGeneration = []

	for i in range(1, len(selected), 2):
		parent1 = eval(selected[i-1])
		parent2 = eval(selected[i])
		child1 = []
		child2 = []

		n = len(parent1)
		idx = 1 + random.randrange(n - 1)

		for j in range(idx):
			child1.append(parent1[j])
			child2.append(parent2[j])

		for j in range(idx, n):
			child1.append(parent2[j])
			child2.append(parent1[j])

		nextGeneration.append(str(child1))
		nextGeneration.append(str(child2))

	return nextGeneration

def getMutations(nextGeneration, mutationProbability):
	mutatedGeneration = []

	for state in nextGeneration:
		state = eval(state)
		n = len(state)
		mutatedState = []
		
		for num in state:
			rand = random.random()
			if rand < mutationProbability:
				mutatedState.append(random.randrange(n))
			else:
				mutatedState.append(num)

		mutatedGeneration.append(str(mutatedState))

	return mutatedGeneration


def geneticAlgorithm(populationCount = 200, mutationProbability = 0.005, maxIterations = 200):
	population = []

	for i in range(populationCount):
		state = getRandomState()
		population.append(state)

	i = 0
	currScore, ncf = getNormalizedCumulativeScore(population)
	maxScore = currScore

	while i < maxIterations and currScore < MAX_SCORE:
		selected = getRouletteSelection(population, ncf)
		nextGeneration = getCrossover(selected)
		mutatedGeneration = getMutations(nextGeneration, mutationProbability)
		population = mutatedGeneration

		currScore, ncf = getNormalizedCumulativeScore(population)
		i += 1
		maxScore = max(maxScore, currScore)

		#print currScore, maxScore
	return currScore

#print geneticAlgorithm()
print simulatedAnnealing(getRandomState())