import argparse

from .clindoc import Clindoc, Builder
from .utils import format_parameters


def main():

    parser = argparse.ArgumentParser(
        prog='clindoc',
        description="Clindoc - Generate documentation for ASP files", epilog="KRR@UP - https://github.com/krr-up", usage='%(prog)s [options]')

    clindoc_cmd_usage = parser.add_argument_group('Global Clindoc parameters')

    clindoc_cmd_usage.add_argument('--project_name', '-p',
                                help='Name of the project')

    clindoc_cmd_usage.add_argument('--src_dir', '-s',
                                help='Directory containing the LP files from which to generate the documentation')

    clindoc_cmd_usage.add_argument('--description', '--desc',
                                action="store",
                                default='Default description',
                                help="Description of the project")

    clindoc_cmd_usage.add_argument('--doc-dir', '-d',
                                action="store",
                                type=str,
                                help="The folder where the documentation in rst format will be generated. If not specified, it will default to [src-dir]/docs/)")

    clindoc_cmd_usage.add_argument('--out-dir', '-b',
                                action="store",
                                type=str,
                                help="Directory where Sphinx will output the generated documentation (if not specified, defaults to [src-dir]/docs/build)")

    clindoc_cmd_usage.add_argument('--builder',
                                action="store",
                                type=str,
                                default="html",
                                help="Sphinx output format parameter (refer to parameter builder sphinx. Can be any builder supported by Sphinx)")

    clindoc_cmd_usage.add_argument('--clean',
                                action="store_true",
                                help="(flag) remove [doc-dir] and [out-dir] before running. Please be sure that you saved any hand-made modification")

    clindoc_cmd_usage.add_argument('--no-sphinx-build',
                                action="store_true",
                                help="(flag,debug) skip Sphinx build")

    clindoc_cmd_usage.add_argument('--no-rst-build',
                                action="store_true",
                                help="(flag,debug) skip rst build section")


    clindoc_cmd_usage.add_argument('--conf-filename',
                                action="store",
                                default=None,
                                help="Path to a configuration file (json format). It can be created from the --dump-conf [path_to_conf] command. Any parameters entered in the command line will be ignored.")

    clindoc_cmd_usage.add_argument('--dump-conf',
                                action="store",
                                default=None,
                                help="Path of a file where the configuration will be dumped. The json file will include all of the configuration you've entered in the command line. It can be used later as default configuration using --path-conf [path_to_conf]")



    parser.version = Clindoc.version

    clindoc_cmd_usage.add_argument('-v',
                                '--version',
                                action='version',
                                help='Print the version and exit')

    # Initialize documentation from components
    for cls in Builder.cls_components:
        cls.cmdline_documentation(parser)

    args = parser.parse_args()


    c = Clindoc(
                parameters = format_parameters(vars(args)))

    c.build_documentation()

