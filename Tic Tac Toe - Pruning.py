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

def makeMove(board, i, j, agent):
	board =  eval(board)

	if board[i][j] == EMPTY:
		board[i][j] = agent

	return str(board)

assert makeMove(str([[PLAYER, CPU, EMPTY], [PLAYER, CPU, EMPTY], [PLAYER, EMPTY, PLAYER]]), 0, 0, CPU) == str([[PLAYER, CPU, EMPTY], [PLAYER, CPU, EMPTY], [PLAYER, EMPTY, PLAYER]])
assert makeMove(str([[PLAYER, CPU, EMPTY], [PLAYER, CPU, EMPTY], [PLAYER, EMPTY, PLAYER]]), 0, 2, CPU) == str([[PLAYER, CPU, CPU], [PLAYER, CPU, EMPTY], [PLAYER, EMPTY, PLAYER]])

def getChildrenRandomlyOrdered(board, agent):
	board = eval(board)
	children = []

	for i in range(3):
		for j in range(3):
			if board[i][j] == EMPTY:
				board[i][j] = agent
				children.append(str(board))
				board[i][j] = EMPTY

	random.shuffle(children)
	return children

assert str([[PLAYER, CPU, CPU], [PLAYER, CPU, EMPTY], [PLAYER, EMPTY, PLAYER]]) in getChildrenRandomlyOrdered(str([[PLAYER, CPU, EMPTY], [PLAYER, CPU, EMPTY], [PLAYER, EMPTY, PLAYER]]), CPU)
assert len(getChildrenRandomlyOrdered(str([[PLAYER, CPU, EMPTY], [PLAYER, CPU, EMPTY], [PLAYER, EMPTY, PLAYER]]), CPU)) == 3

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

def maxPlayer(board, alpha, beta, getChildren = getChildrenRandomlyOrdered):
	if getBoardState(board):
		return getUtility(board), board

	bestValue = -INF
	bestChild = None
	children = getChildren(board, CPU)

	for child in children:
		value, tmp = minPlayer(child, alpha, beta)
		
		if value > bestValue:
			bestValue = value
			bestChild = child

		if bestValue >= beta:
			return bestValue, bestChild
		
		alpha = max(alpha, bestValue)

	return bestValue, bestChild

def minPlayer(board, alpha, beta, getChildren = getChildrenRandomlyOrdered):
	if getBoardState(board):
		return getUtility(board), board

	bestValue = INF
	bestChild = None
	children = getChildren(board, PLAYER)

	for child in children:
		value, tmp = maxPlayer(child, alpha, beta)

		if bestValue > value:
			bestValue = value
			bestChild = child

		if bestValue <= alpha:
			return bestValue, bestChild

		beta = min(beta, bestValue)

	return bestValue, bestChild

def alplaBetaPruning(board):
	return maxPlayer(board, -INF, INF)

def getPlayerMove(board):
	print "\nYour Turn, Enter Input\n"
	i, j = map(int, raw_input().strip().split(' '))
	print "bb"
	board = makeMove(board, i, j, PLAYER)
	print "aaa"
	return board

def playTicTacToe():
	board = getEmptyBoard()

	value, board = alplaBetaPruning(board)
	print "Lets Start. I play first, human! \n"
	printBoard(board)

	while not getBoardState(board):
		
		nextBoard = getPlayerMove(board)
		
		while nextBoard == board:
			print "\nCan you not even play properly?\n"
			nextBoard = getPlayerMove(board)

		board = nextBoard
		printBoard(board)

		if getBoardState(board):
			break

		value, board = alplaBetaPruning(board)

		print "\nMy Turn. Prepare for the worst. \n"
		printBoard(board)

	status = getBoardState(board)

	if status == PLAYER_WIN:
		print "\nI Lose? Impossible! Something must be wrong!"
	elif status == CPU_WIN:
		print "\nI Win. As expected."
	else:
		print "\nIts a Draw! Good game human."

#playTicTacToe()