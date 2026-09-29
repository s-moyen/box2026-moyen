from xopen import xopen
from readfa import readfq
import matplotlib.pyplot as plt
import networkx as nx

forward = "ecoli_sample_perfect_reads_forward.fasta.gz"
both_ways = "ecoli_sample_perfect_reads.fasta.gz"
error001 = "ecoli_sample_reads_001.fasta.gz"
error01 = "ecoli_sample_reads_01.fasta.gz"

files = [forward, both_ways, error001, error01]

file_path_gz = forward

searched_kmer = "CGCTCTGTGTGACAAGCCGGAAACCGCCCAG"

VERBOSE = False

class Dbg:
    def __init__(self):
        self.data = {}
        self.unexplored = []

    def add_node(self, node):
        if not node in self.data.keys():
            self.data[node] = [[], []]

    def add_edge(self, source, dest):
        if source in self.data.keys() and dest in self.data.keys():
            self.data[source][0].append(dest)
            self.data[dest][1].append(source)

    def unitig_from(self, s, building = False):
        if not s in self.data.keys():
            print(s, "was not found.")
            return

        if building:
            self.unexplored.remove(s)

        unitig = s
        current = s
        while len(self.data[current][1]) == 1:
            prev = self.data[current][1][0]

            if len(self.data[prev][0]) == 1:
                current = prev
                unitig = current[0] + unitig

                if building:
                    self.unexplored.remove(current)
            else:
                break


        current = s

        while len(self.data[current][0]) == 1:
            next = self.data[current][0][0]

            if len(self.data[next][1]) == 1:
                current = next
                unitig = unitig + current[-1]

                if building:
                    self.unexplored.remove(current)

            else:
                break

        return unitig

    def create_unitigs(self):
        self.unexplored = list(self.data.keys())
        unitigs = []
        while len(self.unexplored) > 0:
            new = self.unitig_from(self.unexplored[0], True)
            unitigs.append(new)
            print(len(self.unexplored), "left to go.")
        return unitigs

def base_comp(b):
    if b == "A":
        return "T"
    if b == "T":
        return "A"
    if b == "C":
        return "G"
    return "C"

def reverse_complement(seq):
    rev_comp = ""
    for b in seq[::-1]:
        rev_comp += base_comp(b)
    return rev_comp

def create_dbg_seq(seq, k):
    dbg = Dbg()
    for i in range(len(seq) - k + 1):
        u = seq[i:i+k]
        dbg.add_node(u)
        dbg.add_node(reverse_complement(u))
    for u in dbg.data.keys():
        for b in ["A", "T", "C", "G"]:
            v = u[1:]+b
            if u != v:
                dbg.add_edge(u, v)
    return dbg

def count_kmers(path, k):
    count = {}
    j = 1
    total = 30000
    c = 0
    with xopen(path) as fasta:
        for _,seq,_ in readfq(fasta):
            for i in range(len(seq) - k):
                c += 1
                u = seq[i:i+k]
                if u in count.keys():
                    count[u] += 1
                else:
                    count[u] = 1
                u = reverse_complement(u)
                if u in count.keys():
                    count[u] += 1
                else:
                    count[u] = 1
            if VERBOSE:
                print(j, "/", total)
                j += 1
    print(c)
    return count


def process_kmers(path, k):

    print("Processing file :", path)

    count = count_kmers(path, k)
    values = list(count.values())
    total = sum(values)

    print("Total :", total, "kmers processed.")
    print("Including", len(values), "unique kmers.")

    return values

def create_dbg(path, k, t = 1):
    dbg = Dbg()
    kmers = count_kmers(path, k)
    for u in kmers.keys():
        if kmers[u] >= t:
            dbg.add_node(u)
    print("Done calculating kmers.")
    total = len(dbg.data.keys())
    i = 1
    for u in dbg.data.keys():
        for b in ["A", "T", "C", "G"]:
            v = b+u[:-1]
            if u != v:
                dbg.add_edge(u, v)
        if VERBOSE:
            print(i, "/", total)
            i+=1
    return dbg

def dbg_to_nx(dbg):
    g = nx.DiGraph()
    for node in dbg.data.keys():
        g.add_node(node)

    for node in dbg.data.keys():
        print("Adding edges from", node)
        for next in dbg.data[node][0]:
            g.add_edge(node, next)
            print("Added an edge between", node, "and", next)
        print("Done")

    return g

def toy_graphs():
    options = {
        'node_size': 2000,
    }
    dbg = create_dbg_seq("ACGTACAGT", 5)
    g = dbg_to_nx(dbg)
    nx.draw_circular(g, with_labels=True, **options)
    plt.savefig("example_graph.png")

    plt.clf()
    dbg = create_dbg_seq("ACGTACGTA", 5)
    g = dbg_to_nx(dbg)
    nx.draw_circular(g, with_labels=True, **options)
    plt.savefig("repetition_graph.png")

    plt.clf()
    dbg = create_dbg_seq("ACGCACAGT", 5)
    g = dbg_to_nx(dbg)
    nx.draw_circular(g, with_labels=True, **options)
    plt.savefig("change_one_graph.png")


    
def plot_multiplicity():
    plt.figure()

    m1 = process_kmers(forward, 31)
    m2 = process_kmers(both_ways, 31)
    m3 = process_kmers(error001, 31)
    m4 = process_kmers(error01, 31)

    plt.subplot(221)
    plt.hist(m1, bins=max(m1))
    plt.title("Perfect reads, Forward only")

    plt.subplot(222)
    plt.hist(m2, bins=max(m2))
    plt.title("Perfect reads, Both directions")

    plt.subplot(223)
    plt.hist(m3, bins=max(m3))
    plt.title("Imperfect reads, 0.1% error")

    plt.subplot(224)
    plt.hist(m4, bins=max(m4))
    plt.title("Imperfect reads, 1% error")

    plt.tight_layout()

    plt.show()

def calc_on_samples():
    for i in range(1, 5):
        g1 = create_dbg(forward, 31, i)
        g2 = create_dbg(both_ways, 31, i)
        g3 = create_dbg(error001, 31, i)
        g4 = create_dbg(error01, 31, i)

        print("====== t =", i, "=======")

        print("Length of the specific unitig :")

        print("File 1 :", len(g1.unitig_from(searched_kmer)))
        print("File 2 :", len(g2.unitig_from(searched_kmer)))
        print("File 3 :", len(g3.unitig_from(searched_kmer)))
        print("File 4 :", len(g4.unitig_from(searched_kmer)))

        print("\n Sum of length of unitigs :")
        print("File 1 :", sum([len(e) for e in g1.create_unitigs()]))
        print("File 2 :", sum([len(e) for e in g2.create_unitigs()]))
        print("File 3 :", sum([len(e) for e in g3.create_unitigs()]))
        print("File 4 :", sum([len(e) for e in g4.create_unitigs()]))

toy_graphs()
#plot_multiplicity()
#calc_on_samples()


