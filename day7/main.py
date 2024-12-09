import re

def solve(at, to, parts, part2):
    if not len(parts): return at == to

    return solve(at * parts[0], to, parts[1:], part2) \
        or solve(at + parts[0], to, parts[1:], part2) \
        or (part2 and solve(int(str(at) + str(parts[0])), to, parts[1:], part2))

lines = open("input.txt").read().splitlines()
answer_1, answer_2 = 0, 0

for line in lines:
    numbers = re.findall(r"\d+|[+*]", line)
    answer, *parts = map(int, numbers)
    
    answer_1 += answer if solve(parts[0], answer, parts[1:], False) else 0
    answer_2 += answer if solve(parts[0], answer, parts[1:], True) else 0

print("Answer 1:", answer_1) # 4555081946288
print("Answer 2:", answer_2) # 227921760109726