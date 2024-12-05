from functools import cmp_to_key

file = open("input.txt").read()
sortings, pages = file.split("\n\n")

sortings = [ list(map(int, sorting.split("|"))) for sorting in sortings.split("\n") ]
pages = [ list(map(int, page.split(","))) for page in pages.split("\n") ]

def my_sort(a, b):
    if [a, b] in sortings: return -1
    if [b, a] in sortings: return 1
    return 0

answer_1, answer_2 = 0, 0
for page in pages:
    page_sorted = sorted(page, key=cmp_to_key(my_sort))
    middle_number = page_sorted[len(page_sorted) // 2]
    
    if page == page_sorted:
        answer_1 += middle_number
    else:
        answer_2 += middle_number

print("Answer 1:", answer_1) # 5639
print("Answer 2:", answer_2) # 5273