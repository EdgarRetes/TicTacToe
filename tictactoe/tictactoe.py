"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # If the game starts with X always, the player X moves when there are the same amount of X's as O's
    
    Xs = 0
    Os = 0

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == X:
                Xs += 1
            elif board[i][j] == O:
                Os += 1

    if Xs == Os:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Turn = player(board)
    actions = set()

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                actions.add((i, j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Raise exception for invalid movement
    if action not in actions(board):
        raise Exception("Invalid Action")
    
    # Create a copy of the board and then return the copy with the action
    board_copy = copy.deepcopy(board)
    board_copy[action[0]][action[1]] = player(board)
    return board_copy

# Functions to check if someone has won


def columns(board, player_):
    for j in range(len(board)):
        if board[0][j] == player_ and board[1][j] == player_ and board[2][j] == player_:
            return True
    return False

            
def rows(board, player_):
    for i in range(len(board)):
        if board[i][0] == player_ and board[i][1] == player_ and board[i][2] == player_:
            return True
    return False

            
def diagonals(board, player_):
    if board[0][0] == player_ and board[1][1] == player_ and board[2][2] == player_:
        return True
    if board[0][2] == player_ and board[1][1] == player_ and board[2][0] == player_:
        return True
    return False


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for player_ in [X, O]:
        if columns(board, player_) or rows(board, player_) or diagonals(board, player_):
            return player_
        
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # If there is an empty slot the game is not over

    empty = 0
    for row in board:
        for element in row:
            if element == EMPTY:
                empty += 1

    if empty == 0 or winner(board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)

    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0
    
# Maximum and minimum functions
    

def max_value(board):
    v = -math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        # Gets the max value based on the minimum value the opponent can get
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        # Gets the min value based on the max value the opponent can get
        v = min(v, max_value(result(board, action)))
    return v

    
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # Initialize variable for current player using player function

    current_player = player(board)

    if terminal(board):
        return None
    
    # Case if the current player for the ai is X

    elif current_player == X:
        moves = []
        for action in actions(board):
            v = min_value(result(board, action))
            moves.append((v, action))

        # Gets the optimal value and returns its corresponding actions based in its position in the list

        optimal = -math.inf
        index = 0
        optimal_index = None
        for value, action in moves:
            if value > optimal:
                optimal = value
                optimal_index = index
            index += 1

        return moves[optimal_index][1]

    # Case if the current player for the ai is O

    elif current_player == O:
        moves = []
        for action in actions(board):
            v = max_value(result(board, action))
            moves.append((v, action))

        # Gets the optimal value and returns its corresponding actions based in its position in the list

        optimal = math.inf
        index = 0
        optimal_index = None
        for value, action in moves:
            if value < optimal:
                optimal = value
                optimal_index = index
            index += 1

        return moves[optimal_index][1]
