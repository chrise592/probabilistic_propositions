# File: bernoulli.py
# Author: Chris Evers
# Date: 2 April 2018
# Purpose: Problem Set #3, Problem 10: Engineering Design Problem

"""On startup the program should read a file (in the format described below) specifying a
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

"""
import argparse

class BayesianNetwork:
    """This class represents a Bayesian Network of Bernoulli random variable. Its constructor
    arguments include the file name specifying the network, the number of samples to use, and
    the inference algorithm."""
    def __init__(self, filename, num_samples, algorithm):
        """Constructor for the BayesianNetwork class"""
        pass

# Run the program
if __name__ == '__main__':
    # Parse the command line arguments
    # Pass the values to the BayesianNetwork constructor
    # Call the appropriate functions depending on user input
    pass

