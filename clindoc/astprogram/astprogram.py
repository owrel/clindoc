from typing import List,Set, Tuple
from clingo.ast import AST,ASTSequence,ASTType, SymbolicAtom
from enum import Enum

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



class Symbol:
    def __init__(self,ast:SymbolicAtom) -> None:
        self.name = ast.symbol.name
        self.arguments = {ast.symbol.arguments}
        self.signature = f"{self.name}/{len(ast.symbol.arguments)}"
        self.ast = set()
        self.dependencies = set()
        self._occurs = 1

    def __repr__(self) -> str:
        return self.name

    def get_signature(self) -> str:
        return self.signature


class SymbolHolder:
    def __init__(self) -> None:
        self._pool = {}

    def add(self,sym:Symbol)-> None:
        if sym.get_signature() in self._pool:
            self._pool[sym.get_signature()].dependencies.update(sym.dependencies)
            self._pool[sym.get_signature()].ast.update(sym.ast)
            self._pool[sym.get_signature()].arguments.update(sym.arguments)
            self._pool[sym.get_signature()]._occurs += 1
        else :
            self._pool[sym.get_signature()] = sym

    def get(self,signature:str) -> Symbol|None:
        return self._pool.get(signature)

    def __str__(self) ->str:
        ret =""
        for signature in self._pool:
            sym = self.get(signature)
            ret += signature + '\n'
            ret += f'\tDepends on: {list(sym.dependencies)}\n'
            ret += f'\tOccurs: {sym._occurs}\n'



        return ret 


def get_symbolic_atoms(ast: AST) -> Tuple[Set[Symbol], Set[Symbol]]:
    def rec_inner_symbolic_atom(ast:AST, sym:Set, dependencies:Set,trace:List  ):
        new_trace = trace.copy()
        if isinstance(ast, ASTSequence):
            new_trace.append('ASTSequence')
            for _ast in ast:
                rec_inner_symbolic_atom(_ast, sym,dependencies,new_trace)
        else:
            new_trace.append(ast.ast_type)
            if ast.ast_type == ASTType.SymbolicAtom:
                if 'head' in new_trace:
                    if 'head' in new_trace and ASTType.ConditionalLiteral in new_trace and 'condition' in new_trace:
                        dependencies.add(Symbol(ast))
                    else :
                        sym.add(Symbol(ast))
                elif 'body' :
                    dependencies.add(Symbol(ast))
                else:
                    sym.add(Symbol(ast))

            else:
                if ast.child_keys:
                    for child in ast.child_keys:
                        new_trace.append(child)
                        rec_inner_symbolic_atom(eval(f'ast.{child}'), sym,dependencies,new_trace)
                        new_trace.remove(child)
            return (sym,dependencies)
    syms, dependencies = rec_inner_symbolic_atom(ast, set(),set(),[])

    for s in syms:
        s.ast.add(ast)
        s.dependencies.update(dependencies)
    return (syms,dependencies)


class ASTProgram:
    def __init__(self, ast_list: List[AST], file: List[str], path) -> None:
        self.symbol_holer =SymbolHolder()
        self.astlines = [] 


        for ast in ast_list:
            define,dependencies  = get_symbolic_atoms(ast)
            for sym in define:
                self.symbol_holer.add(sym)

            al = ASTLine.factory(ast,define,dependencies)
            if al :
                self.astlines.append(al)
            
                

        for al in self.astlines:
            comments = fetch_comments(al.ast,file)
            al._comments = comments

        print('################')    
        print(self.symbol_holer)




class ASTLineType(Enum):
    Rule = 'Rule'
    Constraint = 'Constraint'
    Fact = 'Fact'

    Definition = 'Definition'
    Input = 'Input'
    Constant = 'Constant'
    Output = 'Output'


class ASTLine:
    def __init__(self,ast:AST,define:List[Symbol],dependencies:List[Symbol]) -> None:
        self._ast = ast
        self._define = define
        self._dependencies = dependencies
        self._comments = None
    
    @property
    def ast(self):
        return self._ast

    @property
    def define(self):
        return self._define

    @property
    def dependencies(self):
        return self._dependencies

    @property
    def type(self):
        return self._type

    @property
    def comments(self):
        return self.comments

    def factory(ast:AST,define:List[Symbol],dependencies:List[Symbol]):
        if ast.ast_type == ASTType.Rule:
            if define and dependencies :
                return Rule(ast,define,dependencies)
            elif define and not dependencies:
                return Fact(ast,define,dependencies)
            elif not define and dependencies:
                return Constraint(ast,define,dependencies)
            else :
                print('Problem')
        else:
            if ast.ast_type == ASTType.Defined:
                return Input(ast,define,dependencies)
            elif ast.ast_type == ASTType.Definition:
                return Definition(ast,define,dependencies)
            elif ast.ast_type == ASTType.ShowTerm:
                return Output(ast,define,dependencies)
            else:
                print(ast)
                print('To be ignore or not implemented yet')



class Rule(ASTLine):
    def __init__(self, ast: AST, define: List[Symbol], dependencies: List[Symbol]) -> None:
        super().__init__(ast, define, dependencies)
        self._type = ASTLineType.Rule

class Constraint(ASTLine):
    def __init__(self, ast: AST, define: List[Symbol], dependencies: List[Symbol]) -> None:
        super().__init__(ast, define, dependencies)
        self._type = ASTLineType.Fact

class Fact(ASTLine):
    def __init__(self, ast: AST, define: List[Symbol], dependencies: List[Symbol]) -> None:
        super().__init__(ast, define, dependencies)
        self._type = ASTLineType.Fact


class Definition(ASTLine):
    def __init__(self, ast: AST, define: List[Symbol], dependencies: List[Symbol]) -> None:
        super().__init__(ast, define, dependencies)
        self._type = ASTLineType.Definition


class Input(ASTLine):
    def __init__(self, ast: AST, define: List[Symbol], dependencies: List[Symbol]) -> None:
        super().__init__(ast, define, dependencies)
        self._type = ASTLineType.Input

class Output(ASTLine):
    def __init__(self, ast: AST, define: List[Symbol], dependencies: List[Symbol]) -> None:
        super().__init__(ast, define, dependencies)
        self._type = ASTLineType.Output


class Constant(ASTLine):
    def __init__(self, ast: AST, define: List[Symbol], dependencies: List[Symbol]) -> None:
        super().__init__(ast, define, dependencies)
        self._type = ASTLineType.Constant



# class Rule:
#     def __init__(self,ast:AST,define:List[Symbol],dependencies:List[Symbol]) -> None:
#         self.ast = ast
#         self.define = define
#         self.dependencies = dependencies
#         self.type = 'Rule'

#     def signature(self):
#         return self._signature

#     def pretty_rule(self):
#         return f"{self.signature()} | Line; {str(self.ast.location.begin.line)}" 






# class Constraint(Rule):
#     id = 1
#     def __init__(self, ast: AST, define: List[Symbol], dependencies: List[Symbol]) -> None:
#         super().__init__(ast, define, dependencies)
#         self.id = Constraint.id
#         Constraint.id += 1
#         self._signature = "Constraint#" + str(self.id)
#         self.type = 'Constraint'


    
# class Predicate(Rule):
#     def __init__(self, ast: AST, define: List[Symbol], dependencies: List[Symbol]) -> None:
#         super().__init__(ast, define, dependencies)
#         sign = ''
#         for d in self.define:
#             sign += d.signature + ' '
#         self._signature = sign
#         self.type = 'Predicate'
        


# class Fact(Rule):
#     def __init__(self, ast: AST, define: List[Symbol], dependencies: List[Symbol]) -> None:
#         super().__init__(ast, define, dependencies)
#         sign = ''
#         for d in self.define:
#             sign += d.signature + ' '
#         self._signature = sign
#         self.type = 'Fact'



# class Definition:
#     def __init__(self,ast:AST) -> None:
#         self.ast = ast

#     def factory(ast,symbols):
        


# class Input(Definition):
#     def __init__(self, ast: AST) -> None:
#         super().__init__(ast)
#         self.signature = f"{ast.name}/{ast.arity}"
#         self.type = 'Input'



# class Constant(Definition):
#     def __init__(self, ast: AST) -> None:
#         super().__init__(ast)
#         self.type = 'Constant'



# class Output(Definition):
#     def __init__(self, ast: AST, dependencies) -> None:
#         super().__init__(ast)
#         self.dependencies = dependencies
#         self.signature = self.ast.term.name + '/' +  str(len(self.ast.term.arguments))
#         self.type = 'Output'



