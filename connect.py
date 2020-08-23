Red = "Red"
Blue = "Blue"

def initial_state():
    return [[None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None]]


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == Red or winner(board) == Blue:
        return True
    for row in board:
        if row.count(None) != 0:
            return False

    return True


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    Redcount = 0
    Bluecount = 0
    for row in board:
        Redcount += row.count(Red)
        Bluecount += row.count(Blue)
    return Red if Redcount == Bluecount else Blue


def winner(board):
    #check horizontal winner
    for row in board:
        potentialWinner = longestSubSequence(row)
        if potentialWinner != None:
            return potentialWinner

    #check vertical winner
    vertList = splitBoard(board, "vertical")
    for vert in vertList:
        potentialWinner = longestSubSequence(vert)
        if potentialWinner != None:
            return potentialWinner

    #check first diagonal
    diagonalList = splitBoard(board, "diagonal")
    for diag in diagonalList:
        potentialWinner = longestSubSequence(diag)
        if potentialWinner != None:
            return potentialWinner

    return None

def splitBoard(board, type):
    splitList = []
    if type == "vertical":
        for col in range(7):
            verticalList = []
            for row in range(6):
                verticalList.append(board[row][col])
            splitList.append(verticalList)
    elif type == "diagonal":
        for x in range(6):
            diagonal1, diagonal2 = [], []
            for y in range(7):
                if valid([x + 3 - y, y]):
                    diagonal1.append(board[x + 3 - y][y])
                if valid([x - 3 + y, y]):
                    diagonal2.append(board[x - 3 + y][y])
            splitList.append(diagonal1)
            splitList.append(diagonal2)

    return splitList


def valid(seq):
    return 0 <= seq[0] <= 5 and 0 <= seq[1] <= 6

def longestSubSequence(seq):
    #return player with sequence of 4 else None
    redSequence, blueSequence = 0, 0
    for color in seq:
        if color == Red:
            blueSequence = 0
            redSequence += 1
            if redSequence == 4:
                return Red
        elif color == Blue:
            redSequence = 0
            blueSequence += 1
            if blueSequence == 4:
                return Blue
        else:
            redSequence, blueSequence = 0, 0


    return None


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in range(7):
        raise Exception("illegal action")

    new_board = initial_state()

    for row in range(6):
        for column in range(7):
            if board[row][column] == Red:
                new_board[row][column] = Red
            elif board[row][column] == Blue:
                new_board[row][column] = Blue

    curr_player = player(board)

    for row in range(6):
        if new_board[5-row][action] == None:
            new_board[5 - row][action] = curr_player
            break

    return new_board


def possibleMoves(board):
    moveSet = set()

    for col in range(7):
        verticalList = []
        for row in range(6):
            verticalList.append(board[row][col])
        if verticalList.count(None) > 0:
            moveSet.add(col)

    return moveSet

def utility(board):

    if terminal(board) and winner(board) == Red:
        return 20
    if terminal(board) and winner(board) == Blue:
        return -20

    longestBlue, longestRed = 0, 0

    for row in board:
        curr_red = subsequence(row, Red)
        curr_blue = subsequence(row, Blue)
        if curr_red > longestRed:
            longestRed = curr_red
        if curr_blue > longestBlue:
            longestBlue = curr_blue

    columns = splitBoard(board, "vertical")
    for col in columns:
        curr_red = subsequence(col, Red)
        curr_blue = subsequence(col, Blue)
        if curr_red > longestRed:
            longestRed = curr_red
        if curr_blue > longestBlue:
            longestBlue = curr_blue

    diagonals = splitBoard(board, "diagonal")
    for dia in diagonals:
        curr_red = subsequence(dia, Red)
        curr_blue = subsequence(dia, Blue)
        if curr_red > longestRed:
            longestRed = curr_red
        if curr_blue > longestBlue:
            longestBlue = curr_blue

    return (longestRed**2)-(longestBlue**2)


def subsequence(seq, color):
    max_length, curr_length = 0, 0

    for value in seq:
        if value == color:
            curr_length += 1
            if curr_length > max_length:
                max_length = curr_length
        else:
            curr_length = 0

    return max_length

def AIalgo(board):

    if terminal(board):
        return None

    if player(board) == Blue:
        current_min = 100
        min_move = 0

        #run min_value on actions
        for move in possibleMoves(board):
            new_board = result(board, move)
            curr_val = max_value(new_board, 0)
            if curr_val < current_min:
                current_min = curr_val
                min_move = move

        return min_move

    else:
        current_max = -100
        max_move = 0
        #run max_value on actions
        for move in possibleMoves(board):
            new_board = result(board, move)
            curr_val = min_value(new_board, 0)
            if curr_val > current_max:
                current_max = curr_val
                max_move = move

        return max_move




def min_value(board, depth):
    if terminal(board):
        utility(board)


    if depth == 3:
        return utility(board)

    v = 100


    for action in possibleMoves(board):
        new_board = result(board, action)
        v = min(v, max_value(new_board, depth+1))

    return v


def max_value(board, depth):
    if terminal(board):
        utility(board)

    if depth == 3:
        return utility(board)

    v = -100


    for action in possibleMoves(board):
        new_board = result(board, action)
        v = max(v, min_value(new_board, depth+1))

    return v
