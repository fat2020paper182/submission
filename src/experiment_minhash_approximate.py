from helpers import jaccard, compute_recall, to_set
from minhash import LSH
from dataset_reader import read_data
import datetime
import math
import random
import pickle
import sys
import time

if __name__ == '__main__':
    ds = sys.argv[1]
    r = float(sys.argv[2])
    reps = int(sys.argv[3])
    k = int(sys.argv[4])
    seed = int(sys.argv[5])
    outer_reps = int(sys.argv[6])
    c = float(sys.argv[7])

    L = math.ceil((2/(1 + r))**k)

    dataset = to_set(read_data(ds))

    print('time,method,r,c,k,L,seed,run,query_id,neighbor_id,query_time,index_build_time,prob')

    run = 0

    with open(ds + '.pickle', 'rb') as f:
        queries, ground_truth = pickle.load(f)

    for _ in range(outer_reps):
        index = LSH(k, L)
        t = time.time()
        index.fit(dataset)
        index_build_time = time.time() - t
        for _ in range(reps):
            for q in queries:
                neighbors, t = index.query_with_radius_uniform_output(dataset[q], r / c)
                for x in neighbors:
                    print(datetime.datetime.now(), 'uniform-approximate', r, c, k, L, seed, run, q, x, t, index_build_time, len(neighbors), sep=',')
                run += 1
