from clingo import Control
from clingo.ast import ProgramBuilder, parse_files
from sphinx.application import Sphinx
from typing import List, Dict

from .east import EnrichedAST
from .builder import Builder
from .utils import create_dir, get_dir_path
from .astline import Constraint

import os
import shutil
import json

"""
Clindoc (CLIngo DOCumentation) is a tool that provides a way to generate documentation from logic programs written in the ASP (Answer Set Programming => Clingo) language. 
It takes a directory containing .lp files as input and generates an output directory containing the documentation in a specified format (e.g HTML). 
The generated documentation contains information about the symbols, dependencies, and constraints in the logic programs, as well as any comments or documentation written within the .lp files themselves. 
Additionally, Clindoc allows for the specification of various parameters for the documentation generation process.
"""




class Clindoc:
    """
    Clindoc is a class for generating documentation for clingo programs.

    It loads clingo programs from a given directory, processes them, and generates reStructuredText files which can be then used to build the documentation using Sphinx.

    It takes an optional parameters argument which can contain the following fields:

    | Parameter       | Type                                                                                                     | Description                                                                                                                                 |
    |-----------------|----------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
    | src_dir         | (str)                                                                                                    | The directory containing the clingo files. If not provided, it defaults to the current directory.                                           |
    | doc_dir (str)   | The directory containing the documentation source files. If not provided, it defaults to <src_dir>/docs. |                                                                                                                                             |
    | out_dir         | (str)                                                                                                    | The directory where the documentation should be built. If not provided, it defaults to <doc_dir>/build.                                     |
    | project_name    | (str)                                                                                                    | The name of the project. If not provided, it defaults to 'Default Name'.                                                                    |
    | builder         | (str)                                                                                                    | The builder to use with Sphinx. If not provided, it defaults to 'html'.                                                                     |
    | clean           | (bool)                                                                                                   | Whether to clean the out_dir before building the documentation. If not provided, it defaults to False.                                      |
    | no_sphinx_build | (bool)                                                                                                   | Whether to run the Sphinx build command after generating the reStructuredText files. If not provided, it defaults to False.                 |
    | no_rst_build    | (bool)                                                                                                   | Whether to generate reStructuredText files or not. If not provided, it defaults to False.                                                   |
    | description     | (str)                                                                                                    | The description of the project. If not provided, it defaults to 'Default description'.                                                      |
    | conf_path       | (str)                                                                                                    | The path to a JSON configuration file. If provided, the options in the file will overwrite the options provided in the parameters argument. |
    | dump_conf       | (str)                                                                                                    | If provided, the current configuration will be dumped to the given file in JSON format.                                                     |
    :param parameters: A dictionary of parameters for the Clindoc object.
    
    """
    VERSION = "0.2.0"

    def __init__(self, parameters: Dict = {}) -> None:
        # Change paths to absolute paths, set default values ...
        self.parameters = self.check_parameters(parameters)

    @classmethod
    def load_folder(cls, parameters) -> List[EnrichedAST]:    
        """
        Load all .lp files in the given folder (recursively) and create EnrichedAST objects for each file.

        :param path: The path of the folder to load files from.
        :param parameters: A dictionary of parameters for the Clindoc object.
        :return: A list of EnrichedAST objects. 
        """
        ret = []

        path = parameters['src_dir']
        if not os.path.isdir(path) or not os.path.exists(path):
            raise ValueError(f"{path} is not a valid directory.")
        lp_paths = []
        for root, dirs, files in os.walk(path):
            lp_paths.extend([os.path.join(root, f)
                            for f in files if f.endswith(".lp")])

        for lp_path in lp_paths:
            ret.append(cls.load_file(lp_path, parameters))

        return ret

    @classmethod
    def load_file(cls, path, parameters):
        """
        Load the given file and create an EnrichedAST object for it.

        :param path: The path of the file to load.
        :param parameters: A dictionary of parameters for the Clindoc object.
        :return: An EnrichedAST object.
        """
        Constraint.id = 0
        ctl = Control()
        with open(path) as f:
            file_lines = f.readlines()

        ast_list = []
        with ProgramBuilder(ctl) as _:
            parse_files([path], ast_list.append)

        return EnrichedAST(ast_list, file_lines, path, parameters)

    
    def check_parameters(self, parameters: Dict):
        """
        Check and adjust the given parameters.

        :param parameters: A dictionary of parameters for the Clindoc object.
        :return: The adjusted parameters.
        """
        if 'conf_path' in parameters:
            if parameters['conf_path']:
                with open(parameters['conf_path'], 'r') as file:
                    parameters = json.loads(file.read())
        else:
            parameters['conf_path'] = None

        if not parameters.get('src_dir'):
            parameters['src_dir'] = '.'

        if not parameters.get('project_name'):
            parameters['project_name'] = 'Default Name'

        parameters['src_dir'] = get_dir_path(parameters['src_dir'])

        if not parameters.get('doc_dir'):
            parameters['doc_dir'] = os.path.join(
                parameters['src_dir'], 'docs')

        else:
            parameters['doc_dir'] = get_dir_path(parameters['doc_dir'])

        if not parameters.get('out_dir'):
            parameters['out_dir'] = os.path.join(
                parameters['src_dir'], 'docs', 'build')

        if not 'builder' in parameters:
            parameters['builder'] = "html"  # Default value

        if not 'clean' in parameters:
            parameters['clean'] = False

        if not 'no_sphinx_build' in parameters:
            parameters['no_sphinx_build'] = False

        if not 'no_rst_build' in parameters:
            parameters['no_rst_build'] = False

        if not 'description' in parameters:
            parameters['description'] = 'Default description'

        if not 'conf_path' in parameters:
            parameters['conf_path'] = None
        else:
            if parameters['conf_path']:
                parameters['conf_path'] = os.path.abspath(
                    parameters['conf_path'])

        if not 'dump_conf' in parameters:
            parameters['dump_conf'] = None
        else:
            if parameters['dump_conf']:
                parameters['dump_conf'] = os.path.abspath(
                    parameters['dump_conf'])
        return parameters

    def build_documentation(self) -> None:
        """
        Build the documentation and then pass it to Sphinx
        """
        self.easts: List[EnrichedAST] = self.load_folder(
            self.parameters)

        if len(self.easts) == 0:
            raise ValueError(f'Empty {self.parameters["src_dir"]} folder')

        if self.parameters['clean']:
            if os.path.exists(self.parameters['doc_dir']):
                shutil.rmtree(self.parameters['doc_dir'])

            if os.path.exists(self.parameters['out_dir']):
                shutil.rmtree(self.parameters['out_dir'])

        create_dir(self.parameters['doc_dir'])
        create_dir(self.parameters['out_dir'])

        self.builder = Builder(self.easts, self.parameters)

        if not self.parameters['no_rst_build']:
            self.builder.build()

        if self.parameters['dump_conf']:
            with open(self.parameters['dump_conf'], 'w') as file:
                file.write(json.dumps(self.parameters, indent=4))

        sphinx_config = {
            "project": self.parameters['project_name'],
            "html_theme": "sphinx_rtd_theme",
            'intersphinx_mapping': {
                'python': ('https://docs.python.org/3/', None),
                'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
            },
            'extensions': [
                "sphinx.ext.napoleon",
                'sphinx.ext.intersphinx'
            ]
        }
        if not self.parameters.get('no_sphinx_build'):
            s = Sphinx(self.parameters['doc_dir'],
                       confdir=None,
                       outdir=self.parameters['out_dir'],
                       doctreedir=os.path.join(
                           self.parameters['out_dir'], "pickle"),
                       buildername=self.parameters['builder'],
                       confoverrides=sphinx_config,
                       verbosity=1)
            s.build()
