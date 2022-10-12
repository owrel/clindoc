from .astprogram import *
from .contributordoc import *
from .dependencygraph import *

from clingo import Control
from clingo.ast import ProgramBuilder, parse_files


class Clindoc:
    def __init__(self) -> None:
        self.astprogram = ASTProgram()

    
    def load_file(self, path):
        ctl = Control()
        with ProgramBuilder(ctl) as _:
            parse_files([path], self.astprogram)

    