import readfa

def compute_subwords(input, k):
    subwords = set()
    for w in [input[i : i+k] for i in range(len(input) - k)]:
        subwords.add(w)
    return subwords
    
def process_base(base):
    if base.upper() in ["A", "D", "M", "R"]:
        return "A"
    if base.upper() in ["B", "C", "S", "Y"]:
        return "C"
    if base.upper() in ["G", "V", "K", "N"]:
        return "G"
    return "T"

def process_seq(seq):
    processed = ""
    for i in range(len(seq)):
        processed += process_base(seq[i])
    return processed

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

def canonical(seq):
    return min(seq, reverse_complement(seq))

def word_to_binary(word):
    BASES = {"A" : 0b00, "C":0b01, "G":0b10, "T":0b11}
    sum = 0
    for b in word:
        sum = 4 * sum + BASES[b]
    return sum

def compute_bin_subwords(input, k):
    subwords = compute_subwords(input, k)
    bin_subwords = set()
    for w in subwords:
        bin_subwords.add(word_to_binary(w))
    return bin_subwords

def reverse_complement_bin(binary, length):
    rev = ~binary
    revcomp = 0
    for i in range(length):
        rem = rev%4
        revcomp = revcomp * 4 + rem
        rev = rev//4
    return revcomp

def binary_canonical(binary, length = 20):
    return min(binary, reverse_complement_bin(binary, length))

files = [readfa.readfq(open("./file" + str(i) + ".fa")) for i in range(1, 7)]

subwords = [set() for i in range(6)]

canonical_subwords = [set() for i in range(6)]

jaccard_indexes = [[0 for i in range(6)] for j in range (6)]

for i in range(6):
    print("\n==========")
    print("File " + str(i + 1) + " :")
    for name, seq, qual in files[i] :
        seq = process_seq(seq)
        subwords[i] = subwords[i].union((compute_bin_subwords(seq, 20)))

    for u in subwords[i]:
        if not (binary_canonical(u) in canonical_subwords[i] or u in canonical_subwords):
            canonical_subwords[i].add(binary_canonical(u))

    for j in range(i+1):
        u_size = len(canonical_subwords[i].union(canonical_subwords[j]))
        i_size = len(canonical_subwords[i].intersection(canonical_subwords[j]))
        jaccard_indexes[i][j] = jaccard_indexes[j][i] = float(i_size)/float(u_size)


print("Numbers of 20-mers :",[len(subwords[i]) for i in range(6)])
print("Numbers of canonical 20-mers", [len(canonical_subwords[i]) for i in range(6)])
print("\nJaccard indexes :\n\n")
for l in jaccard_indexes:
    print(l)