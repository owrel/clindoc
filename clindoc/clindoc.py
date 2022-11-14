from clingo import Control
from clingo.ast import ProgramBuilder, parse_files
from .astprogram import ASTProgram
from .definitiondependencygraph import DefinitionDependencyGraph
from .ruledependencygraph import RuleDependencyGraph

from .userdoc import UserDoc

from .contributordoc import ContributorDoc

from typing import List


class Clindoc:
    def __init__(self) -> None:
        self.astprograms: List[ASTProgram] = []

    def load_file(self, path):
        ctl = Control()
        with open(path) as f:
            file = f.readlines()
        
        ast_list = []
        with ProgramBuilder(ctl) as _:
            parse_files([path], ast_list.append)

        astprogram = ASTProgram(ast_list,file,path)
        
        DefinitionDependencyGraph(astprogram)
        RuleDependencyGraph(astprogram)


        cd = ContributorDoc(file,astprogram)
        cd.build_doc()





        
        # ud = UserDoc(file)
        # ud.parse_documentation()

        # with open("./out.md","w") as f:
        #     f.write(ud.build_md())


    
        
