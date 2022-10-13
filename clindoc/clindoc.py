from clingo import Control
from clingo.ast import ProgramBuilder, parse_files
from .astprogram import ASTProgram
from .dependencygraph import DependencyGraph

from typing import List


class Clindoc:
    def __init__(self) -> None:
        self.astprograms: List[ASTProgram] = []

    def load_file(self, path):
        ctl = Control()
        astprog = ASTProgram(path)
        with ProgramBuilder(ctl) as _:
            parse_files([path], astprog)


        DependencyGraph(astprog)
        
