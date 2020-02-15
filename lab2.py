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

################################################################################
#  Evaluation function
# ------------------------------------------------------------------------------
#
def evaluate(state):
    pass

################################################################################
#  Cutoff test function - has terminal test inside it
# ------------------------------------------------------------------------------
#
def cutoff_test(state, depth):
    if depth == 4 or test_checkmate(state):
        return True
    return False

def test_checkmate(state):
    w_king, b_king = find_kings(state)
    pass

################################################################################
#  Return the list of all successor states for player given a certain state
# ------------------------------------------------------------------------------
#
def get_children(state, player):
    currentBoard = copy.deepcopy(state)
    listOfPossibleStates = []    # list of reachable states

    # if player == "WHITE":
    #      for i in range(0,state.numRows):
    #          for j in range(0,state.numColumns):
    #             if(currentBoard[i][j] == ' '):

    pass
################################################################################
#  Heuristic-Minimax Search
# ------------------------------------------------------------------------------
#
def alpha_beta_h_minimax(state, depth, alpha, beta, player):
    if cutoff_test(state, depth):
        return (evaluate(state), null)
    chosen_child = null

    if player == "WHITE":
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




















#Initially set alpha and beta to some "big" number, but make sure evaluation of terminal nodes
# are some bigger number so code breaks
