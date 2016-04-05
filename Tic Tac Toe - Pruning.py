import random

PLAYER = 'X'
CPU = 'O'
EMPTY = '-'

PLAYER_WIN = 500
CPU_WIN = 550
DRAW = 600

INF = 10**10

def getEmptyBoard():
	board = []
	
	for i in range(3):
		row = []

		for j in range(3):
			row.append(EMPTY)

		board.append(row)

	return str(board)

assert getEmptyBoard() == str([[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]])

def getBoardState(board):
	board = eval(board)
	full = True

	for i in range(3):
		for j in range(3):
			if board[i][j] == EMPTY:
				full = False

		if board[i][0] == board[i][1] == board[i][2] and board[i][0] != EMPTY:
			return PLAYER_WIN if board[i][0] == PLAYER else CPU_WIN
		if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
			return PLAYER_WIN if board[0][i] == PLAYER else CPU_WIN

	if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
		return PLAYER_WIN if board[0][0] == PLAYER else CPU_WIN

	if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
		return PLAYER_WIN if board[0][2] == PLAYER else CPU_WIN

	if full:
		return DRAW

	return None

assert getBoardState(getEmptyBoard()) == None
assert getBoardState(str([[PLAYER, CPU, PLAYER], [CPU, PLAYER, EMPTY], [CPU, EMPTY, PLAYER]])) == PLAYER_WIN

def makeMove(board, move, agent):
	i = move[0]
	j = move[1]
	board =  eval(board)

	if board[i][j] == EMPTY:
		board[i][j] = agent

	return str(board)

assert makeMove(str([[PLAYER, CPU, EMPTY], [PLAYER, CPU, EMPTY], [PLAYER, EMPTY, PLAYER]]), (0, 0), CPU) == str([[PLAYER, CPU, EMPTY], [PLAYER, CPU, EMPTY], [PLAYER, EMPTY, PLAYER]])
assert makeMove(str([[PLAYER, CPU, EMPTY], [PLAYER, CPU, EMPTY], [PLAYER, EMPTY, PLAYER]]), (0, 2), CPU) == str([[PLAYER, CPU, CPU], [PLAYER, CPU, EMPTY], [PLAYER, EMPTY, PLAYER]])

def getMovesSeriallyOrdered(board, _):
	board = eval(board)
	moves = []

	for i in range(3):
		for j in range(3):
			if board[i][j] == EMPTY:
				moves.append((i, j))

	return moves

def getMovesRandomlyOrdered(board, _):
	moves = getMovesSeriallyOrdered(board, _)
	random.shuffle(moves)
	return moves

assert (0, 2) in getMovesRandomlyOrdered(str([[PLAYER, CPU, EMPTY], [PLAYER, CPU, EMPTY], [PLAYER, EMPTY, PLAYER]]), PLAYER)
assert len(getMovesRandomlyOrdered(str([[PLAYER, CPU, EMPTY], [PLAYER, CPU, EMPTY], [PLAYER, EMPTY, PLAYER]]), PLAYER)) == 3

def getUtility(board):	
	if getBoardState(board) == PLAYER_WIN:
		return -1
	elif getBoardState(board) == CPU_WIN:
		return 1
	else:
		return 0

assert getUtility(str([[PLAYER, CPU, PLAYER], [CPU, PLAYER, EMPTY], [CPU, EMPTY, PLAYER]])) == -1
assert getUtility(str([[PLAYER, CPU, PLAYER], [CPU, PLAYER, EMPTY], [CPU, CPU, CPU]])) == 1
assert getUtility(str([[PLAYER, CPU, PLAYER], [CPU, PLAYER, CPU], [CPU, PLAYER, CPU]])) == 0

def printRow(row):
	print ' ' + row[0] + ' | ' + row[1] + ' | ' + row[2] + ' '

def printBoard(board):
	board = eval(board)
	printRow(board[0])
	print '-----------'
	printRow(board[1])
	print '-----------'
	printRow(board[2])

def maxPlayer(board, alpha, beta, depth, stats, getMoves = getMovesRandomlyOrdered):
	if getBoardState(board):
		stats[0] = max(stats[0], depth)
		return getUtility(board), board

	bestValue = -INF
	bestChild = None
	moves = getMoves(board, CPU)

	for move in moves:
		stats[1] += 1
		child = makeMove(board, move, CPU)
		value, tmp = minPlayer(child, alpha, beta, depth + 1, stats, getMoves)
		
		if value > bestValue:
			bestValue = value
			bestChild = child

		if bestValue >= beta:
			return bestValue, bestChild
		
		alpha = max(alpha, bestValue)

	return bestValue, bestChild

def minPlayer(board, alpha, beta, depth, stats, getMoves):
	if getBoardState(board):
		stats[0] = max(stats[0], depth)
		return getUtility(board), board

	bestValue = INF
	bestChild = None
	moves = getMoves(board, PLAYER)

	for move in moves:
		stats[1] += 1
		child = makeMove(board, move, PLAYER)
		value, tmp = maxPlayer(child, alpha, beta, depth + 1, stats, getMoves)

		if bestValue > value:
			bestValue = value
			bestChild = child

		if bestValue <= alpha:
			return bestValue, bestChild

		beta = min(beta, bestValue)

	return bestValue, bestChild

def alplaBetaPruning(board, getMoves = getMovesRandomlyOrdered):
	stats = [0, 0]
	ret = maxPlayer(board, -INF, INF, 0, stats, getMoves)
	print stats
	return ret, stats

def getPlayerMove(board):
	print "\nYour Turn, Enter Input\n"
	move = map(int, raw_input().strip().split(' '))
	board = makeMove(board, move, PLAYER)
	return board

def playTicTacToe():
	board = getEmptyBoard()

	(value, board), stats = alplaBetaPruning(board)
	print "Lets Start. I play first, human! \n"

	print stats
	printBoard(board)

	while not getBoardState(board):
		
		nextBoard = getPlayerMove(board)
		
		while nextBoard == board:
			print "\nCan you not even play properly?\n"
			nextBoard = getPlayerMove(board)

		board = nextBoard
		print stats
		printBoard(board)

		if getBoardState(board):
			break

		(value, board), stats = alplaBetaPruning(board)

		print "\nMy Turn. Prepare yourself. \n"
		print stats
		printBoard(board)

	status = getBoardState(board)

	if status == PLAYER_WIN:
		print "\nI Lose? Impossible! Something must be wrong!"
	elif status == CPU_WIN:
		print "\nI Win. As expected."
	else:
		print "\nIts a Draw! Good game human."

#playTicTacToe()

def calcNodeCount(d, bf):
	nodes = 0
	for i in range(d+1):
		nodes += pow(bf, i)
	return nodes

def getBranchingFactor(d, n):
	lo, hi = 0.0, 10.0

	while lo < (hi - 10**-5):
		mid = (lo + hi)/2
		nodes = calcNodeCount(d, mid)

		if nodes == n:
			return mid
		elif nodes < n:
			lo = mid
		else:
			hi = mid

	return lo

def getMovesBetterOrdered(board, agent):
	board = eval(board)
	moves = []
	a = [(1, 1), (0, 0), (0, 2), (2, 0), (2, 2), (0, 1), (1, 0), (2, 1), (1, 2)]

	for aa in a:
		if board[aa[0]][aa[1]] == EMPTY:
			moves.append(aa)

	return moves

def getWinPositions(board, agent):
	board = eval(board)
	moves = []

	cnt3, pos3 = 0, -1
	cnt4, pos4 = 0, -1

	for i in range(3):
		cnt1, pos1 = 0, -1
		cnt2, pos2 = 0, -1

		for j in range(3):
			cnt1 += board[i][j] == agent
			cnt2+= board[j][i] == agent

			if board[i][j] == EMPTY:
				pos1 = j

			if board[j][i] == EMPTY:
				pos2 = j

		if cnt1 == 2 and pos1 >= 0:
			moves.append((i, pos1))

		if cnt2 == 2 and pos2 >= 0:
			moves.append((pos2, i))

		cnt3 += board[i][i] == agent
		cnt4 += board[i][2-i] == agent

		if board[i][i] == EMPTY:
			pos3 = i

		if board[i][2-i] == EMPTY:
			pos4 = i

	if cnt3 == 2 and pos3 >= 0:
		moves.append((pos3, pos3))

	if cnt4 == 2 and pos4 >= 0:
		moves.append((pos4, 2-pos4))

	return moves

def getMovesEvenBetterOrdered(board, agent):
	moves = []
	otherAgent = PLAYER if agent == CPU else CPU

	s_moves = getWinPositions(board, agent)
	for i in s_moves:
		moves.append(i)

	s_moves = getWinPositions(board, otherAgent)
	for i in s_moves:
		moves.append(i)

	s_moves = getMovesBetterOrdered(board, agent)
	for i in s_moves:
		if not i in moves:
			moves.append(i)

	return moves 

_, stats = alplaBetaPruning(getEmptyBoard(), getMovesSeriallyOrdered)
print getBranchingFactor(stats[0], stats[1])

_, stats = alplaBetaPruning(getEmptyBoard(), getMovesBetterOrdered)
print getBranchingFactor(stats[0], stats[1])

_, stats = alplaBetaPruning(getEmptyBoard(), getMovesEvenBetterOrdered)
print getBranchingFactor(stats[0], stats[1])

playTicTacToe()