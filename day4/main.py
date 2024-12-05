import numpy as np

text = open("input.txt").read()
matrix = [ list(_) for _ in text.split("\n") ]

W, H = len(matrix[0]), len(matrix)
directions = [ (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1) ]

answer_1 = 0

SEARCH = "XMAS"
for y in range(H):
    for x in range(W):
        for dx, dy in directions:
            for i in range(len(SEARCH)):
                if x + i*dx < 0 or W <= x + i*dx or y + i*dy < 0 or H <= y + i*dy:
                    break
                if matrix[y + i*dy][x + i*dx] != SEARCH[i]:
                    break
            else:
                answer_1 += 1

print("Answer 1:", answer_1) # 2454

answer_2 = 0

for x in range(1, H-1):
    for y in range(1, W-1):
        at = matrix[x][y]

        if at != "A": continue
        
        topleft = matrix[x-1][y-1]
        topright = matrix[x-1][y+1]
        bottomleft = matrix[x+1][y-1]
        bottomright = matrix[x+1][y+1]

        A = (topleft == "M" and bottomright == "S") or (topleft == "S" and bottomright == "M")
        B = (topright == "M" and bottomleft == "S") or (topright == "S" and bottomleft == "M")

        if A and B: answer_2 += 1

print("Answer 2:", answer_2) # 1858