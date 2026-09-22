from readfa import readfq
from simreads import simulate_reads_of_fixed_size
import numpy as np
from python_tsp.exact import solve_tsp_branch_and_bound

SEQ_LENGTH = 20_000
READ_LENGTH = 100

def overlap_size(u, v):
    size = min(len(u), len(v))
    overlap_size = 0 
    for i in range(1, size+1):
        if u[-i:] == v[:i]:
            overlap_size = i
    return overlap_size

def merge_words(u, v):
    size = overlap_size(u, v)
    return u + v[size:]

def find_biggest_overlap(reads):
    max_size = 0
    max_i = 0
    max_j = 1
    for i in range(len(reads)):
        for j in range(len(reads)):
            size = overlap_size(reads[i], reads[j]) 
            if j != i and size> max_size:
                max_size, max_i, max_j = size, i, j
    return max_i, max_j


def greedy_scs(reads):
    while len(reads) > 1:
        i, j = find_biggest_overlap(reads)
        reads[i] = merge_words(reads[i], reads[j])
        del reads[j]
    return reads[0]

def solve_using_tsp(reads):
    size = len(reads)
    graph = np.zeros((size+1, size+1))
    for i in range(size):
        for j in range(size):
            graph[i][j] = READ_LENGTH - overlap_size(reads[i], reads[j])
        graph[i][-1] = READ_LENGTH
    # Technically, the solver finds a Hamiltonian cycle. 
    # However, this definition allows for a trick : 
    # since all cycles must include an edge leaving v_f and we know that edge has weight 0,
    # this cycle has the same weight as a path that ends in v_f.
    return solve_tsp_branch_and_bound(graph)



file = open("./genome.fa")
genome = readfq(file)
sequence = ""
for name, seq, qual in genome:
    sequence = seq[:SEQ_LENGTH]
reads = simulate_reads_of_fixed_size(sequence, READ_LENGTH)
