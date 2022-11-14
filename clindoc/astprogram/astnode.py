from typing import Dict, List
from clingo.ast import AST, ASTType, ASTSequence, SymbolicAtom, ConditionalLiteral



class ASTNode:
    def __init__(self, ast: AST, file: List[str]) -> None:

        self.type = ast.ast_type
        self.ast = ast
        self.comments = fetch_comments(self.ast, file)
        self._child_keys_separation = get_child_keys_separation(ast)
        self._raw = f"{ast}"
        
        # contraint
    def isconstraint(self):
        print(self.get_pool())
        for sym in  self.get_pool():
            if isinstance(sym,SymbolConstraint):
                return True
        return False

    def get_pool(self):
        ret = []
        for key in self._child_keys_separation:
            for sym in self._child_keys_separation[key]:
                ret.append(sym)
        return ret


            # # #                    # # #
            # Inner classes, methods ... #
            # # #                    # # #


class Symbol:
    def __init__(self,ast:SymbolicAtom) -> None:
        self.name = ast.symbol.name
        self.arguments = ast.symbol.arguments
        self.signature = f"{self.name}/{len(self.arguments)}"

class SymbolConstraint:
    constraint_id = 1
    def __init__(self,ast):
        self.signature = f"Constraint#{SymbolConstraint.constraint_id}"
        SymbolConstraint.constraint_id += 1 

        self.name = self.signature
        self.arguments = []
        

class SymbolSequence:
    def __init__(self) -> None:
        self._seq = {}

    def append(self, sym:Symbol):
        if sym.signature in self._seq:
            self._seq[sym.signature].append(sym)
        else:
            self._seq[sym.signature] = [sym]

    def __add__(self, sym:Symbol):
        self.append(sym)

    
    def __getitem__(self,name:str):
        return self._seq[name]

    def __len__(self):
        return len(self._seq)

    def __iter__(self):
        for key in self._seq:
            yield key

    def __str__(self):
        ret = ""
        for key in self._seq:
            ret += f"{key} : {self._seq[key]}\n" 
        return ret


def get_inner_symbolic_atoms(ast) -> SymbolSequence:

    def rec_inner_symbolic_atom(ast, ss:SymbolSequence) -> SymbolSequence:

        if isinstance(ast, ASTSequence):
            for _ast in ast:
                rec_inner_symbolic_atom(_ast, ss)
        else:
            if ast.ast_type == ASTType.BooleanConstant:
                ss.append(SymbolConstraint(ast))

            elif ast.ast_type == ASTType.SymbolicAtom:
                ss.append(Symbol(ast))
            else:
                if ast.child_keys:
                    for child in ast.child_keys:
                        rec_inner_symbolic_atom(eval(f'ast.{child}'), ss)

        return ss

    return rec_inner_symbolic_atom(ast, SymbolSequence())


def get_child_keys_separation(ast) -> Dict:
    
    ret = {}
    valid = 0
    for child in ast.child_keys:
        mem = get_inner_symbolic_atoms(eval(f'ast.{child}'))
        ret[child] = mem
        if mem:
            valid += 1
    if valid == 0 : return {}
    return ret


def fetch_comments(ast: AST, file: List[str], identificator="%-") -> List[str]:
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



