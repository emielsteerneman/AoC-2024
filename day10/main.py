import numpy as np
from functools import reduce

text = open("input.txt", "r").read().splitlines()

matrix = np.array([ list(_) for _ in text ], dtype=int)
matrix_padded = np.zeros(matrix.shape + np.array([2, 2]), dtype=int) - 1
matrix_padded[1:-1, 1:-1] = matrix
matrix = matrix_padded

plus_mask = np.array([[0, 1, 0],[1, 0, 1],[0, 1, 0]])

def traverse(grid, at):
    level = grid[at]
    if level == 9: return [at]

    aty, atx = at
    submatrix = grid[aty-1:aty+2, atx-1:atx+2] * plus_mask
    
    coords = list(zip(*np.where(submatrix == level + 1)))
    coords = [ (y + aty - 1, x + atx - 1) for y, x in coords ]
    
    return reduce(lambda acc, coord: acc + traverse(grid, coord), coords, [])

trailheads = list(zip(*np.where(matrix == 0)))
peaks = [ traverse(matrix, coord) for coord in trailheads ]
print("Answer 1:", sum([ len(set(c)) for c in peaks ])) # 841
print("Answer 2:", sum([ len(c) for c in peaks ])) # 1875