from helpers import jaccard, compute_recall, to_set
from minhash import LSH
from dataset_reader import read_data
import datetime
import math
import random
import pickle
import sys
import time

def compute_ball_ratio(queries, distances, r, cr):
    n_r, n_cr = 0, 0
    for q in queries:
        for d in distances[q]:
            if d >= r:
                n_cr += 1
                n_r += 1
            if d >= cr:
                n_cr += 1
            if d < cr:
                break

    return r, cr, n_cr, n_r, n_cr / n_r

if __name__ == '__main__':
    ds = sys.argv[1]
    r = float(sys.argv[2])
    reps = int(sys.argv[3])
    k = int(sys.argv[4])
    seed = int(sys.argv[5])

    #L = math.ceil((2/(1 + r))**k)
    L = math.ceil(math.log(0.01)/ math.log(1 - ((1 + r) / 2)**k))

    dataset = to_set(read_data(ds))

    print('time,method,r,k,L,seed,query_id,neighbor_id,query_time,index_build_time')

    with open(ds + '.pickle', 'rb') as f:
        queries, ground_truth = pickle.load(f)

    for _ in range(reps):
        index = LSH(k, L)
        t = time.time()
        index.fit(dataset)
        index_build_time = time.time() - t

        for q in queries:
            i, t = index.query_with_radius(dataset[q], r)
            print(datetime.datetime.now(), 'standard-high', r, k, L, seed, q, i, t, index_build_time, sep=',')
            i, t = index.query_with_radius_uniform(dataset[q], r)
            print(datetime.datetime.now(), 'uniform-high', r, k, L, seed, q, i, t, index_build_time, sep=',')
