# i only got 14/15 with this code :( working on something better!
groups = [[], []] # 0 = same, 1 = diff

for g in groups:
    for _ in range(int(input())):
        g.append(input().split())
violations = len(groups[0])

for _ in range(int(input())):
    assigned = input().split()
    for i in range(len(groups)):
        for pair in groups[i]:
            c = i * 2 - 1
            m = len(set(assigned + pair))
            violations += (m == 3) * c
print(violations)
