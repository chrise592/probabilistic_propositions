This is a generic program for performing approximate inference in Bayesian Networks
of Bernoulli random variables (probabilistic proposition).

Program Specification
On startup the program should read a file (in the format described below) specifying a
Bayesian Networks of Bernoulli random variables. The file name, the number of samples to use,
and the inference algorithm should be read from the command line (in that order). The program
should work for any size network that will reasonably fit in memory.

After reading the file, the program should prompt the user for one of four commands,
Describe, Tell, Ask, and Quit. If any command is malformed the program should print
an error and prompt again.

The Describe command should print the available variables and if they are an evidence
variable or not, i.e. if a value is assigned to that node. The Quit command should simply
exit the program.

The Tell command should be of the form:

Tell VAR {0,1,?}

where VAR is a variable in the network, setting it to 0 or 1 respectively, or clearing it
in the case of ?.

The Ask command should be of the form:

Ask VAR

where VAR is any variable in the network, printing the P(VAR) using the selected
inference algorithm, either ”weighted” or ”gibbs”. If ”weighted” is specified, the program
should use the likelihood weighting approximate inference algorithm described in section
14.5 of your text (Figure 14.15). If ”gibbs” is specified, the program should use the Gibbs
sampling approximate inference algorithm described in section 14.5 of your text (Figure
14.16).

For example, to run your program on the BN described in the file test.net using 1000
samples and Gibbs sampling, the program would be invoked as

python bernoulli.py test.net 1000 gibbs

File Format
The file format is text based. The first line are two space separated integers, N and M,
specifying the number of nodes and connections in the network respectively. The next N
lines are single words indicating the text label for each node. The next M lines are space
separated words specifying the connections in the network, with the arc going from the
first to the second label. The last N lines specify the probability table of each node,
with the first word being the node label followed by P space separated floating point
numbers, one for each line of the associated probability table in lexical ordering of the
variable labels. Thus the total number of fields on the line depends on the in-degree of
that node. For example, the following text file describes the example Bayesian network
in the figure below.
3 2
A
B
C
A C
B C
A 0.3 0.7
B 0.75 0.25
C 0.1 0.3 0.45 0.15
