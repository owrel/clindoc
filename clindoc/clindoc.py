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
            file_lines = f.readlines()
            file = f.read()

        with open(path) as f:
            file = f.read()
        
        ast_list = []
        with ProgramBuilder(ctl) as _:
            parse_files([path], ast_list.append)

        astprogram = ASTProgram(ast_list,file_lines,path)
        
        DefinitionDependencyGraph(astprogram)
        RuleDependencyGraph(astprogram)



        md = ""
        ud = UserDoc(file)
        ud.parse_documentation()
        m =ud.build_md() 
        if m :
            md += "\n# User documentation\n"
            md += m
        else :
            print('No User Documentation found')
        
        md += "\n# Contributor documentation\n"

        cd = ContributorDoc(file_lines,astprogram)
        md += cd.build_doc()

        md += f'\n![Definition Dependency Graph](DefinitionDependencyGraph.png)'
        md += f'\n![Rule Dependency Graph](RuleDependencyGraph.png)'

        
        
        with open("./out.md","w") as f:
            f.write(md)


    
        
