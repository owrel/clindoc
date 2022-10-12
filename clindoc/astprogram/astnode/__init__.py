from typing import List
from clingo.ast import AST, ASTType, ASTSequence, SymbolicAtom
def get_inner_symbolic_atom(ast) -> List[SymbolicAtom]:
    def rec_inner_symbolic_atom(ast,l) -> List[SymbolicAtom]:
        # if child_keys -> can go further, otherwise, looking for ASTType.SymbolicAtom
        if isinstance(ast,ASTSequence):
            for _ast in ast:
                rec_inner_symbolic_atom(_ast,l)
        else:

            if ast.ast_type == ASTType.SymbolicAtom:
                symbol = ast.symbol
                #Maybe returning a litle custum object ??
                l.append(symbol.name)
            else:
                if ast.child_keys:
                    for child in ast.child_keys:
                        rec_inner_symbolic_atom(eval(f'ast.{child}'),l)
                
        return l

    return rec_inner_symbolic_atom(ast,[])


class ASTNode:
    def __init__(self,ast:AST) -> None:
        self._type = ast.ast_type
        self._inner_symatom = get_inner_symbolic_atom(ast)
        self._raw = f"{ast}"
        self.ast = ast

        