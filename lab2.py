import copy
import numpy as np
# State representation of matrices
#   Upper case: White pieces (can only move upward)
#   Lower case: Black pieces (can only move downward)
# King   (K, k)
# Queen  (Q, q)
# Rook   (R, r)
# Bishop (B, b)
# Knight (N, n)
# Pawn   (P, p)
initial_state_A = [
['_', '_', '_', '_', '_', '_', 'q', 'k'],
['_', '_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', '_', '_', 'P', '_', 'p'],
['_', '_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', '_', '_', '_', 'Q', 'P'],
['_', '_', '_', '_', '_', 'P', 'P', '_'],
['_', '_', '_', '_', 'R', '_', 'K', '_']
]

initial_state_B = [
['_', '_', 'B', '_', '_', '_', '_', '_'],
['_', '_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', 'K', '_', '_', '_', '_'],
['_', 'p', '_', '_', '_', '_', '_', '_'],
['_', '_', 'k', '_', '_', '_', '_', '_'],
['P', '_', '_', '_', '_', 'P', '_', '_'],
['_', 'B', '_', '_', '_', '_', '_', '_'],
['N', '_', '_', '_', '_', 'N', '_', '_']
]

initial_state_C = [
['_', '_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', 'K', '_', '_', '_', '_'],
['_', '_', 'R', '_', 'P', '_', '_', '_'],
['_', 'P', '_', 'k', 'r', '_', '_', '_'],
['_', '_', '_', 'N', 'p', 'b', '_', '_'],
['_', '_', '_', '_', 'P', '_', '_', '_'],
['_', '_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', '_', '_', 'N', '_', '_']
]

# Constants for Reinfield values
QUEEN  = 9
ROOK   = 5
BISHOP = 3
KNIGHT = 3
PAWN   = 1

# Max depth
MAX_DEPTH = 4

################################################################################
#  Evaluation function
# ------------------------------------------------------------------------------
#  Linear weighted sum of features
def evaluate(state):
    # Piece counts
    white_queen  = 0
    black_queen  = 0
    white_rook   = 0
    black_rook   = 0
    white_bishop = 0
    black_bishop = 0
    white_knight = 0
    black_knight = 0
    white_pawn   = 0
    black_pawn   = 0

    # Traverse over board and count number of each piece
    for row in range(len(state)):
        for col in range(len(state[0])):
            piece = state[row][col]
            if piece   == 'Q': white_queen  += 1
            elif piece == 'q': black_queen  += 1
            elif piece == "R": white_rook   += 1
            elif piece == "r": black_rook   += 1
            elif piece == "B": white_bishop += 1
            elif piece == "b": black_bishop += 1
            elif piece == "N": white_knight += 1
            elif piece == "n": black_knight += 1
            elif piece == "P": white_pawn   += 1
            elif piece == "p": black_pawn   += 1

    weighted_sum = (QUEEN  * (white_queen-black_queen)   +
                    ROOK   * (white_rook-black_rook)     +
                    BISHOP * (white_bishop-black_bishop) +
                    KNIGHT * (white_knight-black_knight) +
                    PAWN   * (white_pawn-black_pawn))

    return weighted_sum


################################################################################
#  Cutoff test function - has terminal test inside it
# ------------------------------------------------------------------------------
#
def cutoff_test(state, depth, player):
    is_max_depth = False
    is_checkmate = False

    if depth == MAX_DEPTH: # assuming that depth starts at 1
        is_max_depth = True
    if test_checkmate(state, player):
        is_checkmate = True

    return (is_max_depth, is_checkmate)

################################################################################
#  Check if current state is a terminal state/checkmate
# ------------------------------------------------------------------------------
#
def test_checkmate(state, player):
    # Get king position based on player
    enemy_king = 'k' if player == "WHITE" else 'K'
    king_row, king_col = 0, 0
    for row in range(len(state)):
        try:
            king_col = state[row].index(enemy_king)
            king_row = row
        except ValueError:
            continue

    is_checkmate = False
    # If the enemy king has no legal moves, this state is checkmate
    enemy_set, friendly_set = None, None

    if enemy_king == "k":
        enemy_set = set({'p', 'n', 'r', 'b', 'q', 'k'})
        friendly_set = set({'P', 'N', 'R', 'B', 'Q', 'K'})

    else:
        friendly_set = set({'p', 'n', 'r', 'b', 'q', 'k'})
        enemy_set = set({'P', 'N', 'R', 'B', 'Q', 'K'})


    return is_checkmate



################################################################################
#  Return the list of all successor states for player given a certain state
# ------------------------------------------------------------------------------
#
def get_children(state, player):
    currentBoard = copy.deepcopy(state)
    listOfPossibleStates = []    # list of reachable states

    if player == "WHITE":
        for i in range(0,len(currentBoard)):
            for j in range(0,len(currentBoard[0])):

                if(currentBoard[i][j] == 'P'):
                    move_pawn_white(currentBoard, listOfPossibleStates, j, i)

                elif(currentBoard[i][j] == 'N'):
                    move_knight_white(currentBoard, listOfPossibleStates, j, i)

                elif(currentBoard[i][j] == 'R'):
                    move_rook_white(currentBoard, listOfPossibleStates, j, i)

                elif(currentBoard[i][j] == 'B'):
                    move_bishop_white(currentBoard, listOfPossibleStates, j, i)

                elif(currentBoard[i][j] == 'Q'):
                    move_queen_white(currentBoard, listOfPossibleStates, j, i)

                elif(currentBoard[i][j] == 'K'):
                    move_king_white(currentBoard, listOfPossibleStates, j, i)


        return listOfPossibleStates

    elif(player == "BLACK"):
        for i in range(0,len(currentBoard)):
            for j in range(0,len(currentBoard[0])):
               if(currentBoard[i][j] == 'p'):
                   move_pawn_black(currentBoard, listOfPossibleStates, j, i)

               elif(currentBoard[i][j] == 'n'):
                   move_knight_black(currentBoard, listOfPossibleStates, j, i)

               elif(currentBoard[i][j] == 'r'):
                   move_rook_black(currentBoard, listOfPossibleStates, j, i)

               elif(currentBoard[i][j] == 'b'):
                   move_bishop_black(currentBoard, listOfPossibleStates, j, i)

               elif(currentBoard[i][j] == 'q'):
                   move_queen_black(currentBoard, listOfPossibleStates, j, i)

               elif(currentBoard[i][j] == 'k'):
                   move_king_black(currentBoard, listOfPossibleStates, j, i)

        return listOfPossibleStates

    else:
        pass


#Adds all possible moves for a given white pawn to the child list
def move_pawn_white(state, list, x_cord, y_cord):
    enemy_set = set({'p', 'n', 'r', 'b', 'q', 'k'})

    #Pawn moves forward by one
    if(y_cord - 1 >= 0):
        if(state[y_cord - 1][x_cord] == '_'):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 1][x_cord] = 'P'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    #Pawn takes enemy piece to the top right of it
    if((y_cord - 1) >= 0 and (x_cord + 1) < len(state)):
        if(state[y_cord - 1][x_cord + 1] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 1][x_cord + 1] = 'P'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    #Pawn takes enemy piece to the top left of it
    if((y_cord - 1) >= 0 and (x_cord - 1) >= 0):
        if(state[y_cord - 1][x_cord - 1] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 1][x_cord - 1] = 'P'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

#Adds all possible moves for a given white knight to the child list
def move_knight_white(state, list, x_cord, y_cord):
    friendly_set = set({'P', 'N', 'R', 'B', 'Q', 'K'})

    #Piece moves up one and left two
    if(y_cord - 1 >= 0 and x_cord - 2 >= 0):
        if(state[y_cord - 1][x_cord - 2] not in friendly_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 1][x_cord - 2] = 'N'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    #Piece moves up one and right two
    if(y_cord - 1 >= 0 and x_cord + 2 < len(state)):
        if(state[y_cord - 1][x_cord + 2] not in friendly_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 1][x_cord + 2] = 'N'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    #Piece moves up two and left one
    if(y_cord - 2 >= 0 and x_cord - 1 >= 0):
        if(state[y_cord - 2][x_cord - 1] not in friendly_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 2][x_cord - 1] = 'N'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    #Piece moves up two and right one
    if(y_cord - 2 >= 0 and x_cord + 1 < len(state)):
        if(state[y_cord - 2][x_cord + 1] not in friendly_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 2][x_cord +1] = 'N'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    #Piece moves down one and right two
    if(y_cord + 1 < len(state) and x_cord + 2 < len(state)):
        if(state[y_cord + 1][x_cord + 2] not in friendly_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 1][x_cord + 2] = 'N'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    #Piece moves down one and left two
    if(y_cord + 1 < len(state) and x_cord - 2 >= 0):
        if(state[y_cord + 1][x_cord - 2] not in friendly_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 1][x_cord - 2] = 'N'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    #Piece moves down 2 and right 1
    if(y_cord + 2 < len(state) and x_cord + 1 < len(state)):
        if(state[y_cord + 2][x_cord + 1] not in friendly_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 2][x_cord + 1] = 'N'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    #Piece moves down 2 and left 1
    if(y_cord + 2 < len(state) and x_cord - 1 >= 0):
        if(state[y_cord + 2][x_cord - 1] not in friendly_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 2][x_cord - 1] = 'N'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)


def move_rook_white(state, list, x_cord, y_cord):
    enemy_set = set({'p', 'n', 'r', 'b', 'q', 'k'})
    friendly_set = set({'P', 'N', 'R', 'B', 'Q', 'K'})

    # Move up direction
    for y in range(y_cord-1, -1, -1):
        if(state[y][x_cord] in friendly_set):
            break
        if(state[y][x_cord] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y][x_cord] = 'R'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)
            break
        if state[y][x_cord] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y][x_cord] = 'R'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move down direction
    for y in range(y_cord+1, len(state), 1):
        if(state[y][x_cord] in friendly_set):
            break
        if(state[y][x_cord] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y][x_cord] = 'R'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)
            break
        if state[y][x_cord] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y][x_cord] = 'R'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move left direction
    for x in range(x_cord-1, -1, -1):
        if(state[y_cord][x] in friendly_set):
            break
        if(state[y_cord][x] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord][x] = 'R'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)
            break
        if state[y_cord][x] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y_cord][x] = 'R'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move right direction
    for x in range(x_cord+1, len(state), 1):
        if(state[y_cord][x] in friendly_set):
            break
        if(state[y_cord][x] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord][x] = 'R'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)
            break
        if state[y_cord][x] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y_cord][x] = 'R'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)


def move_bishop_white(state, list, x_cord, y_cord):
    enemy_set = set({'p', 'n', 'r', 'b', 'q', 'k'})
    friendly_set = set({'P', 'N', 'R', 'B', 'Q', 'K'})
    inBounds = True

    # Move up-left direction
    y = y_cord
    x = x_cord
    while(inBounds):
        if(y - 1 >= 0 and x + 1 < len(state)):
            y = y - 1
            x = x + 1
            if(state[y][x] in friendly_set):
                break
            if(state[y][x] in enemy_set):
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'B'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
                break
            if state[y][x] == '_':
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'B'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
        else:
            inBounds = False

    # Move up-right direction
    inBounds = True
    y = y_cord
    x = x_cord
    while(inBounds):
        if(y - 1 >= 0 and x - 1 >= 0):
            y = y - 1
            x = x - 1
            if(state[y][x] in friendly_set):
                break
            if(state[y][x] in enemy_set):
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'B'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
                break
            if state[y][x] == '_':
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'B'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
        else:
            inBounds = False

    # Move down-left direction
    inBounds = True
    y = y_cord
    x = x_cord
    while(inBounds):
        if(y + 1 < len(state) and x - 1 >= 0):
            y = y + 1
            x = x - 1
            if(state[y][x] in friendly_set):
                break
            if(state[y][x] in enemy_set):
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'B'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
                break
            if state[y][x] == '_':
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'B'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
        else:
            inBounds = False

    # Move down-right direction
    inBounds = True
    y = y_cord
    x = x_cord
    while(inBounds):
        if(y + 1 < len(state) and x + 1 < len(state)):
            y = y + 1
            x = x + 1
            if(state[y][x] in friendly_set):
                break
            if(state[y][x] in enemy_set):
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'B'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
                break
            if state[y][x] == '_':
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'B'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
        else:
            inBounds = False

def move_queen_white(state, list, x_cord, y_cord):
    enemy_set = set({'p', 'n', 'r', 'b', 'q', 'k'})
    friendly_set = set({'P', 'N', 'R', 'B', 'Q', 'K'})
    inBounds = True

    # Move up-left direction
    y = y_cord
    x = x_cord
    while(inBounds):
        if(y - 1 >= 0 and x + 1 < len(state)):
            y = y - 1
            x = x + 1
            if(state[y][x] in friendly_set):
                break
            if(state[y][x] in enemy_set):
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'Q'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
                break
            if state[y][x] == '_':
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'Q'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
        else:
            inBounds = False

    # Move up-right direction
    inBounds = True
    y = y_cord
    x = x_cord
    while(inBounds):
        if(y - 1 >= 0 and x - 1 >= 0):
            y = y - 1
            x = x - 1
            if(state[y][x] in friendly_set):
                break
            if(state[y][x] in enemy_set):
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'Q'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
                break
            if state[y][x] == '_':
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'Q'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
        else:
            inBounds = False

    # Move down-left direction
    inBounds = True
    y = y_cord
    x = x_cord
    while(inBounds):
        if(y + 1 < len(state) and x - 1 >= 0):
            y = y + 1
            x = x - 1
            if(state[y][x] in friendly_set):
                break
            if(state[y][x] in enemy_set):
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'Q'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
                break
            if state[y][x] == '_':
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'Q'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
        else:
            inBounds = False

    # Move down-right direction
    inBounds = True
    y = y_cord
    x = x_cord
    while(inBounds):
        if(y + 1 < len(state) and x + 1 < len(state)):
            y = y + 1
            x = x + 1
            if(state[y][x] in friendly_set):
                break
            if(state[y][x] in enemy_set):
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'Q'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
                break
            if state[y][x] == '_':
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'Q'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
        else:
            inBounds = False

    # Move up direction
    for y in range(y_cord-1, -1, -1):
        if(state[y][x_cord] in friendly_set):
            break
        if(state[y][x_cord] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y][x_cord] = 'Q'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)
            break
        if state[y][x_cord] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y][x_cord] = 'Q'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move down direction
    for y in range(y_cord+1, len(state), 1):
        if(state[y][x_cord] in friendly_set):
            break
        if(state[y][x_cord] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y][x_cord] = 'Q'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)
            break
        if state[y][x_cord] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y][x_cord] = 'Q'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move left direction
    for x in range(x_cord-1, -1, -1):
        if(state[y_cord][x] in friendly_set):
            break
        if(state[y_cord][x] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord][x] = 'Q'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)
            break
        if state[y_cord][x] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y_cord][x] = 'Q'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move right direction
    for x in range(x_cord+1, len(state), 1):
        if(state[y_cord][x] in friendly_set):
            break
        if(state[y_cord][x] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord][x] = 'Q'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)
            break
        if state[y_cord][x] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y_cord][x] = 'Q'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

def move_king_white(state, list, x_cord, y_cord):
    enemy_set = set({'p', 'n', 'r', 'b', 'q', 'k'})
    friendly_set = set({'P', 'N', 'R', 'B', 'Q', 'K'})

    # Move up-left direction
    if(y_cord - 1 >= 0 and x_cord + 1 < len(state)):
        if(state[y_cord - 1][x_cord + 1] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 1][x_cord + 1] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

        if state[y_cord - 1][x_cord + 1] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 1][x_cord + 1] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move up-right direction
    if(y_cord - 1 >= 0 and x_cord - 1 >= 0):
        if(state[y_cord - 1][x_cord - 1] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 1][x_cord - 1] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

        if state[y_cord - 1][x_cord - 1] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 1][x_cord - 1] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move down-left direction
    if(y_cord + 1 < len(state) and x_cord - 1 >= 0):
        if(state[y_cord + 1][x_cord - 1] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 1][x_cord - 1] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

        if state[y_cord + 1][x_cord - 1] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 1][x_cord - 1] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move down-right direction
    if(y_cord + 1 < len(state) and x_cord + 1 < len(state)):
        if(state[y_cord + 1][x_cord + 1] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 1][x_cord + 1] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

        if state[y_cord + 1][x_cord + 1] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 1][x_cord + 1] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move up direction
    if(y_cord - 1 >= 0):
        if(state[y_cord - 1][x_cord] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 1][x_cord] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

        if state[y_cord - 1][x_cord] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 1][x_cord] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move down direction
    if(y_cord + 1 < len(state)):
        if(state[y_cord + 1][x_cord] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 1][x_cord] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

        if state[y_cord + 1][x_cord] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 1][x_cord] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move left direction
    if(x_cord - 1 >= 0):
        if(state[y_cord][x_cord - 1] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord][x_cord - 1] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

        if state[y_cord][x_cord - 1] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y_cord][x_cord - 1] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move right direction
    if(x_cord + 1 < len(state)):
        if(state[y_cord][x_cord + 1] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord][x_cord + 1] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

        if state[y_cord][x_cord + 1] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y_cord][x_cord + 1] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)


#Adds all possible moves for a given black pawn to the child list
def move_pawn_black(state, list, x_cord, y_cord):
    enemy_set = set({'P', 'N', 'R', 'B', 'Q', 'K'})

    #Pawn moves down by 1 space
    if(y_cord + 1 < len(state)):
        if(state[y_cord + 1][x_cord] == '_'):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 1][x_cord] = 'p'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    #Pawn takes piece to the bottom right of it
    if((y_cord + 1) < len(state) and (x_cord + 1) < len(state)):
        if(state[y_cord + 1][x_cord + 1] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 1][x_cord + 1] = 'p'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)
    #Pawn takes piece to the bottom left of it
    if((y_cord + 1) < len(state) and (x_cord - 1) >= 0):
        if(state[y_cord + 1][x_cord - 1] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 1][x_cord - 1] = 'p'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

#Adds all possible moves for a given white knight to the child list
def move_knight_black(state, list, x_cord, y_cord):
    friendly_set = set({'p', 'n', 'r', 'b', 'q', 'k'})

    #Piece moves up one and left two
    if(y_cord - 1 >= 0 and x_cord - 2 >= 0):
        if(state[y_cord - 1][x_cord - 2] not in friendly_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 1][x_cord - 2] = 'n'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    #Piece moves up one and right two
    if(y_cord - 1 >= 0 and x_cord + 2 < len(state)):
        if(state[y_cord - 1][x_cord + 2] not in friendly_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 1][x_cord + 2] = 'n'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    #Piece moves up two and left one
    if(y_cord - 2 >= 0 and x_cord - 1 >= 0):
        if(state[y_cord - 2][x_cord - 1] not in friendly_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 2][x_cord - 1] = 'n'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    #Piece moves up two and right one
    if(y_cord - 2 >= 0 and x_cord + 1 < len(state)):
        if(state[y_cord - 2][x_cord + 1] not in friendly_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 2][x_cord +1] = 'n'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    #Piece moves down one and right two
    if(y_cord + 1 < len(state) and x_cord + 2 < len(state)):
        if(state[y_cord + 1][x_cord + 2] not in friendly_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 1][x_cord + 2] = 'n'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    #Piece moves down one and left two
    if(y_cord + 1 < len(state) and x_cord - 2 >= 0):
        if(state[y_cord + 1][x_cord - 2] not in friendly_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 1][x_cord - 2] = 'n'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    #Piece moves down two and right one
    if(y_cord + 2 < len(state) and x_cord + 1 < len(state)):
        if(state[y_cord + 2][x_cord + 1] not in friendly_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 2][x_cord + 1] = 'n'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    #Pieces moves down two and left one
    if(y_cord + 2 < len(state) and x_cord - 1 >= 0):
        if(state[y_cord + 2][x_cord - 1] not in friendly_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 2][x_cord - 1] = 'n'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

def move_rook_black(state, list, x_cord, y_cord):
    friendly_set = set({'p', 'n', 'r', 'b', 'q', 'k'})
    enemy_set = set({'P', 'N', 'R', 'B', 'Q', 'K'})

    # Move up direction
    for y in range(y_cord-1, -1, -1):
        if(state[y][x_cord] in friendly_set):
            break
        if(state[y][x_cord] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y][x_cord] = 'R'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)
            break
        if state[y][x_cord] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y][x_cord] = 'R'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move down direction
    for y in range(y_cord+1, len(state), 1):
        if(state[y][x_cord] in friendly_set):
            break
        if(state[y][x_cord] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y][x_cord] = 'R'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)
            break
        if state[y][x_cord] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y][x_cord] = 'R'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move left direction
    for x in range(x_cord-1, -1, -1):
        if(state[y_cord][x] in friendly_set):
            break
        if(state[y_cord][x] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord][x] = 'R'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)
            break
        if state[y_cord][x] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y_cord][x] = 'R'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move right direction
    for x in range(x_cord+1, len(state), 1):
        if(state[y_cord][x] in friendly_set):
            break
        if(state[y_cord][x] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord][x] = 'R'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)
            break
        if state[y_cord][x] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y_cord][x] = 'R'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

def move_bishop_black(state, list, x_cord, y_cord):
    friendly_set = set({'p', 'n', 'r', 'b', 'q', 'k'})
    enemy_set = set({'P', 'N', 'R', 'B', 'Q', 'K'})
    inBounds = True

    # Move up-left direction
    y = y_cord
    x = x_cord
    while(inBounds):
        if(y - 1 >= 0 and x + 1 < len(state)):
            y = y - 1
            x = x + 1
            if(state[y][x] in friendly_set):
                break
            if(state[y][x] in enemy_set):
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'B'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
                break
            if state[y][x] == '_':
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'B'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
        else:
            inBounds = False

    # Move up-right direction
    inBounds = True
    y = y_cord
    x = x_cord
    while(inBounds):
        if(y - 1 >= 0 and x - 1 >= 0):
            y = y - 1
            x = x - 1
            if(state[y][x] in friendly_set):
                break
            if(state[y][x] in enemy_set):
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'B'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
                break
            if state[y][x] == '_':
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'B'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
        else:
            inBounds = False

    # Move down-left direction
    inBounds = True
    y = y_cord
    x = x_cord
    while(inBounds):
        if(y + 1 < len(state) and x - 1 >= 0):
            y = y + 1
            x = x - 1
            if(state[y][x] in friendly_set):
                break
            if(state[y][x] in enemy_set):
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'B'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
                break
            if state[y][x] == '_':
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'B'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
        else:
            inBounds = False

    # Move down-right direction
    inBounds = True
    y = y_cord
    x = x_cord
    while(inBounds):
        if(y + 1 < len(state) and x + 1 < len(state)):
            y = y + 1
            x = x + 1
            if(state[y][x] in friendly_set):
                break
            if(state[y][x] in enemy_set):
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'B'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
                break
            if state[y][x] == '_':
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'B'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
        else:
            inBounds = False

def move_queen_black(state, list, x_cord, y_cord):
    friendly_set = set({'p', 'n', 'r', 'b', 'q', 'k'})
    enemy_set = set({'P', 'N', 'R', 'B', 'Q', 'K'})
    inBounds = True

    # Move up-left direction
    y = y_cord
    x = x_cord
    while(inBounds):
        if(y - 1 >= 0 and x + 1 < len(state)):
            y = y - 1
            x = x + 1
            if(state[y][x] in friendly_set):
                break
            if(state[y][x] in enemy_set):
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'Q'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
                break
            if state[y][x] == '_':
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'Q'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
        else:
            inBounds = False

    # Move up-right direction
    inBounds = True
    y = y_cord
    x = x_cord
    while(inBounds):
        if(y - 1 >= 0 and x - 1 >= 0):
            y = y - 1
            x = x - 1
            if(state[y][x] in friendly_set):
                break
            if(state[y][x] in enemy_set):
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'Q'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
                break
            if state[y][x] == '_':
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'Q'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
        else:
            inBounds = False

    # Move down-left direction
    inBounds = True
    y = y_cord
    x = x_cord
    while(inBounds):
        if(y + 1 < len(state) and x - 1 >= 0):
            y = y + 1
            x = x - 1
            if(state[y][x] in friendly_set):
                break
            if(state[y][x] in enemy_set):
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'Q'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
                break
            if state[y][x] == '_':
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'Q'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
        else:
            inBounds = False

    # Move down-right direction
    inBounds = True
    y = y_cord
    x = x_cord
    while(inBounds):
        if(y + 1 < len(state) and x + 1 < len(state)):
            y = y + 1
            x = x + 1
            if(state[y][x] in friendly_set):
                break
            if(state[y][x] in enemy_set):
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'Q'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
                break
            if state[y][x] == '_':
                newBoard = copy.deepcopy(state)
                newBoard[y][x] = 'Q'
                newBoard[y_cord][x_cord] = '_'
                list.append(newBoard)
        else:
            inBounds = False

    # Move up direction
    for y in range(y_cord-1, -1, -1):
        if(state[y][x_cord] in friendly_set):
            break
        if(state[y][x_cord] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y][x_cord] = 'Q'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)
            break
        if state[y][x_cord] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y][x_cord] = 'Q'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move down direction
    for y in range(y_cord+1, len(state), 1):
        if(state[y][x_cord] in friendly_set):
            break
        if(state[y][x_cord] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y][x_cord] = 'Q'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)
            break
        if state[y][x_cord] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y][x_cord] = 'Q'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move left direction
    for x in range(x_cord-1, -1, -1):
        if(state[y_cord][x] in friendly_set):
            break
        if(state[y_cord][x] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord][x] = 'Q'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)
            break
        if state[y_cord][x] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y_cord][x] = 'Q'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move right direction
    for x in range(x_cord+1, len(state), 1):
        if(state[y_cord][x] in friendly_set):
            break
        if(state[y_cord][x] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord][x] = 'Q'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)
            break
        if state[y_cord][x] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y_cord][x] = 'Q'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

def move_king_black(state, list, x_cord, y_cord):
    friendly_set = set({'p', 'n', 'r', 'b', 'q', 'k'})
    enemy_set = set({'P', 'N', 'R', 'B', 'Q', 'K'})

    # Move up-left direction
    if(y_cord - 1 >= 0 and x_cord + 1 < len(state)):
        if(state[y_cord - 1][x_cord + 1] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 1][x_cord + 1] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

        if state[y_cord - 1][x_cord + 1] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 1][x_cord + 1] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move up-right direction
    if(y_cord - 1 >= 0 and x_cord - 1 >= 0):
        if(state[y_cord - 1][x_cord - 1] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 1][x_cord - 1] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

        if state[y_cord - 1][x_cord - 1] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 1][x_cord - 1] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move down-left direction
    if(y_cord + 1 < len(state) and x_cord - 1 >= 0):
        if(state[y_cord + 1][x_cord - 1] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 1][x_cord - 1] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

        if state[y_cord + 1][x_cord - 1] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 1][x_cord - 1] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move down-right direction
    if(y_cord + 1 < len(state) and x_cord + 1 < len(state)):
        if(state[y_cord + 1][x_cord + 1] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 1][x_cord + 1] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

        if state[y_cord + 1][x_cord + 1] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 1][x_cord + 1] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move up direction
    if(y_cord - 1 >= 0):
        if(state[y_cord - 1][x_cord] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 1][x_cord] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

        if state[y_cord - 1][x_cord] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 1][x_cord] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move down direction
    if(y_cord + 1 < len(state)):
        if(state[y_cord + 1][x_cord] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 1][x_cord] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

        if state[y_cord + 1][x_cord] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 1][x_cord] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move left direction
    if(x_cord - 1 >= 0):
        if(state[y_cord][x_cord - 1] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord][x_cord - 1] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

        if state[y_cord][x_cord - 1] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y_cord][x_cord - 1] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    # Move right direction
    if(x_cord + 1 < len(state)):
        if(state[y_cord][x_cord + 1] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord][x_cord + 1] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

        if state[y_cord][x_cord + 1] == '_':
            newBoard = copy.deepcopy(state)
            newBoard[y_cord][x_cord + 1] = 'K'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

################################################################################
#  Heuristic-Minimax Search
# ------------------------------------------------------------------------------
#
def alpha_beta_search(state, depth):
    value, chosen_state = max_value(state, float("-inf"), float("inf"), depth)

    return chosen_state

def max_value(state, alpha, beta, depth):
    is_max_depth, is_checkmate = cutoff_test(state, depth, "WHITE")
    if is_checkmate:
        return (1000/depth), state
    if is_max_depth:
        return evaluate(state), state

    value = float("-inf")
    chosen_state = None
    for child in get_children(state, "WHITE"):
        min_val, min_state = min_value(child, alpha, beta, depth+1)
        value = max(value, min_val)
        if value == min_val:
            chosen_state = child

        if value >= beta:
            return value, chosen_state
        alpha = max(alpha, value)

    return value, chosen_state

def min_value(state, alpha, beta, depth):
    is_max_depth, is_checkmate = cutoff_test(state, depth, "BLACK")
    if is_checkmate:
        return (1000/depth), state
    if is_max_depth:
        return evaluate(state), state

    value = float("inf")
    chosen_state = None
    for child in get_children(state, "WHITE"):
        max_val, max_state = max_value(child, alpha, beta, depth+1)
        value = min(value, max_val)
        if value == max_val:
            chosen_state = child

        if value <= alpha:
            return value, chosen_state
        beta = min(beta, value)

    return value, chosen_state

# Testing getChildren
# list = get_children(initial_state_A, 'WHITE')
# state_counter = 0
# print("List:")
# for lists in list:
#     print(np.matrix(lists))
#     print()
#     state_counter = state_counter + 1
# print("Branching factor: ", state_counter)

choice = alpha_beta_search(initial_state_A, 1)
print(np.matrix(choice))












#
#Initially set alpha and beta to some "big" number, but make sure evaluation of terminal nodes
# are some bigger number so code breaks

# OLD CODE BELOW

# def alpha_beta_h_minimax(state, depth, alpha, beta, player):
#     # Cutoff test checks both depth reached and checkmate status
#     is_max_depth, is_checkmate = cutoff_test(state, depth, player)
#     if is_checkmate:
#         return (1000/depth, None)
#     if is_max_depth:
#         return (evaluate(state), None)
#     chosen_child = None
#
#     if player == "WHITE":
#         # Put all child nodes into a priority queue based on distance moved / piece type
#         for child in get_children(state, player):
#             value = alpha_beta_h_minimax(child, depth+1, alpha, beta, "BLACK")
#             if value[0] > alpha:
#                 alpha = value[0]
#                 chosen_child = child
#             if beta <= alpha:
#                 break
#         return (alpha, chosen_child)
#
#     else: # player == "BLACK" #
#         for child in get_children(state, player):
#             value = alpha_beta_h_minimax(child, depth+1, alpha, beta, "WHITE")
#             if value[0] < beta:
#                 beta = value[0]
#                 chosen_child = child
#             if beta <= alpha:
#                 break
#             return(beta, chosen_child)
