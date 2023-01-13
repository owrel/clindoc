from typing import List, Set, Tuple
from clingo.ast import AST, ASTSequence, ASTType, SymbolicAtom, Variable, Location
from enum import Enum
import re


def fetch_comments(ast: AST, file: List[str], identificator="%-") -> List[str]:
    lines = file.copy()
    lines = lines[:ast.location.begin.line]
    lines.reverse()
    comments = []
    found = False
    for idx, line in enumerate(lines):
        if not found:
            if identificator in line and not found:
                if idx == 0:
                    comments.append(
                        line[line.index(identificator)+len(identificator):].strip())
                    found = True
                if idx > 0 and line.strip()[:len(identificator)] == identificator:
                    comments.append(
                        line[line.index(identificator)+len(identificator):].strip())
                    found = True
                else:
                    break
            elif line.strip() and idx != 0:
                break

    comments.reverse()
    return comments


class Tag:
    def __init__(self, name: str, parameters: List[str], description: str | None, line_number: int, path: str) -> None:
        self.name = name
        self.parameters = parameters
        self.description = description
        self.line_number = line_number
        self.path = path


class ASTProgram:
    def __init__(self, ast_list: List[AST], file_lines: List[str], path: str) -> None:
        self._file_lines: List[str] = file_lines
        self._path = path
        self._tags = self.fetch_all_tag()
        self.ast_lines, self.external_ast_lines = self._build_ast_lines(ast_list)
        self.symbol_holder = SymbolHolder(ast_list,self._tags)
        self.term_holder = TermHolder(ast_list, self._tags)

    def _analyze_line(self, idx: int, line: str, path: str) -> Tag | None:
        def _extract_parameters(s):
            result = []
            current_word = ""
            in_parentheses = False
            in_double_quote = False
            for c in s:
                if c == "(":
                    in_parentheses = True
                elif c == ")":
                    in_parentheses = False
                elif c == '"':
                    if in_double_quote : in_double_quote= False
                    else : in_double_quote = True

                elif c == "," and not in_parentheses:
                    result.append(current_word)
                    current_word = ""
                else:
                    current_word += c
            result.append(current_word)
            return result

        tag_identifier = "@"
        description_identifier = "->"
        rgx = f" *{tag_identifier} *(?P<tag_name>[a-zA-Z]+) *\((?P<parameters>.*)\) *({description_identifier}(?P<description> *[^\\n]*))?"
        match = re.search(rgx, line.strip())

        if not match:
            return

        parameters = _extract_parameters(match['parameters'])
        tag_name = match['tag_name']
        description = match['description']

        return Tag(tag_name, parameters, description, idx, path)

    def fetch_all_tag(self) -> dict:
        ret = {}

        for idx, line in enumerate(self._file_lines):
            tag = self._analyze_line(idx, line, self._path)
            if not tag:
                continue

            if not tag.name in ret:
                ret[tag.name] = [tag]
            else:
                ret[tag.name].append(tag)

        return ret

    def get_section(self, obj) -> Tag|None:
        line = obj.location.begin.line - 1
        current_section = None
        if self._tags.get('section'):
            for section in sorted(self._tags['section'],key= lambda x : x.line_number):
                if section.line_number < line:
                    current_section = section
                else:
                    break
        return current_section

    def _build_ast_lines(self, ast_list: Tuple[List[AST],List[AST]]):
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
        external_ast_lines = []

        for ast in ast_list:
            syms, dependencies = deep_search_sym_dep(ast, set(), set(), [])
            al = ASTLine.factory(ast, syms, dependencies)
            if al:
                al._section = self.get_section(al)
                comments = fetch_comments(al.ast, self._file_lines)
                al._comments = comments
                
                if al.location.begin.filename == self._path:
                    ast_lines.append(al)
                else:
                    external_ast_lines.append(al)

        return ast_lines,external_ast_lines


class Symbol:
    def __init__(self, ast: SymbolicAtom, defined_predicate:List[Tag]|None = None) -> None:
        self.name = ast.symbol.name
        self.arguments = ast.symbol.arguments
        self.signature = f"{self.name}/{len(ast.symbol.arguments)}"
        self.location = ast.symbol.location
        self.tag = None
        self.definition = None
        if defined_predicate:
            for tag in defined_predicate:
                if tag.parameters[0] == self.name:
                    self.tag = tag
                    self.definition = tag.description
                    break

    def __repr__(self) -> str:
        return self.name

    def get_signature(self) -> str:
        return self.signature


class SymbolHolder:
    def __init__(self, ast_list,tags:dict) -> None:
        self._pool = {}
        self.tags = tags
        self._find_symbols(ast_list)

    def add(self, sym: Symbol) -> None:
        if sym.get_signature() in self._pool:
            self._pool[sym.get_signature()].append(sym)
        else:
            self._pool[sym.get_signature()] = [sym]

    def get(self, signature: str) -> List[Symbol] | None:
        return self._pool.get(signature)

    def _find_symbols(self, ast_list: List[AST]):
        def deep_find_symbols(sh, ast: AST):
            if isinstance(ast, ASTSequence):
                for a in ast:
                    deep_find_symbols(sh, a)
            else:
                if ast.ast_type == ASTType.SymbolicAtom:
                    sh.add(Symbol(ast,self.tags.get('predicate')))
                else:
                    if ast.child_keys:
                        for key in ast.child_keys:
                            a = eval(f'ast.{key}')
                            if a:
                                deep_find_symbols(sh, a)
        for ast in ast_list:
            if ast.location.begin.filename == ast_list[0].location.begin.filename:
                deep_find_symbols(self, ast)

    def keys(self):
        return self._pool.keys()


class Term:
    def __init__(self, var: Variable, defined_terms: List[Tag] | None = None) -> None:
        self.name = var.name
        self.location: Set[Location] = [var.location]
        self.tag = None
        self.definition = None
        if defined_terms:
            for tag in defined_terms:
                if tag.parameters[0] == self.name:
                    self.tag = tag
                    self.definition = tag.description
                    break


class TermHolder:
    def __init__(self, ast_list: List[AST], tags:dict) -> None:
        self._pool = {}
        self.tags = tags
        self._find_terms(ast_list)

    def add(self, term: Term) -> None:
        if term.name in self._pool:
            self._pool[term.name].append(term)
        else:
            self._pool[term.name] = [term]

    def get(self, name: str) -> Term | None:
        return self._pool.get(name)

    def _find_terms(self, ast_list: List[AST]):
        def deep_find_terms(th, ast: AST | ASTSequence):
            if isinstance(ast, ASTSequence):
                for a in ast:
                    deep_find_terms(th, a)
            else:
                if ast.ast_type == ASTType.Variable:
                    th.add(Term(ast,self.tags.get('term')))
                else:
                    for keys in ast.child_keys:
                        a = eval(f'ast.{keys}')
                        if a:
                            deep_find_terms(th, a)

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
        self._section = None

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

    @property
    def section(self):
        return self._section

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
