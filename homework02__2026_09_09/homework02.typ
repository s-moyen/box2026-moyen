= BOX : Homework 02

== Question 1.

N/A

== Question 2-4.

#table(
  columns: (auto, auto, auto, auto, auto),
  align: horizon,
  table.header(
    [File], [Number of sequences], [Length (bases)], [Species], [Number of canonical 20-mers]  
  ),
  [`file1.fa`], [1],[$2.22 times 10^6$],[Streptococcus Pneumoniae],[$2.15 times 10^6$],
  [`file2.fa`], [1],[$2.99 times 10^4$],[SARS-CoV-2],[$2.99 times 10^4$],
  [`file3.fa`], [1],[$9.18 times 10^3$],[HIV],[$9.08 times 10^3$],
  [`file4.fa`], [7],[$2.55 times 10^6$],[Streptococcus],[$2.27 times 10^6$],
  [`file5.fa`], [1],[$2.97 times 10^4$],[SARS-CoV-2],[$2.85 times 10^4$],
  [`file6.fa`], [1],[$2.13 times 10^5$],[Streptoccocus],[$1.96 times 10^5$],
)

== Question 3.

While the fourth and sixth file both contain sequences from the Streptococcus genus, I could not identify exactly which species they were from.

== Question 4.

I made the decision to replace all ambiguities, assigning a fixed base to each ambiguity (eg. "Y" is always replaced by "C").

Calculating the Jaccard indexes for each pair of files yields the following table :

#table(
  columns: (auto, auto, auto, auto, auto, auto, auto),
  align: horizon,
  table.header(
    [], [`file1.fa`], [`file2.fa`], [`file3.fa`], [`file4.fa`] , [`file5.fa`], [`file6.fa`]
  ),
  [`file1.fa`], [$1$],[$1.85 times 10^(-6)$],[$0$],[$4.28 times 10^(-3)$],[$9.27 times 10^(-7)$],[$3.57 times 10^(-5)$],
  [`file2.fa`], [$1.85 times 10^(-6)$],[$1$],[$0$],[$0$], [$8.18 times 10^(-1)$], [$0$],
  [`file3.fa`], [$0$],[$0$],[1],[$0$], [$0$], [$0$],
  [`file4.fa`], [$4.28 times 10^(-3)$],[$0$],[$0$],[$1$], [$0$], [$8.92 times 10^(-2)$],
  [`file5.fa`], [$9.27 times 10^(-7)$],[$8.18 times 10^(-1)$],[$0$],[$0$], [$1$], [$0$],
  [`file6.fa`], [$3.57 times 10^(-5)$],[$0$],[$0$],[$8.92 times 10^(-2)$], [$0$], [$1$],
)

We notice that the table is symmetrical ($J(A, B) = J(B, A)$, so no surprises there) and that the diagonal is made of ones ($J(A, A) = 1$, again, no surprises).

What is more interesting to note is that file 3 has no similarity to any other file (being the only instance of HIV genome) and that files 2 and 5 have a lot of similarities to each other (as they are both genomes of SARS-CoV-2) but are very different from all other files.

Finally, we can see that files 1, 4 and 6 all have some amount of similarities to one another, but not nearly as much as between files 2 and 5. This is likely because, while they all come from members of the Streptoccocus genus, they do not come from the same species within that genus.

== Question 5.

Now, A is represented by `00`, C by `01`, G by `10`, and T by `11`.
