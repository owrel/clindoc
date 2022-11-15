import argparse


parser = argparse.ArgumentParser(
    description="Clindoc - Gernerate documentation for ASP files", epilog="KRR@UP - https://github.com/krr-up")

parser.add_argument('file',
                    action='store',
                    type=str,
                    nargs="+",
                    help='file(s) to generate the documentation from')


parser.version = "0.0.1"
parser.add_argument('-v',
                    '--version',
                    action='version',
                    help='print the version and exit')

# Action tree
parser.add_argument('--output-type', "-o",
                    action="store",
                    default="markdown",
                    type=str,
                    help="type format of the output (markdown(=default),html,pdf)")


parser.add_argument('--rule-dependency-graph', '--rdg',
                    action="store_true",
                    help="include rule dependency graph")

parser.add_argument('--rule-dependency-graph', '--rdg',
                    action="store_true",
                    help="include rule dependency graph")

parser.add_argument('--definition-dependency-graph', '--ddg',
                    action="store_true",
                    help="include definition dependency graph")