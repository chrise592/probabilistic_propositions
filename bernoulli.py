# File: bernoulli.py
# Author: Chris Evers
# Date: 2 April 2018
# Description: Problem Set #3, Problem 10: Engineering Design Problem

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

where VAR is any variable in the network, printing the P(VAR) using the selected inference
algorithm, either "weighted" or "gibbs". If "weighted" is specified, the program
14.5 of your text (Figure 14.15). If "gibbs" is specified, the program should use the Gibbs
sampling approximate inference algorithm described in section 14.5 of your text (Figure 14.16).

For example, to run your program on the BN described in the file test.net using 1000
samples and Gibbs sampling, the program would be invoked as

python bernoulli.py test.net 1000 gibbs

"""
import argparse


class BayesianNetwork:
    """This class represents a Bayesian Network of Bernoulli random variable. Its constructor
    arguments include the file name specifying the network, the number of samples to use, and
    the inference algorithm."""
    def __init__(self, file, num_samples, algorithm):
        """Constructor for the BayesianNetwork class"""
        self.file = file
        self.num_samples = num_samples
        self.algorith = algorithm
        self.bn_graph = {}
        self.bn_table = {}
        self.vars = []
        self.constructBN()

    def constructBN(self):
        """Contruct the Bayesian network from the data passed to the parameters in __init__()."""
        n, m, line_num = 0, 0, 0
        for line in self.file:
            fields = line.split()
            if line_num == 0:
                n, m = int(fields[0]), int(fields[1])
            elif line_num <= n:
                self.vars.append(fields[0])
                self.bn_graph[fields[0]] = []
                self.bn_table[fields[0]] = []
            elif line_num <= n + m:
                self.bn_graph[fields[0]].append(fields[1])
            else:
                self.bn_table[fields[0]] = [float(x) for x in fields if fields.index(x) != 0]
            line_num += 1

    def describe(self):
        """This function prints the available variables and if they are an evidence
        variable or not."""
        for var in self.vars:
            print var + ': Evidence'
        print ''

    def tell(self, var, value):
        """This function tells the bayesian network information about a variable."""
        print ''

    def ask(self, var):
        """This function returns the value of a given variable after performing the
        specified inference algorithm."""
        print ''


def gibbs():
    """Gibbs inference algorithm."""
    pass


def weighted():
    """Weighted inference algorithm."""
    pass


# Run the program
if __name__ == '__main__':
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Bayesian Network of Bernoulli random variables')
    parser.add_argument('file', type=file)
    parser.add_argument('num_samples', type=int)
    parser.add_argument('algorithm', choices=['gibbs', 'weighted'])
    args = parser.parse_args()
    # Pass the values to the BayesianNetwork constructor
    bn = BayesianNetwork(args.file, args.num_samples, args.algorithm)
    # Call the appropriate functions depending on user input
    while True:
        # Request command
        args = raw_input('(Describe, Tell VAR {0, 1, ?}, Ask VAR, or Quit) \n> ').split()
        if args == []:
            print ''
            continue
        elif args[0] == 'Describe':
            # Print the available variables and if they are evidence or not
            if len(args) != 1:
                print 'Not a valid command. Usage: "Describe"\n'
            else:
                bn.describe()
        elif args[0] == 'Tell':
            # Tell the network the value of a certain variable: Tell VAR {0, 1, ?}
            if len(args) != 3:
                print 'Not a valid command. Usage: "Tell VAR {0, 1, ?}"\n'
            elif args[1] not in bn.vars:
                print 'Not a valid command. "' + args[1] + '" is not an available variable.\n'
            elif args[2] not in ['0', '1', '?']:
                print 'Not a valid command. Must assign "0", "1", or "?" to a variable.\n'
            else:
                bn.tell(args[1], args[2])
        elif args[0] == 'Ask':
            # Print P(VAR): Ask VAR
            if len(args) != 2:
                print 'Not a valid command. Usage: "Ask VAR"\n'
            elif args[1] not in bn.vars:
                print 'Not a valid command. "' + args[1] + '" is not an available variable.\n'
            else:
                bn.ask(args[1])
        elif args[0] == 'Quit':
            # Break out of the while loop
            if len(args) != 1:
                print 'Not a valid command. Usage: "Quit"\n'
            else:
                break
        else:
            print 'Not a valid command. Follow prompt guidelines.\n'

# End of program
