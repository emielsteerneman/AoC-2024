import numpy as np
from collections import Counter

lines = open("input.txt").read().split("\n")
numbers = [ map(int, line.split("   ")) for line in lines ]
numbers = list(zip(*numbers))
n_left, n_right = map(np.array, map(sorted, numbers))
counter = Counter(n_right)

answer_1 = np.sum(np.abs(n_left-n_right))

answer_2 = sum( counter[_] * _ for _ in n_left)

print("Answer 1:", answer_1) # 1151792
print("Answer 2:", answer_2) # 21790168

