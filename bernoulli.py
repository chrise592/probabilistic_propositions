# File: bernoulli.py
# Author: Chris Evers
# Date: 7 April 2018
# Description: Problem Set #3, Problem 10: Engineering Design Problem

"""The following repository which is offered by the recommended text, 'AIMA', was used for
reference in the creation of this python module:

    https://github.com/aimacode/aima-python

In this implementation, nodes in the Bayesian network can have, at most, 2 parents.

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

where VAR is any variable in the network, printing the P(VAR) using the selected inference
algorithm, either "weighted" or "gibbs". If "weighted" is specified, the program
14.5 of your text (Figure 14.15). If "gibbs" is specified, the program should use the Gibbs
sampling approximate inference algorithm described in section 14.5 of your text (Figure 14.16).

For example, to run your program on the BN described in the file test.net using 1000
samples and Gibbs sampling, the program would be invoked as

python bernoulli.py test.net 1000 gibbs

"""

import argparse
import random
from collections import defaultdict

#___________________________________________________________________________________________


def extend(s, var, val):
    """Copy the substitution s and extend it by setting var to val; return copy."""
    s2 = s.copy()
    s2[var] = val
    return s2


def event_values(event, variables):
    """Return a tuple of the values of variables in event."""
    if isinstance(event, tuple) and len(event) == len(variables):
        return event
    else:
        return tuple([event[var] for var in variables])


def normalize(vector):
    """Multiply each number by a constant such that the sum is 1.0."""
    total = float(sum(vector.values()))
    for val in vector:
        vector[val] /= total
    return vector


def probability(p):
    """Return true with probability p."""
    return p > random.uniform(0.0, 1.0)


def product(numbers):
    """Return the product of the numbers, e.g. product([2, 3, 10]) == 60"""
    result = 1
    for x in numbers:
        result *= x
    return result

#___________________________________________________________________________________________


class BayesianNetwork:
    """This class represents a Bayesian Network of Bernoulli random variable. Its constructor
    arguments include the file name specifying the network, the number of samples to use, and
    the inference algorithm."""

    values = [True, False]

    def __init__(self, file):
        """Constructor for the BayesianNetwork class"""
        self.nodes = []
        self.vars = []
        node_specs = {}
        n, m, line_num = 0, 0, 0
        for line in file:
            fields = line.split()
            if line_num == 0:
                n, m = int(fields[0]), int(fields[1])
            elif line_num <= n:
                node_specs[fields[0]] = [[], None]
            elif line_num <= n + m:
                node_specs[fields[1]][0].append(fields[0])
            else:
                if len(node_specs[fields[0]][0]) == 0:  # No parents, get probability of true value
                    node_specs[fields[0]][1] = float(fields[2])
                elif len(node_specs[fields[0]][0]) ==  1:  # One parent
                    node_specs[fields[0]][1] = {False: float(fields[1]),
                                                True: float(fields[2])}
                elif len(node_specs[fields[0]][0]) == 2:  # Two parents
                    node_specs[fields[0]][1] = {(False, False): float(fields[1]),
                                                (False, True): float(fields[2]),
                                                (True, False): float(fields[3]),
                                                (True, True): float(fields[4])}
                # Add node to Bayesian network
                self.add(fields[0], node_specs[fields[0]][0], node_specs[fields[0]][1])
            line_num += 1

    def add(self, X, parents, cpt):
        """Add a node to the network."""
        node = BayesianNode(X, parents, cpt)
        assert node.var not in self.vars
        assert all((parent in self.vars) for parent in node.parents)
        self.nodes.append(node)
        self.vars.append(node.var)
        for parent in node.parents:
            self.varNode(parent).children.append(node)

    def varNode(self, var):
        """Return the node for var."""
        for n in self.nodes:
            if n.var == var:
                return n
        raise Exception("No such variable: {}".format(var))


class BayesianNode:
    """A conditional probability distribution for a Bernoulli variable.
    Part of a BayesianNetwork."""

    def __init__(self, X, parents, cpt):
        """X is a variable name, parents is a sequence of variable names,
        cpt is the conditional probability table of the variable."""
        if isinstance(cpt, (float, int)):  # no parents
            cpt = {(): cpt}
        elif isinstance(cpt, dict):  # one parent
            if cpt and isinstance(list(cpt.keys())[0], bool):
                cpt = {(v,): p for v, p in cpt.items()}
        assert isinstance(cpt, dict)
        for vs, p in cpt.items():
            assert isinstance(vs, tuple) and len(vs) == len(parents)
            assert all(isinstance(v, bool) for v in vs)
            assert 0 <= p <= 1

        self.var = X
        self.parents = parents
        self.cpt = cpt
        self.children = []

    def p(self, value, event):
        """Return the conditional probability P(X=value | parents=parents_values),
        where parent_values are the values of parents in event."""
        assert isinstance(value, bool)
        ptrue = self.cpt[event_values(event, self.parents)]
        return ptrue if value else 1 - ptrue

    def sample(self, event):
        """Return True/False at random according with the conditional probability
        given the parents."""
        return probability(self.p(True, event))

#______________________________________________________________________________________


def likelihoodWeighting(X, e, bn, N):
    """The likelihood-weighting algorithm for inference in Bayesian networks.
    inputs: X, the query variable
            e, observed values for variables E
            bn, a Bayesian network specifying joint distribution P(X1,...,Xn)
            N, the total number of samples to be generated
    local variables: W, a vector of weighted counts for each value of X, initially zero
    """
    W = {x: 0 for x in bn.values}
    for j in range(N):
        x, w = weightedSample(bn, e)
        W[x[X]] += w
    return normalize(W)


def weightedSample(bn, e):
    """Each nonevidence variable is sampled according to the conditional distribution
    given the values already sampled for the variable's parents, while a weight is
    accumulated based on the likelihood for each evidence variable."""
    w, x = 1.0, dict(e)  # x is an event with n elements initialized from e
    for node in bn.nodes:
        Xi = node.var
        if Xi in e:
            w *= node.p(e[Xi], x)
        else:
            x[Xi] = node.sample(x)
    return x, w

#___________________________________________________________________________________________


def gibbsAsk(X, e, bn, N):
    """The Gibbs sampling algorithm for approximate inference in Bayesian networks;
    this version cycles through the variables, but choosing variables at random also works.
    local variables: count, a vector of counts for each value of X, initially zero
                     Z, the nonevidence variables in bn
                     x, the current state of the network, initially copied from e
    """
    assert X not in e, "Query variable must be distinct from evidence"
    counts = {x: 0 for x in bn.values}
    Z = [var for var in bn.vars if var not in e]
    x = dict(e)
    for Zi in Z:
        x[Zi] = random.choice(bn.values)
    for j in range(N):
        for Zi in Z:
            x[Zi] = sampleMarkovBlanket(Zi, x, bn)
            counts[x[X]] += 1
    return normalize(counts)


def sampleMarkovBlanket(X, e, bn):
    """Return a sample from P(x|mb) where mb (Markov blanket) of X is
    X's parents, children, and children's parents."""
    Xnode = bn.varNode(X)
    Q = {}
    for xi in bn.values:
        ei = extend(e, X, xi)
        # Equation 14.12
        Q[xi] = Xnode.p(xi, e) * product(Yj.p(ei[Yj.var], ei)
                                         for Yj in Xnode.children)
    return probability(normalize(Q)[True])

#______________________________________________________________________________________________


# Run the program
if __name__ == '__main__':
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Bayesian Network of Bernoulli random variables')
    parser.add_argument('file', type=file)
    parser.add_argument('num_samples', type=int)
    parser.add_argument('algorithm', choices=['gibbs', 'weighted'])
    args = parser.parse_args()
    N = args.num_samples
    if args.algorithm == 'gibbs':
        algorithm = gibbsAsk
    else:
        algorithm = likelihoodWeighting
    # Create the Bayesian network
    bn = BayesianNetwork(args.file)
    # Create evidence dict
    e = {}
    # Call the appropriate functions depending on user input
    while True:
        # Request command
        args = raw_input('(Describe, Tell VAR {0, 1, ?}, Ask VAR, or Quit)\n> ').split()
        if args == []:
            print ''
            continue
        elif args[0] == 'Describe':
            # Print the available variables and if they are evidence or not
            if len(args) != 1:
                print 'Not a valid command. Usage: "Describe"\n'
            else:
                for var in bn.vars:
                    if var in e.keys():
                        print var + ': evidence'
                    else:
                        print var + ': non-evidence'
                print ''
        elif args[0] == 'Tell':
            # Tell the network the value of a certain variable: Tell VAR {0, 1, ?}
            if len(args) != 3:
                print 'Not a valid command. Usage: "Tell VAR {0, 1, ?}"\n'
            elif args[1] not in bn.vars:
                print 'Not a valid command. "' + args[1] + '" is not an available variable.\n'
            elif args[2] not in ['0', '1', '?']:
                print 'Not a valid command. Must assign "0", "1", or "?" to a variable.\n'
            else:
                X = args[1]
                if args[2] == '0':
                    e[X] = False
                elif args[2] == '1':
                    e[X] = True
                elif args[1] in e.keys():
                    del e[X]
                print ''
        elif args[0] == 'Ask':
            # Print P(VAR): Ask VAR
            if len(args) != 2:
                print 'Not a valid command. Usage: "Ask VAR"\n'
            elif args[1] not in bn.vars:
                print 'Not a valid command. "' + args[1] + '" is not an available variable.\n'
            else:
                X = args[1]
                p = algorithm(X, e, bn, N)
                print 'P(' + X + ') =', p[True],'\n'
        elif args[0] == 'Quit':
            # Break out of the while loop
            if len(args) != 1:
                print 'Not a valid command. Usage: "Quit"\n'
            else:
                break
        else:
            print 'Not a valid command. Follow prompt guidelines.\n'

# End of program
