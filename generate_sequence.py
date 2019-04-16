import argparse
from itertools import cycle
from random import choice, seed


seed(0)
alphabets = {'dna': 'AGCT',
             'rna': 'AGCU',
             'protein': 'ACDEFGHIKLMNPQRSTVWY'}
parser = argparse.ArgumentParser(description='Generates fasta file with given number of sequencess of given length.')
parser.add_argument("-type", nargs='?', type=str, default='range', choices=['rna', 'dna', 'protein'], help='type of molecule to generate sequence')
parser.add_argument('-number', nargs='?', type=int, default=1, help='number of sequences to generate')
parser.add_argument('-length', nargs='*', type=int, default=[100], help='lengths of sequences to generate')
parser.add_argument('-prefix', nargs='?', type=str, default='rna', help='prefix for names to be used')
parser.add_argument('-line_length', nargs='?', type=int, default=60, help='how many sequence letters to put in one line. If 0, sequence will be printed in one line.')
parser.add_argument('-out', nargs='?', type=str, default=None, help='output file name')

args = parser.parse_args()


def generate(code, length, alphabet, line_length):
    seq = [">" + args.prefix + ":" + str(length) + ":" + str(code)]
    if line_length == 0:
        str_length = length
        div = 1
        mod = 0
    else:
        str_length = line_length
        div = length // line_length
        mod = length % line_length
    seq += ["".join([choice(alphabet) for i in range(str_length)]) for j in range(div)] + ["".join([choice(alphabet) for i in range(mod)])] 
    return "\n".join(seq)


iter_length = cycle(args.length)
with open(args.out, 'w') as outfile:
    for number in range(args.number):
        outfile.write(generate(number, next(iter_length), alphabets[args.type], args.line_length))
        outfile.write("\n")
