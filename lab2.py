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
[‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘q’, ‘k’],
[‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’],
[‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘P’, ‘_’, ‘p’],
[‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’],
[‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’],
[‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘Q’, ‘P’],
[‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘P’, ‘P’, ‘_’],
[‘_’, ‘_’, ‘_’, ‘_’, ‘R’, ‘_’, ‘K’, ‘_’]
]

initial_state_B = [
[‘_’, ‘_’, ‘B’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’],
[‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’],
[‘_’, ‘_’, ‘_’, ‘K’, ‘_’, ‘_’, ‘_’, ‘_’],
[‘_’, ‘p’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’],
[‘_’, ‘_’, ‘k’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’],
[‘P’, ‘_’, ‘_’, ‘_’, ‘_’, ‘P’, ‘_’, ‘_’],
[‘_’, ‘B’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’],
[‘N’, ‘_’, ‘_’, ‘_’, ‘_’, ‘N’, ‘_’, ‘_’]
]

initial_state_C = [
[‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’],
[‘_’, ‘_’, ‘_’, ‘K’, ‘_’, ‘_’, ‘_’, ‘_’],
[‘_’, ‘_’, ‘R’, ‘_’, ‘P’, ‘_’, ‘_’, ‘_’],
[‘_’, ‘P’, ‘_’, ‘k’, ‘r’, ‘_’, ‘_’, ‘_’],
[‘_’, ‘_’, ‘_’, ‘N’, ‘p’, ‘b’, ‘_’, ‘_’],
[‘_’, ‘_’, ‘_’, ‘_’, ‘P’, ‘_’, ‘_’, ‘_’],
[‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘_’],
[‘_’, ‘_’, ‘_’, ‘_’, ‘_’, ‘N’, ‘_’, ‘_’]
]