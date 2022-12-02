from typing import List, Set, Tuple
from clingo.ast import AST, ASTSequence, ASTType, SymbolicAtom, Variable, Location
from enum import Enum


def fetch_comments(ast: AST, file: List[str], identificator="%-") -> List[str]:
    lines = file.copy()
    lines = lines[:ast.location.begin.line]
    lines.reverse()
    comments = []
    for idx,line in enumerate(lines):
        
        if identificator in line:
            if idx == 0:
                comments.append(line[line.index(identificator)+len(identificator):].strip())
            if idx >0 and line.strip()[:len(identificator)] == identificator:
                comments.append(line[line.index(identificator)+len(identificator):].strip())
            else:
                break
        elif line.strip():
            print(line)
            break
    comments.reverse()
    return comments

class ASTProgram:
    def __init__(self, ast_list: List[AST], file_lines: List[str], path:str) -> None:
        self._file_lines = file_lines


        self.ast_lines = self._build_ast_lines(ast_list)
        self.symbol_holder = SymbolHolder(ast_list)
        self.term_holder = TermHolder(ast_list)

        
        self._section = self._init_sections(file_lines)

    def _init_sections(self,file_lines: List[str]):
        ret = []
        current_section = None
        section_tag = "@section:"
        for l in file_lines:
            if section_tag in l:
                start_index = l.index(section_tag) + len(section_tag)
                l = l[start_index:]
                current_section = l

            ret.append(current_section)
        return ret

    def get_section(self,obj):
        print(obj.location)
        line = obj.location.begin.line -1

        return self._section[line]


    def _build_ast_lines(self,ast_list: List[AST]):
        def deep_search_sym_dep(ast: AST, sym: Set, dep: Set, trace: List):
            new_trace = trace.copy()
            if isinstance(ast, ASTSequence):
                new_trace.append('ASTSequence')
                for _ast in ast:
                    deep_search_sym_dep(_ast, sym, dep, new_trace)
            else:
                new_trace.append(ast.ast_type)
                if ast.ast_type == ASTType.SymbolicAtom:
                    if 'head' in new_trace:
                        if 'head' in new_trace and ASTType.ConditionalLiteral in new_trace and 'condition' in new_trace:
                            dep.add(Symbol(ast))
                        else:
                            sym.add(Symbol(ast))
                    elif 'body':
                        dep.add(Symbol(ast))
                    else:
                        sym.add(Symbol(ast))
                else:
                    if ast.child_keys:
                        for child in ast.child_keys:
                            a = eval(f'ast.{child}')
                            if a:
                                new_trace.append(child)
                                deep_search_sym_dep(
                                    a, sym, dep, new_trace)
                                new_trace.remove(child)
                return (sym, dep)

        ast_lines = []
        for ast in ast_list:
            syms, dependencies = deep_search_sym_dep(ast, set(), set(), [])
            al = ASTLine.factory(ast,syms,dependencies)
            if al :
                ast_lines.append(al)
                comments = fetch_comments(al.ast,self._file_lines)
                al._comments = comments

        return ast_lines

    


class Symbol:
    def __init__(self, ast: SymbolicAtom) -> None:
        self.name = ast.symbol.name
        self.arguments = {ast.symbol.arguments}
        self.signature = f"{self.name}/{len(ast.symbol.arguments)}"
        self.location = {ast.symbol.location}
        self._occurs = 0


    def __repr__(self) -> str:
        return self.name

    def get_signature(self) -> str:
        return self.signature


class SymbolHolder:
    def __init__(self,ast_list) -> None:
        self._pool = {}
        self._find_symbols(ast_list)

    def add(self, sym: Symbol) -> None:
        if sym.get_signature() in self._pool:
            self._pool[sym.get_signature()].arguments.update(sym.arguments)
            self._pool[sym.get_signature()]._occurs += 1
        else:
            self._pool[sym.get_signature()] = sym

    def get(self, signature: str) -> Symbol | None:
        return self._pool.get(signature)


    def _find_symbols(self,ast_list: List[AST]):
        def deep_find_symbols(sh, ast: AST):
            if isinstance(ast, ASTSequence):
                for a in ast:
                    deep_find_symbols(sh,a)
            else:
                if ast.ast_type == ASTType.SymbolicAtom:
                    sh.add(Symbol(ast))
                else:
                    if ast.child_keys:
                        for key in ast.child_keys:
                            a = eval(f'ast.{key}')
                            if a: 
                                deep_find_symbols(sh,a)
        for ast in ast_list:
            deep_find_symbols(self,ast)

    def keys(self):
        return self._pool.keys()


class Term:
    def __init__(self, var: Variable) -> None:
        self.name = var.name
        self.location : Set[Location] = [var.location]

    def __repr__(self) -> str:
        return f"{self.name}:[L{self.location.begin.line} C{self.location.begin.column}]"



class TermHolder:
    def __init__(self,ast_list:List[AST]) -> None:
        self._pool = {}
        self._find_terms(ast_list)

    def add(self,term:Term) -> None:
        if term.name in self._pool:
            self._pool[term.name].location.append(term.location)
        else:
            self._pool[term.name] = term 

    def get(self,name:str) -> Term | None:
        return self._pool.get(name)

    def _find_terms(self, ast_list: List[AST]):
        def deep_find_terms(th, ast: AST | ASTSequence):
            if isinstance(ast, ASTSequence):
                for a in ast:
                    deep_find_terms(th, a)
            else:
                if ast.ast_type == ASTType.Variable:
                    th.add(Term(ast))
                else:
                    for keys in ast.child_keys:
                        a = eval(f'ast.{keys}')
                        if a:
                            deep_find_terms(th,a)

        for ast in ast_list:
            deep_find_terms(self, ast)

    def keys(self):
        return self._pool.keys()


class ASTLineType(Enum):
    Rule = 'Rule'
    Constraint = 'Constraint'
    Fact = 'Fact'

    Definition = 'Definition'
    Input = 'Input'
    Constant = 'Constant'
    Output = 'Output'


class ASTLine:
    def __init__(self, ast: AST, define: List[Symbol], dependencies: List[Symbol]) -> None:
        self._ast = ast
        self._define = define
        self._dependencies = dependencies
        self._comments = None
        self._location = ast.location
        self._location_link = self._to_github_link_location()

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
        return self._comments
    
    @property
    def location(self):
        return self._location

    def factory(ast: AST, define: List[Symbol], dependencies: List[Symbol]):
        if ast.ast_type == ASTType.Rule:
            if define and dependencies:
                return Rule(ast, define, dependencies)
            elif define and not dependencies:
                return Fact(ast, define, dependencies)
            elif not define and dependencies:
                return Constraint(ast, define, dependencies)
            else:
                print('Problem')
        else:
            if ast.ast_type == ASTType.Defined:
                return Input(ast, define, dependencies)
            elif ast.ast_type == ASTType.Definition:
                return Definition(ast, define, dependencies)
            elif ast.ast_type == ASTType.ShowSignature or ast.ast_type == ASTType.ShowTerm:
                return Output(ast, define, dependencies)
            else:
                print(ast, ast.ast_type)
                print('To be ignore or not implemented yet')

    def _to_github_link_location(self):
        return f'https://github.com/Owrel/clindoc/blob/master/{self.location.begin.filename}#L{self.location.begin.line}'


class Rule(ASTLine):
    def __init__(self, ast: AST, define: List[Symbol], dependencies: List[Symbol]) -> None:
        super().__init__(ast, define, dependencies)
        self._type = ASTLineType.Rule


class Constraint(ASTLine):
    id = 0

    def __init__(self, ast: AST, define: List[Symbol], dependencies: List[Symbol]) -> None:
        super().__init__(ast, define, dependencies)
        self._type = ASTLineType.Constraint
        self.id = Constraint.id
        Constraint.id += 1


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

    def get_output_signature(self):
        if self.ast.ast_type == ASTType.ShowTerm:
            return f"{self.ast.term.name}/{len(self.ast.term.arguments)}"
        else:
            return f"{self.ast.name}/{self.ast.arity}"


class Constant(ASTLine):
    def __init__(self, ast: AST, define: List[Symbol], dependencies: List[Symbol]) -> None:
        super().__init__(ast, define, dependencies)
        self._type = ASTLineType.Constant
