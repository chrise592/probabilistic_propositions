Chris Evers
Problem Set 3, Problem 10 Analysis
-------------------------------------
Network 1

3 2
A
B
C
A C
B C
A 0.3 0.7
B 0.75 0.25
C 0.1 0.3 0.45 0.15
--------------------------------------
Network 2

4 4
Cloudy
Sprinkler
Rain
WetGrass
Cloudy Sprinkler
Cloudy Rain
Sprinkler WetGrass
Rain WetGrass
Cloudy 0.5 0.5
Sprinkler 0.5 0.1
Rain 0.2 0.8
WetGrass .0 .9 .9 .99
--------------------------------------
Network 3

1 0
A
A 0.3 0.7
--------------------------------------
Network 4

2 1
A
B
A B
A 0.3 0.7
B 0.75 0.25
--------------------------------------
Network 5

4 3
A
B
C
D
A C
B C
C D
A 0.3 0.7
B 0.75 0.25
C 0.1 0.4 0.4 0.8
D 0.5 0.5
--------------------------------------
The above specified 5 different networks of varying size and CPT's.

                                    Analysis Chart

Num Samples                 | 10            |    100        | 500           |   1000        |
----------------------------|---------------|---------------|---------------|---------------|
Network 1                   |Gibbs:      0.2|Gibbs:     0.14|Gibbs:    0.154|Gibbs:    0.158|
P(C|A=1,B=1)                |Weighted:   0.1|Weighted:  0.16|Weighted: 0.156|Weighted: 0.152|
----------------------------|---------------|---------------|---------------|---------------|
Network 2                   |Gibbs:      1.0|Gibbs:     0.95|Gibbs:    0.963|Gibbs:    0.990|
P(Rain|Cloudy=1,WetGrass=1) |Weighted: 0.857|Weighted: 0.963|Weighted: 0.971|Weighted: 0.973|
----------------------------|---------------|---------------|---------------|---------------|
Network 3                   |Gibbs:      0.8|Gibbs:     0.65|Gibbs:    0.708|Gibbs:    0.689|
P(A)                        |Weighted:   0.7|Weighted:  0.73|Weighted:  0.67|Weighted: 0.717|
----------------------------|---------------|---------------|---------------|---------------|
Network 4                   |Gibbs:      0.2|Gibbs:     0.22|Gibbs:    0.234|Gibbs:    0.235|
P(B|A=1)                    |Weighted:   0.2|Weighted:  0.25|Weighted: 0.288|Weighted: 0.258|
----------------------------|---------------|---------------|---------------|---------------|
Network 5                   |Gibbs:     0.75|Gibbs:     0.51|Gibbs:    0.497|Gibbs:    0.478|
P(D|A=0,B=1)                |Weighted:   0.3|Weighted:   0.5|Weighted: 0.508|Weighted: 0.497|
----------------------------|---------------|---------------|---------------|---------------|

The above chart compares constant probabilities from each of the 5 networks, using various
numbers of samples, and both the Gibbs and Likelihood Weighting algorithms. Some conclusions
can be drawn about how each variable affects the outputted probability. First of all, as the
number of samples increased, the probabilities converged to actual probability given in the
CPT. In the case of network 5, where C is a hidden variable, the lower num_samples gave
very unreliable guesses. The Gibbs and Weighted algorithms also gave quite different results,
all things remaining constant. I think that the difference actualyl depends on the structure
of the network, because the values differed much in network 5, where it has an unknown hidden
variable. The algorithms also gave surprisingly different results in network 3, which only
has one variable. The weighted algorithm actually gave more consistent results, where Gibbs
varied more, with only one variable.
