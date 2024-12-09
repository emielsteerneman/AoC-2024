import numpy as np
from itertools import combinations

text = open("input.txt").read()
frequencies = set(text) - set("\n.#")
grid = np.array([ list(_) for _ in text.splitlines()])
H, W = grid.shape

anti_nodes_1 = set()
anti_nodes_2 = set()

for freq in frequencies:
    yx = list(zip(*(np.where(grid == freq))))
    yx = [np.array(_, dtype=int) for _ in yx]
    yx_pairs = list(combinations(yx, 2))

    in_grid = lambda p: 0 <= p[0] < H and 0 <= p[1] < W

    for p1, p2 in yx_pairs:

        if in_grid( c := p1 - (p2 - p1)):
            anti_nodes_1.add ( tuple(c) )
        if in_grid( c := p2 - (p1 - p2)):
            anti_nodes_1.add ( tuple(c) )

        for dir in [-1, 1]:
            i = 0
            while True:
                c = p1 + i * dir * (p2 - p1)
                if not in_grid(c): break
                anti_nodes_2.add(tuple(c))
                i += 1
                
print("Answer 1:", len(anti_nodes_1)) # 367
print("Answer 2:", len(anti_nodes_2)) # 1285