import math
import random
import time

from helpers import jaccard

class MinHash():
    def __init__(self):
        # choose four random 8 bit tables
        self.t1 = [random.randint(0, 2**32 - 1) for _ in range(2**8)]
        self.t2 = [random.randint(0, 2**32 - 1) for _ in range(2**8)]
        self.t3 = [random.randint(0, 2**32 - 1) for _ in range(2**8)]
        self.t4 = [random.randint(0, 2**32 - 1) for _ in range(2**8)]

    def intern_hash(self, x):
        return self.t1[(x >> 24) & 0xff] ^ self.t2[(x >> 16) & 0xff ] ^\
            self.t3[(x >> 8) & 0xff] ^ self.t4[x & 0xff]

    def hash(self, L):
        return min([self.intern_hash(x) for x in L])

    def get_element(self, L):
        h = self.hash(L)
        for x in L:
            if self.intern_hash(x) == h:
                return x

class OneBitMinHash():
    def __init__(self, k):
        self.k = k
        self.hash_fcts = [MinHash() for _ in range(self.k)]

    def hash(self, q):
        h = 0
        for hash_fct in self.hash_fcts:
            h += hash_fct.hash(q) % 2
            h *= 2
        return h


class Index():
    def fit(self, X):
        pass

    def query(self, q, r):
        pass

class LSH(Index):
    def __init__(self, k, L):
        self.k = k
        self.L = L
        self.tables = [{} for _ in range(self.L)]

        self.hashes = [OneBitMinHash(k) for _ in range(self.L)]

    def fit(self, X):
        self.X = X
        for i, x in enumerate(self.X):
            self.hash_values = [h.hash(x) for h in self.hashes]
            for j, h in enumerate(self.hash_values):
                self.tables[j].setdefault(h, []).append(i)

    # return k nearest points to q found in candidate set
    def knn_query(self, q, k):
        self.hash_values = [h.hash(q) for h in self.hashes]
        res = []
        for i, h in enumerate(self.hash_values):
            res.extend(self.tables[i].get(h, []))
        len_with_duplicates = len(res)
        res = set(res)
        len_without_duplicates = len(res)
        res_w_distances = [(i, jaccard(q, self.X[i])) for i in res]

        return sorted(res_w_distances, key=lambda x:-x[1])[:k], len_with_duplicates, len_without_duplicates

    # return first point at distance at least r encountered
    def query_with_radius(self, q, r):
        t = time.time()
        self.hash_values = [h.hash(q) for h in self.hashes]
        for i, h in enumerate(self.hash_values):
            for c in self.tables[i].get(h, []):
                if self.X[c] != q and jaccard(q, self.X[c]) >= r:
                    return c, time.time() - t
        return None, time.time() - t

    def query_with_radius_random_start(self, q, r):
        t = time.time()
        start_bucket = random.choice(range(self.L))
        order = list(range(start_bucket, self.L)) + list(range(start_bucket))
        hash_values = [h.hash(q) for h in self.hashes]
        for i in order:
            for c in self.tables[i].get(hash_values[i], []):
                if self.X[c] != q and jaccard(q, self.X[c]) >= r:
                    return c, time.time() - t
        return None, time.time() - t

    def query_with_radius_uniform(self, q, r):
        t = time.time()
        self.hash_values = [h.hash(q) for h in self.hashes]
        res = []
        for i, h in enumerate(self.hash_values):
            res.extend(self.tables[i].get(h, []))
        len_with_duplicates = len(res)
        res = set(res)
        len_without_duplicates = len(res)
        res_w_distances = [i for i in res if q != self.X[i] and jaccard(q, self.X[i]) >= r]

        # return a random point
        if len(res_w_distances) > 0:
            return random.choice(res_w_distances), time.time() - t
        return None, time.time() - t

    def query_with_radius_uniform_output(self, q, r):
        t = time.time()
        self.hash_values = [h.hash(q) for h in self.hashes]
        res = []
        for i, h in enumerate(self.hash_values):
            res.extend(self.tables[i].get(h, []))
        len_with_duplicates = len(res)
        res = set(res)
        len_without_duplicates = len(res)
        return [i for i in res if q != self.X[i] and jaccard(q, self.X[i]) >= r], time.time() - t


