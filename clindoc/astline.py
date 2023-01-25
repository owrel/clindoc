from enum import Enum

from clingo.ast import AST, ASTType
from typing import List

from .symbol import Symbol


class ASTLineType(Enum):
    """
    Enumeration of the possible types of an ASTLine.
    """
    Rule = 'Rule'
    Constraint = 'Constraint'
    Fact = 'Fact'
    Definition = 'Definition'
    Input = 'Input'
    Constant = 'Constant'
    Output = 'Output'


class ASTLine:
    """
    Represents a line of the logic program, encapsulating the corresponding clingo AST node and the symbols defined or used on that line.
    :param ast: The clingo AST node corresponding to the line.
    :param define: The list of symbols defined on this line.
    :param dependencies: The list of symbols used on this line.
    """
    def __init__(self, ast: AST, define: List[Symbol], dependencies: List[Symbol]) -> None:
        self.ast = ast
        self.define = define
        self.dependencies = dependencies
        self.comments = None
        self.location = ast.location
        self.section = None
        self._identifier = None
        self.prefix = ""

    @property
    def identifier(self):
        return self._identifier

    def factory(ast: AST, 
                define: List[Symbol], 
                dependencies: List[Symbol], 
                section=None,
                comments=None,
                src_dir=None):
        """
        A factory method used to create the appropriate subclass of ASTLine based on the type of the provided AST node.
        :param ast: The clingo AST node representing the logic statement.
        :param define: A list of Symbol objects representing the defined symbols in the logic statement.
        :param dependencies: A list of Symbol objects representing the dependencies in the logic statement.
        :return: An instance of the appropriate ASTLine subclass (e.g. Rule, Constraint, Fact, Definition, Input, or Output)
        """
        
        ret = None
        if ast.ast_type == ASTType.Rule:
            if define and dependencies:
                ret =  Rule(ast, define, dependencies)
            elif define and not dependencies:
                ret = Fact(ast, define, dependencies)
            elif not define and dependencies:
                ret = Constraint(ast, define, dependencies)
            else:
                print('Problem')
        else:
            if ast.ast_type == ASTType.Defined:
                ret= Input(ast, define, dependencies)
            elif ast.ast_type == ASTType.Definition:
                ret =  Definition(ast, define, dependencies)
            elif ast.ast_type == ASTType.ShowSignature or ast.ast_type == ASTType.ShowTerm:
                ret = Output(ast, define, dependencies)
            else:
                print(ast, ast.ast_type)
                print('To be ignore or not implemented yet')
        if ret:
            ret.section = section
            ret.comments = comments
            prefix = ret.location.begin.filename.replace(
                src_dir, "")[1:]
            prefix = prefix.replace('/', '.')
            prefix = prefix.replace('.lp', "")
            prefix += '.'
            ret.prefix = prefix
        
        return ret
                
        


class Rule(ASTLine):
    def __init__(self, ast: AST, define: List[Symbol], dependencies: List[Symbol]) -> None:
        super().__init__(ast, define, dependencies)
        self.type = ASTLineType.Rule
        self._identifier = str(list(self.define)[0].signature)


class Constraint(ASTLine):
    id = 0

    def __init__(self, ast: AST, define: List[Symbol], dependencies: List[Symbol]) -> None:
        super().__init__(ast, define, dependencies)
        self.type = ASTLineType.Constraint
        self.id = Constraint.id
        Constraint.id += 1
        self._identifier = f"Constraint#{self.id}"


class Fact(ASTLine):
    def __init__(self, ast: AST, define: List[Symbol], dependencies: List[Symbol]) -> None:
        super().__init__(ast, define, dependencies)
        self.type = ASTLineType.Fact
        self._identifier = str(list(self.define)[0].signature)


class Definition(ASTLine):
    def __init__(self, ast: AST, define: List[Symbol], dependencies: List[Symbol]) -> None:
        super().__init__(ast, define, dependencies)
        self.type = ASTLineType.Definition
        self._identifier = f"{self.ast.name}"


class Input(ASTLine):
    def __init__(self, ast: AST, define: List[Symbol], dependencies: List[Symbol]) -> None:
        super().__init__(ast, define, dependencies)
        self.type = ASTLineType.Input
        self._identifier = f"{self.ast.name}/{self.ast.arity}"


class Output(ASTLine):
    def __init__(self, ast: AST, define: List[Symbol], dependencies: List[Symbol]) -> None:
        super().__init__(ast, define, dependencies)
        self.type = ASTLineType.Output
        if 'term' in self.ast.keys():
            self._identifier = f"{self.ast.term.name}/{len(self.ast.term.arguments)}"
        else:
            self._identifier = f"{self.ast.name}/{len(self.ast.arguments)}"


class Constant(ASTLine):
    def __init__(self, ast: AST, define: List[Symbol], dependencies: List[Symbol]) -> None:
        super().__init__(ast, define, dependencies)
        self.type = ASTLineType.Constant
        self._identifier = self.ast.name
