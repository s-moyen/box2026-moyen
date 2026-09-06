= BOX : Homework 01

== Question 1.

N/A

== Question 2.

After plugging various sequences from the file into NCBI BLAST, each query overwhelmingly finds similarities to known sequences of _Streptococcus Pneumoniae_, a species of bacteria. Therefore, it seems very likely that the given genome is from a _Streptococcus Pneumoniae_.

== Question 3.

The genome has the following subword complexity function :

#grid(
  columns: 2,
  [#figure(image("genome_complexity.png", width: 100%), caption: [Subword complexity of the genome in linear scale])],
  [#figure(image("genome_log_complexity.png", width: 100%), caption: [Subword complexity of the genome in logarithmic scale])],
)

== Question 4.

The random sequence has the following subword complexity function :

#grid(
  columns: 2,
  [#figure(image("random_complexity.png", width: 100%), caption: [Subword complexity of the random sequence in linear scale])],
  [#figure(image("random_log_complexity.png", width: 100%), caption: [Subword complexity of the random in logarithmic scale])],
)

== Question 5.

The Fibonacci sequence has the following subword complexity function :

#grid(
  columns: 2,
  [#figure(image("fibonacci_complexity.png", width: 80%), caption: [Subword complexity of the random sequence in linear scale])],
)

== Question 6.

We immediatly notice that the Fibonacci sequence has a linear subword complexity, meaning it is made from the same few patterns repeating themselves.

For both the random sequence and the genome, we can see that the complexity functions follow an exponential growth up to about $k = 10$, and then become constant at around 2 million unique subwords. This means that up to $k=10$, nearly every single possible $k$-subword appears in each sequence.

Since the entire genome contains just over 2 million bases, the $k$-subword count can never go above 2 million. Since it is about 2 million, this means that for $k>10$, nearly every $k$-subword in the genome (or the random sequence) is unique.
