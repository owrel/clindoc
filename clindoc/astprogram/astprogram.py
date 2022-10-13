from typing import List
from clingo.ast import AST
from .astnode import ASTNode


class ASTProgram:
    def __init__(self, path: str) -> None:
        self.astnodes: List[ASTNode] = []
        self._rawast: List[AST] = []
        self._path = path
        

        with open(path) as f:
            self.file = f.readlines()

    def get_pool(self):
        pass

    def get_nodes(self) -> List[ASTNode]:
        return self.astnodes

    def __call__(self, ast: AST) -> None:
        self.astnodes.append(ASTNode(ast, self.file))
        self._rawast.append(ast)


