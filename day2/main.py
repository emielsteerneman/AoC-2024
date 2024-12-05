import numpy as np

reports = open("input.txt").read().splitlines()
reports = [list(map(int, report.split())) for report in reports]

slope_check = lambda l: np.all( (1 <= np.abs(np.diff(l))) & (np.abs(np.diff(l)) <= 3) )
direction_check = lambda l: np.abs( np.sum(np.sign(np.diff(l))) ) == len(l) - 1

answer_1 = sum([slope_check(report) & direction_check(report) for report in reports])

print("Answer 1:", answer_1) # 502

n_valid = 0
for row in reports:
    matrix = np.array([np.delete(row, i) for i in range(len(row))])
    slope = np.apply_along_axis(slope_check, 1, matrix)
    direction = np.apply_along_axis(direction_check, 1, matrix)
    n_valid += np.any( slope & direction )

print("Answer 2:", n_valid)