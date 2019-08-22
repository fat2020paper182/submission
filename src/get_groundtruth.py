from helpers import jaccard
from minhash import LSH
from dataset_reader import read_data
import random
import pickle
import sys

def to_set(X):
    Y = [set(x) for x in X.values()]
    return Y

def bruteforce(X):
    distances = {}
    for i, x in enumerate(X):
        for y in X:
            distances.setdefault(i, []).append(jaccard(x, y))

    for k in distances:
        distances[k].sort(key=lambda x: -x)

    return distances

def find_interesting_queries(X, query_id):
    distances = bruteforce(X)

    if query_id:
        return [query_id], distances

    else:
        interesting_queries = []

        for k in distances:
            if distances[k][40] > 0.2:
                interesting_queries.append(k)


        print(len(interesting_queries))

        random.shuffle(interesting_queries)
        return interesting_queries[:50], distances

if __name__ == '__main__':
    ds = sys.argv[1]
    query_id = None
    if len(sys.argv) == 3:
        query_id = int(sys.argv[2])
    dataset = to_set(read_data(ds))
    print(len(dataset))
    queries, ground_truth = find_interesting_queries(dataset, query_id)

    with open(ds + '.pickle', 'wb') as f:
        pickle.dump([queries, ground_truth], f, pickle.HIGHEST_PROTOCOL)


