import re
import numpy as np

text = open("input.txt").read()

mul_regex = re.compile(r"mul\((\d+),(\d+)\)")

dos   = np.array([-1] + [ m.start() for m in re.finditer(r"do\(\)", text) ])
donts = np.array([-1] + [ m.start() for m in re.finditer(r"don't\(\)", text) ])
mults = [ (m.start(), m) for m in re.finditer(mul_regex, text) ]

answer_1, answer_2 = 0, 0

for mult_start, mult in mults:
    
    mult_answer = int(mult.group(1)) * int(mult.group(2))
    answer_1 += mult_answer
    
    if donts[donts < mult_start][-1] <= dos[dos < mult_start][-1]:
        answer_2 += mult_answer

print("Answer 1:", answer_1) # 166630675
print("Answer 2:", answer_2) # 93465710

