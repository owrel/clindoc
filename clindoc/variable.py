from __future__ import annotations
from clingo.ast import Location, AST, ASTSequence, ASTType
from typing import List

from .directive import Directive


class Variable:
    """
    Represents a variable found in a logic program, along with any associated metadata from directives found in the program's comments.

    :param var: The clingo.ast.Variable object this class wraps.
    :param directive: A Directive object associated with this variable, if one is present.
    """

    def __init__(self, var: ASTType.Variable, directive: Directive | None):

        self.name: str = var.name
        self.location: Location = var.location
        self.directive = directive
        self.description = None
        if directive:
            self.definition = directive.description
            
        self.ast = var
        
    def __repr__(self) -> str:
        return f"{self.name}"

    @classmethod
    def extract_variables(cls,
                        ast_list: List[AST],
                        predicate_directives=List[Directive],
                        current_file_path=str,
                        ) -> List[Variable]:
    
        """
        Extracts all variables found in the given list of AST nodes and returns them as a list of Variable objects.
        Each variable will be associated with any directive metadata found in the program's comments, if any.
        
        :param ast_list: A list of AST nodes representing the logic program.
        :param predicate_directives: A list of Directive objects representing the predicate directives found in the program's comments.
        :param current_file: The path of the current file.
        :return: A list of Variable objects representing the variables found in the given list of AST nodes.
        """
        def rec_extraction(pool: List, ast: AST, var_directives: List[Directive]):
            if isinstance(ast, ASTSequence):
                for a in ast:
                    rec_extraction(pool, a, var_directives)
            else:
                if ast.ast_type == ASTType.Variable:
                    if var_directives:
                        for directive in var_directives:
                            if directive.parameters[0] == ast.name:
                                pool.append(cls(ast, directive))
                                break
                        else:
                            pool.append(cls(ast, None))
                    else:
                        pool.append(cls(ast, None))
                else:
                    if ast.child_keys:
                        for key in ast.child_keys:
                            ast_child = eval(f'ast.{key}')
                            if ast_child:
                                rec_extraction(pool, ast_child, var_directives)

        pool = []
        for ast in ast_list:
            if ast.location.begin.filename == current_file_path:
                rec_extraction(pool, ast, predicate_directives)

        return pool
