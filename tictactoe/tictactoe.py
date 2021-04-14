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
    # calculate sum of number of Xs and Os in every row 
    Nx = board[0].count("X")+board[1].count("X")+board[2].count("X")
    No = board[0].count("O")+board[1].count("O")+board[2].count("O")

    if Nx > No: 
        return O    # if Nx is greater that means O's turn
    else:
        return X    # if Nx = No or No is greater, that means X's turn


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):  # for every row
        for j in range(3): # for every column
            if board[i][j] == EMPTY:    # if cell is empty, that means avialable action
                actions.add((i,j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    try:
        # deep copy the board, so that the change done on solution does not reflect on board
        solution = copy.deepcopy(board) 

        # replace cell located by action by current player symbole
        solution[action[0]][action[1]] = player(board) 
        return solution
    except:
        raise NameError("Wrong action input!") # raise exception if try code does not work properly


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # define set contains all cell indices that if are equal, will be a winner
    win_states = {((0,0),(0,1),(0,2)),
                ((1,0),(1,1),(1,2)),
                ((2,0),(2,1),(2,2)),
                ((0,0),(1,0),(2,0)),
                ((0,1),(1,1),(2,1)),
                ((0,2),(1,2),(2,2)),
                ((0,0),(1,1),(2,2)),
                ((0,2),(1,1),(2,0))}

    for win_state in win_states:
        # get values of each cell indicated by win_state indices
        a = board[win_state[0][0]][win_state[0][1]]
        b = board[win_state[1][0]][win_state[1][1]]
        c = board[win_state[2][0]][win_state[2][1]]
        # if they are equal and not empty, there is a winnew
        if a == b and a == c and a != EMPTY:
            # the winner is the last player 
            if player(board) == X: 
                return O
            elif player(board) == O:
                return X

    # return None if no winner
    return None 



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) in [X, O]: # if there is a winner, game is over
        return True
    else:
        # if empty cell still exists, game is still on
        for i in range(3):
            for j in range(3):
                if board[i][j] == None:
                    return False
        # if no emty cell, game is over
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    s = winner(board)
    if s == X:
        return 1
    elif s == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # if game is over, return None
    if terminal(board):
        return None
    
    if player(board) == X: # if current player is X 
        v = float("-inf") # initial score that Max player will never choose
        # loop over every action till get action with max value of min player "O" can optimally do
        for action in actions(board):
            min_v = Min_Value(result(board, action), v) # Min player will do the min of that result
            if min_v > v: # if score higher than last action, Max player should select it
                v = min_v
                a = action
        return a
    else: # if current player is O
        v = float("inf") # initial score that Min player will never choose
        # loop over every action till get action with min value of max player "X" can optimally do
        for action in actions(board):
            max_v = Max_Value(result(board, action), v) # Max player will do the max of that result
            if max_v < v: # if score is lower than last action, Min player should select it
                v = max_v
                a = action
        return a

# Max_Value and Min_Value are 2 nested function
# it breaks when reaches a terminal state
def Max_Value(board, v_ref):
    if terminal(board):
        return utility(board)
    v = float("-inf")
    for action in actions(board):
        v = max(v, Min_Value(result(board, action), v))
        # if result of that gets score higher than the state before in the higher level "line 170", 
        # return inf as the Max player will definitly select that action done on the parent rather than
        # the action before it.
        # And Min player in higher level will not select it.
        if v >= v_ref: 
            return float("inf")
    return v

def Min_Value(board, v_ref):
    if terminal(board):
        return utility(board)
    v = float("inf")
    for action in actions(board):
        v = min(v, Max_Value(result(board, action), v))
        # if result of that gets score lower than the state before in the higher level "line 158", 
        # return -inf as the Min player will definitly select that action done on the parent rather than 
        # the before before it.
        # And Max player in higher level will not select it.
        if v <= v_ref:
            return float("-inf")
    return v
