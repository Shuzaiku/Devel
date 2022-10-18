groups = [[],[]] # 0 = same, 1 = diff
assigned = []

for g in groups:
    for _ in range(int(input())):
        g.append(input().split())
violations = len(groups[0])

for a in range(int(input())):
    assigned.append(input().split())

for i in range(len(groups)):
    g = groups[i]
    increase = i * 2 - 1

    for pair in g:
        for a in assigned:
            union_len = len(set(a + pair))
            violations += union_len == 3 and increase or 0 # 3 means there's a pair of duplicates
print(violations)