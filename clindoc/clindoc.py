from clingo import Control
from clingo.ast import ProgramBuilder, parse_files
from sphinx.application import Sphinx
from typing import List, Dict

from .astprogram import ASTProgram, Constraint
from .builder import Builder
from .utils import create_dir, get_dir_path

import os
import shutil

import json

class Clindoc:

    """
    project_name : Name of the project 
    src_dir : Directory containing the .lp files from which to generate the documentation
    parameters : Parameters for the different part of the app, inc. components, sphinx...
    """

    version = "0.1.0"

    def __init__(self,
                 project_name: str,
                 src_dir: str,
                 parameters: Dict) -> None:

        # Theses are not in parameters var because these are the parameters that can't have default values and are also the minimal variables required.
        self.project_name = project_name
        self.src_dir = get_dir_path(src_dir)

        # Change paths to absolute paths, set default values ...
        self.parameters = self._check_parameters(parameters)

    def _check_parameters(self, parameters: Dict):

        if not parameters.get('doc_dir'):
            parameters['doc_dir'] = os.path.join(
                self.src_dir, 'docs', 'source')

        if not parameters.get('out_dir'):
            parameters['out_dir'] = os.path.join(self.src_dir, 'docs', 'build')

        if not parameters.get('builder'):
            parameters['builder'] = "html"  # Default value

        if not parameters.get('clean'):
            parameters['clean'] = False
        
        if not parameters.get('no_sphinx_build'):
            parameters['no_sphinx_build'] = False

        if not parameters.get('description'):
            parameters['description'] = None

        return parameters

    def _load_folder(self) -> List[ASTProgram]:
        path = self.src_dir
        ret = []
        if not os.path.isdir(path) or not os.path.exists(path):
            raise ValueError(f"{path} is not a valid directory.")
        lp_files = []
        for root, dirs, files in os.walk(path):
            lp_files.extend([os.path.join(root, f)
                            for f in files if f.endswith(".lp")])

        for lp_file in lp_files:
            ret.append(self._load_file(lp_file))

        return ret

    def _load_file(self, path):
        Constraint.id = 0
        ctl = Control()
        with open(path) as f:
            file_lines = f.readlines()

        ast_list = []
        with ProgramBuilder(ctl) as _:
            parse_files([path], ast_list.append)

        return ASTProgram(ast_list, file_lines, path)

    def build_documentation(self) -> None:

        self.astprograms: List[ASTProgram] = self._load_folder()

        if len(self.astprograms) == 0:
            raise ValueError(f'Empty {self.parameters["src_dir"]} folder')



        if self.parameters['clean']:
            shutil.rmtree(self.parameters['doc_dir'])
            shutil.rmtree(self.parameters['out_dir'])
        
        create_dir(self.parameters['doc_dir'])


        self.builder = Builder(self.astprograms, self.parameters)
        self.builder.build()


        print(json.dumps(self.parameters,indent=4))


        self._sphinx_config = {
            "project": self.project_name,
            "html_theme": "sphinx_rtd_theme",
            'intersphinx_mapping': {
                'python': ('https://docs.python.org/3/', None),
                'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
            },
            'extensions': [
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
                    confoverrides=self._sphinx_config,
                    verbosity=1)
            s.build()
