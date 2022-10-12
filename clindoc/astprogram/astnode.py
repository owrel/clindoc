from typing import Dict, List
from clingo.ast import AST, ASTType, ASTSequence, SymbolicAtom
from clorm import get_symbol_mode


def get_inner_symbolic_atoms(ast) -> List[SymbolicAtom]:
    def rec_inner_symbolic_atom(ast, l) -> List[SymbolicAtom]:

        if isinstance(ast, ASTSequence):
            for _ast in ast:
                rec_inner_symbolic_atom(_ast, l)
        else:

            if ast.ast_type == ASTType.SymbolicAtom:
                symbol = ast.symbol
                # Maybe returning a litle custum object ??
                l.append(symbol.name)
            else:
                if ast.child_keys:
                    for child in ast.child_keys:
                        rec_inner_symbolic_atom(eval(f'ast.{child}'), l)

        return l

    return rec_inner_symbolic_atom(ast, [])


def get_child_keys_separation(ast) -> Dict:
    ret = {}
    for child in ast.child_keys:
        mem = get_inner_symbolic_atoms(eval(f'ast.{child}'))
        if mem:
            ret[child] = mem
    return ret


def fetchcomments(ast: AST, file: List[str], identificator="%-") -> List[str]:
    lines = file.copy()
    lines = lines[:ast.location.begin.line-1]
    lines.reverse()
    comments = []
    for line in lines:
        if line.strip() and line.strip()[0:2] == identificator:
            comments.append(line.strip()[2:])
        else:
            break
    comments.reverse()
    return comments


class ASTNode:
    def __init__(self, ast: AST, file: List[str]) -> None:

        self.type = ast.ast_type
        self.ast = ast
        self.comments = fetchcomments(self.ast, file)

        self._inner_symatoms = get_inner_symbolic_atoms(ast)
        self._child_keys_separation = get_child_keys_separation(ast)
        self._raw = f"{ast}"
