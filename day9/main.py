# import reduce
from functools import reduce

FID, FS, FREE = 0, 1, 2
get_answer = lambda fs: reduce(lambda at, f: (at[0] + f[1] + f[2], at[1] + sum(range(at[0], at[0] + f[1])) * f[0]), fs, (0, 0))[1]

text = list(open("input.txt").read())
text = list(map(int, list(text)))

files = text[::2]
space = text[1::2] + [0]

""" Part 1 """
files_spaces = [ [fid, fs, s] for fs, s, fid in zip(files, space, range(len(files))) ]
at_left, at_right = 0, len(files_spaces) - 1

while at_left < at_right:
    while files_spaces[at_left][FREE] == 0: at_left += 1
    if files_spaces[at_right][FS] == 0: at_right -= 1

    if at_right <= at_left: break

    fid, fs, s = files_spaces[at_right]
    space_free = files_spaces[at_left][FREE]

    size = min(space_free, fs)

    files_spaces[at_left][FREE] = 0
    files_spaces[at_right][FS] -= size

    files_spaces = files_spaces[:at_left+1] + [[fid, size, space_free-size]] + files_spaces[at_left+1:at_right+1]

    at_right += 1

print("answer 1:", get_answer(files_spaces)) # 6331212425418

""" Part 2 """
files_spaces = [ [fid, fs, s] for fs, s, fid in zip(files, space, range(len(files))) ]
search_forward, search_backward = 0, 0

for i in range(len(files_spaces)-1, -1, -1):
    idx = i + search_backward
    while files_spaces[idx][FID] != i: idx -= 1

    fid, fs, s = files_spaces[idx]

    for idx_free in range(search_forward, idx):
        
        fid2, fs2, space_free = files_spaces[idx_free]

        if space_free == 0 and search_forward+1 == idx_free: search_forward += 1

        if fs <= space_free:
        
            if idx_free+1 == idx:
                files_spaces[idx][FREE] += space_free
                files_spaces[idx_free][FREE] = 0
            else:
                files_spaces[idx_free] = [fid2, fs2, 0]
                files_spaces[idx - 1][2] += fs + s
                files_spaces = files_spaces[:idx_free+1] + [[fid, fs, space_free - fs]] + files_spaces[idx_free+1:idx] + files_spaces[idx+1:]
                search_backward += 1
            break

print("Answer 2:", get_answer(files_spaces)) # 6363268339304