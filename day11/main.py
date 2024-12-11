import numpy as np
from functools import lru_cache

@lru_cache(maxsize=None)
def rule(n):
    if n == 0: return [1]
    if (f := int(np.log10(n))) % 2 == 1: 
        f = 1 + f // 2
        a = n // (10**f)
        b = n % (a * 10**f)
        return [a, b]
    return [n * 2024]

@lru_cache(maxsize=None)
def blink(number, n):
    if n == 0: return 1
    return sum([blink(x, n-1) for x in rule(number)])

numbers = list(map(int, open('input.txt').read().split(' ')))
answer_1 = sum([blink(x, 25) for x in numbers])
answer_2 = sum([blink(x, 75) for x in numbers])

print("Answer 1:", answer_1) # 224529
print("Answer 2:", answer_2) # 266820198587914