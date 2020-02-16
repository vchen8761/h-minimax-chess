import copy
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
def cutoff_test(state, depth):
    is_max_depth = False
    is_checkmate = False

    if depth == 4: # assuming that depth starts at 1
        is_max_depth = True
    if test_checkmate(state):
        is_checkmate = True

    return (is_max_depth, is_checkmate)

################################################################################
#  Check if current state is a terminal state/checkmate
# ------------------------------------------------------------------------------
#
def test_checkmate(state):
    return False



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

                if(currentBoard[i][j] == 'p'):
                    move_pawn_white(currentBoard, listOfPossibleStates, j, i)

                elif(currentBoard[i][j] == 'n'):
                    move_knight_white(currentBoard, listOfPossibleStates, j, i)

                elif(currentBoard[i][j] == 'r'):
                    move_rook_white(currentBoard, listOfPossibleStates, j, i)

                elif(currentBoard[i][j] == 'b'):
                    move_bishop_white(currentBoard, listOfPossibleStates, j, i)

                elif(currentBoard[i][j] == 'q'):
                    move_queen_white(currentBoard, listOfPossibleStates, j, i)

                elif(currentBoard[i][j] == 'k'):
                    move_king_white(currentBoard, listOfPossibleStates, j, i)


        return listOfPossibleStates

    elif(player == "BLACK"):
        for i in range(0,len(currentBoard)):
            for j in range(0,len(currentBoard[0])):
               if(currentBoard[i][j] == 'P'):
                   move_pawn(currentBoard, listOfPossibleStates, j, i)

               elif(currentBoard[i][j] == 'N'):
                   move_knight(currentBoard, listOfPossibleStates, j, i)

               elif(currentBoard[i][j] == 'R'):
                   move_rook(currentBoard, listOfPossibleStates, j, i)

               elif(currentBoard[i][j] == 'B'):
                   move_bishop(currentBoard, listOfPossibleStates, j, i)

               elif(currentBoard[i][j] == 'Q'):
                   move_queen(currentBoard, listOfPossibleStates, j, i)

               elif(currentBoard[i][j] == 'K'):
                   move_king(currentBoard, listOfPossibleStates, j, i)

               return listOfPossibleStates

    else:
        pass



def move_pawn_white(state, list, x_cord, y_cord):
    enemy_set = set({'P', 'N', 'R', 'B', 'Q', 'K'})

    if(y_cord - 1 >= 0):
        if(state[y_cord - 1][x_cord] == '_'):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 1][x_cord] = 'p'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    if((y_cord - 1) >= 0 and (x_cord + 1) < len(state)):
        if(state[y_cord - 1][x_cord + 1] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 1][x_cord + 1] = 'p'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    if((y_cord - 1) >= 0 and (x_cord - 1) >= 0):
        if(state[y_cord - 1][x_cord - 1] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord - 1][x_cord - 1] = 'p'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

def move_knight_white(state, list, x_cord, y_cord):
    pass

def move_rook_white(state, list, x_cord, y_cord):
    pass

def move_bishop_white(state, list, x_cord, y_cord):
    pass

def move_queen_white(state, list, x_cord, y_cord):
    pass

def move_king_white(state, list, x_cord, y_cord):
    pass



def move_pawn_black(state, list, x_cord, y_cord):
    enemy_set = set({'p', 'n', 'r', 'b', 'q', 'k'})

    if(y_cord + 1 < len(state)):
        if(state[y_cord + 1][x_cord] == '_'):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 1][x_cord] = 'p'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    if((y_cord + 1) < len(state) and (x_cord + 1) < len(state)):
        if(state[y_cord + 1][x_cord + 1] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 1][x_cord + 1] = 'p'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

    if((y_cord + 1) < len(state) and (x_cord - 1) >= 0):
        if(state[y_cord + 1][x_cord - 1] in enemy_set):
            newBoard = copy.deepcopy(state)
            newBoard[y_cord + 1][x_cord - 1] = 'p'
            newBoard[y_cord][x_cord] = '_'
            list.append(newBoard)

def move_knight_black(state, list, x_cord, y_cord):
    pass

def move_rook_black(state, list, x_cord, y_cord):
    pass

def move_bishop_black(state, list, x_cord, y_cord):
    pass

def move_queen_black(state, list, x_cord, y_cord):
    pass

def move_king_black(state, list, x_cord, y_cord):
    pass
################################################################################
#  Heuristic-Minimax Search
# ------------------------------------------------------------------------------
#
def alpha_beta_h_minimax(state, depth, alpha, beta, player):
    # Cutoff test checks both depth reached and checkmate status
    is_max_depth, is_checkmate = cutoff_test(state, depth)
    if is_checkmate:
        return (1000/depth, null)
    if is_max_depth:
        return (evaluate(state), null)
    chosen_child = null

    if player == "WHITE":
        # Put all child nodes into a priority queue based on distance moved / piece type
        for child in get_children(state, player):
            value = alpha_beta_h_minimax(child, depth+1, alpha, beta, "BLACK")
            if value > alpha:
                alpha = value
                chosen_child = child
            if beta <= alpha:
                break
        return (alpha, chosen_child)

    else: # player == "BLACK" #
        for child in get_children(state, player):
            value = alpha_beta_h_minimax(child, depth+1, alpha, beta, "WHITE")
            if value < beta:
                beta = value
                chosen_child = child
            if beta <= alpha:
                break
            return(beta, chosen_child)

def printBoard(list):
    for i in range(0,len(list)):
        for j in range(0, len(list[0])):
            print(list[i][j], end = ' ')
            print()


list = get_children(initial_state_A, 'WHITE')

print("List:")
printBoard(list)

print(evaluate(initial_state_A))













#
#Initially set alpha and beta to some "big" number, but make sure evaluation of terminal nodes
# are some bigger number so code breaks
