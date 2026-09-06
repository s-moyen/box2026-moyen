from random import randint
import matplotlib.pyplot as plt
import pylab

def compute_subwords(input, k):
    subwords = set()
    for w in [input[i : i+k] for i in range(len(input) - k)]:
        subwords.add(w)
    return subwords

def subword_complexity_sequence(input_sequence, k):
    subwords = set()
    for w in input_sequence:
        subwords = subwords.union(compute_subwords(w, k))
    return len(subwords)

def rand_word(k):
    word = ""
    letters = ["A", "T", "C", "G"]
    for i in range(k):
        word += letters[randint(0, 3)]
    return word

def fibo_step(word):
    next = ""
    for l in word:
        if l == "A":
            next += "AB"
        else:
            next += "A"
    return next

def fibo_word(k):
    word = "A"
    while len(word) < k:
        word = fibo_step(word)
    return word


def process_file(data):
    file_sequences = []
    rand_sequences = []
    fibo_sequences = []
    k = -1
    for line in data:
        if line[0] == ">":
            k += 1
            file_sequences.append("")
        else:
            file_sequences[k] += line[:-1]
    for k in range(len(file_sequences)):
        rand_sequences.append(rand_word(len(file_sequences[k])))
        fibo_sequences.append(fibo_word(len(file_sequences[k])))

    return file_sequences, rand_sequences, fibo_sequences


file = open("./genome_hw1.fa")
data = file.readlines()
sequences = process_file(data)

file_complexity = [0 for k in range(2, 31)]
rand_complexity = [0 for k in range(2, 31)]
fibo_complexity = [0 for k in range(2, 31)]


for k in range(2, 31):
    file_complexity[k-2] = subword_complexity_sequence(sequences[0], k)
    rand_complexity[k-2] = subword_complexity_sequence(sequences[1], k)
    fibo_complexity[k-2] = subword_complexity_sequence(sequences[2], k)
    print("Done calculating every " + str(k) + "-subword")
