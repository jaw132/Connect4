# Define the two players
Red = "Red"
Blue = "Blue"

# Initialise the empty 6x7 connect4 grid
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
    # To determine a winner, each horizontal, vertical and diagonal line has to be checked for a contiguous sequence of 4 colours
    
    #check for horizontal winner
    for row in board:
        potentialWinner = longestSubSequence(row)
        if potentialWinner != None:
            return potentialWinner

    #check for vertical winner
    vertList = splitBoard(board, "vertical")
    for vert in vertList:
        potentialWinner = longestSubSequence(vert)
        if potentialWinner != None:
            return potentialWinner

    #check for diagonal winner
    diagonalList = splitBoard(board, "diagonal")
    for diag in diagonalList:
        potentialWinner = longestSubSequence(diag)
        if potentialWinner != None:
            return potentialWinner

    return None

# Split the board into its component rows/columns based on the parameter
# e.g. if vertical is passed then a list of all the columns is returned
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

# Checks if index is on the grid
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

    # initailise new board as to not overwrite current state, will be important as the minimax algorithm is called recursively
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

# Returns the set of possible moves for the current player
def possibleMoves(board):
    moveSet = set()

    for col in range(7):
        verticalList = []
        for row in range(6):
            verticalList.append(board[row][col])
        if verticalList.count(None) > 0:
            moveSet.add(col)

    return moveSet

# Non linear utility function that determines the current state of a given board, a positive value indicates the red player has the 
# advantage and a negative value the blue player.
def utility(board):

    # If a player wins then assign a high value of 20
    if terminal(board) and winner(board) == Red:
        return 20
    if terminal(board) and winner(board) == Blue:
        return -20

    # Loop over all vertical, horizontal and diagonal subsequence and find the longest subsequence for each player
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

    ''' Return the longest red sequence squared minus the longest blue sequence squared, this flags up dangerous longer sequences
    e.g. 3^2-2^2 = 5 whereas 2^2-1^2 = 3, even though in both cases the difference in sequence length is one, the blue player will realise
    the first case is a worse position to be in'''
    return (longestRed**2)-(longestBlue**2)

# Finds longest subsequence for passed color
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

# Returns the optimal move for the AI to make 
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



# Returns the minimum utility of the possible moves assuming the opponent will chose the maximum
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

# Returns the maximum utility of the possible moves assuming the opponent will chose the minimum
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
