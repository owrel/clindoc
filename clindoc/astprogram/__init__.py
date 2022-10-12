from typing import List
from clingo.ast import AST
from .astnode import ASTNode

class ASTProgram:
    def __init__(self) -> None:
        self.astnodes:List[ASTNode] = []
        self._rawast : List[AST] = []

    def get_pool(self):
        pass

    def __call__(self, ast:AST) -> None:
        self.astnodes.append(ASTNode(ast))
        self._rawast.append(ast)

    
