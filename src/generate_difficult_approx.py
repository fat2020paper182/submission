import itertools
l = list(range(30))

nn = list(range(27))

l1 = list(range(18))
l2 = list(range(15, 30))

for x in list(itertools.combinations(l1, 17)) + list(itertools.combinations(l1, 16)) + list(itertools.combinations(l1, 15)):
    for y in x:
        print(y, end=' ')
    print()

print(" ".join([str(x) for x in l1]))
print(" ".join([str(x) for x in l2]))
print(" ".join([str(x) for x in nn]))
print(" ".join([str(x) for x in l]))







