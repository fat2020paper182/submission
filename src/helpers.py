def jaccard(X, Y):
    return len(X & Y) / len(X.union(Y))

def compute_recall(ground_truth, res):
    return len([x for x in res if x[1] >= ground_truth[-1] - 1e-6])/ len(ground_truth)

def to_set(X):
    Y = [set(x) for x in X.values()]
    return Y
