from __future__ import annotations
from clingo.ast import SymbolicAtom, AST, ASTSequence, ASTType
from typing import List

from .directive import Directive


class Symbol:
    """
    Represents a symbol in a logic program, along with any associated directive metadata found in the program's comment.
    Note that the Symbol class is not intended to be instantiated directly by user code. 
    But rather is used internally by the EnrichedAST class to represent symbols with their associated metadata.

    :param ast: The clingo AST node representing the symbol.
    :param directive: The directive associated with the symbol, if any.
    """

    def __init__(self, ast: SymbolicAtom, directive: Directive | None) -> None:
        self.name = ast.symbol.name
        self.arguments = ast.symbol.arguments
        self.signature = f"{self.name}/{len(ast.symbol.arguments)}"
        self.location = ast.symbol.location
        self.directive = directive
        self.definition = None
        self.ast = ast
        if directive:
            self.definition = directive.description

    def __repr__(self) -> str:
        return f"{self.prefix}{self.signature}"
    
    @classmethod
    def extract_symbols(cls,
                        ast_list: List[AST],
                        predicate_directives=List[Directive],
                        current_file_path=str,
                        ) -> List[Symbol]:
        """
        Extracts all symbols found in the given list of AST nodes and returns them as a list of Symbol objects.
        Each symbol will be associated with any directive metadata found in the program's comments, if any.
        
        :param ast_list: A list of AST nodes representing the logic program.
        :param predicate_directives: A list of Directive objects representing the predicate directives found in the program's comments.
        :param current_file: The path of the current file.
        :return: A list of Symbol objects representing the symbols found in the given list of AST nodes.
        """
        def rec_extraction(pool: List, ast: AST, predicate_directives: List[Directive] | None):
            if isinstance(ast, ASTSequence):
                for a in ast:
                    rec_extraction(pool, a, predicate_directives)
            else:
                if ast.ast_type == ASTType.SymbolicAtom:
                    if predicate_directives:
                        for directive in predicate_directives:
                            if directive.parameters[0] == ast.symbol.name:
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
                                rec_extraction(pool, ast_child, predicate_directives)

        pool = []
        # print(ast_list)
        for ast in ast_list:
            if ast.location.begin.filename == current_file_path:
                rec_extraction(pool, ast, predicate_directives)

        return pool