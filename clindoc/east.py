from __future__ import annotations
from typing import List, Dict, Tuple, Set
from clingo.ast import AST, ASTSequence, ASTType, Location, Position

# Local import
from .directive import Directive
from .symbol import Symbol
from .variable import Variable
from .astline import ASTLine
from .comment import Comment


class EnrichedAST:
    """
    The EnrichedAST (east) class provides additional information and functionality for analyzing and working with an Abstract Syntax Tree (AST) generated from a logic program. 
    This class takes as input a list of AST objects, the lines of the source file as a list of strings, the filename to the source file, and some parameters to configure it.
    
    :param ast_list: AST of the encoding as a list
    :param file: str list representing the file
    :param filename: location of the file
    :param parameters: documentation parameters 
    """

    COMMENT_IDENTIFIER = "%-"

    def __init__(self,
                 ast_list: List[AST],
                 file: List[str],
                 filename: str,
                 parameters: Dict,
                 ) -> None:

        self.file = file
        self.filename = filename
        self.parameters = parameters
        
        self.directives = Directive.extract_directives(
            self.file, self.filename)
        
        self.comments = Comment.extract_comments(file,filename)

        self.symbols = Symbol.extract_symbols(
            ast_list, self.directives.get('predicates'), filename)
        
        self.variables = Variable.extract_variables(
            ast_list, self.directives.get('var'), filename)
        
        self.ast_lines, self.external_ast_lines = self.build_ast_lines(
            ast_list)

        

    # @classmethod
    # def get_comments(cls, ast: AST, file: List[str]) -> List[str]:
    #     """
    #     Fetches all comments that appear before the given AST node in the file.
    #     The comments are returned as a list of strings, in the order they appear in the file.

    #     :param ast: The AST node for which to fetch comments.
    #     :param file: A list of strings representing the lines of the logic program file.
    #     :return: A list of comments strings.
    #     """
    #     lines = file.copy()
    #     lines = lines[:ast.location.begin.line]
    #     lines.reverse()
    #     comments = []
    #     found = False
    #     for idx, line in enumerate(lines):
    #         if not found:
    #             if cls.COMMENT_IDENTIFIER in line and not found:
    #                 if idx == 0:
    #                     comments.append(
    #                         line[line.index(cls.COMMENT_IDENTIFIER)+len(cls.COMMENT_IDENTIFIER):].strip())
    #                     found = True
    #                 if idx > 0 and line.strip()[:len(cls.COMMENT_IDENTIFIER)] == cls.COMMENT_IDENTIFIER:
    #                     comments.append(
    #                         line[line.index(cls.COMMENT_IDENTIFIER)+len(cls.COMMENT_IDENTIFIER):].strip())
    #                     found = True
    #                 else:
    #                     break
    #             elif line.strip() and idx != 0:
    #                 break

    #     comments.reverse()
    #     return comments
    
    def get_line(self,line:int):
        """
        Given a line number, returns every element at this line position
        
        :param line: line number where the elements needs to be retrieve
        :return: A list of element
        """
        ret = []
        all_elem = []
        all_elem.extend(self.directives)
        all_elem.extend(self.comments)
        all_elem.extend(self.variables)
        all_elem.extend(self.ast_lines)
        
        for elem in all_elem:
            if elem.location.begin.line == line or elem.location.begin.line-1 == line :
                ret.append(ret)
                
        return ret
    
    

    def get_comments(self, ast: AST) -> List[Comment]:
        """
        Return a list of comments associated to the 

        :param ast: The AST node for which to fetch comments.
        :param file: A list of strings representing the lines of the logic program file.
        :return: A list of comments.
        """
        ret = []
        line_number = ast.location.begin.line
        for comment in self.comments:
            if line_number == comment.location.begin.line:
                ret.append(comment)
                        
        return ret
                        
            
            
        
        


    def get_section(self, obj) -> Directive | None:
        """
        Given an object with a location attribute, returns the section directive that the object belongs to. 
        If no associated section directive is found, returns None.
        
        :param obj: An object with a location attribute, such as an AST node or a Symbol.
        :return: The section Directive that the object belongs to, or None if no associated section directive is found.
        """
        line = obj.location.begin.line - 1
        current_section = None
        if self.directives.get('section'):
            for section in sorted(self.directives['section'], key=lambda directive: directive.line_number):
                if section.line_number < line:
                    current_section = section
                else:
                    break
        return current_section

    def get_symbol(self, ast: ASTType.SymbolicAtom):
        """
        Given an AST symbolic atom, returns the Symbol object already computed that corresponds to it.
        
        :param ast: The AST symbolic atom to find the corresponding Symbol for.
        :return: The Symbol object corresponding to the given AST symbolic atom, or None if no such symbol is found.
        """
        for symbol in self.symbols:
            if ast.symbol.name == symbol.name and ast.symbol.location == symbol.location:
                return symbol

        return Symbol(ast,None)

    def build_ast_lines(self, ast_list: Tuple[List[AST], List[AST]]):
        """
        Builds the final AST lines, by extracting the symbols and dependencies from the given list of AST elements. 
        This method will also filter the lines based on their file origin, and return the internal and external (coming from an #include statement) lines separately.
        
        :param ast_list: A tuple of lists containing the internal and external AST elements.
        :return: A tuple of lists containing the internal and external AST lines.
        """
        self.ast_lines = None
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
                            dep.add(self.get_symbol(ast))
                        else:
                            sym.add(self.get_symbol(ast))
                    elif 'body':
                        dep.add(self.get_symbol(ast))
                    else:
                        sym.add(self.get_symbol(ast))
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
            al = ASTLine.factory(ast, syms, dependencies,
                                 section=self.get_section(ast),
                                 comments=self.get_comments(ast),
                                 src_dir=self.parameters['src_dir'])
            
            if al:
                if al.location.begin.filename == self.filename:
                    ast_lines.append(al)
                else:
                    external_ast_lines.append(al)

        return ast_lines, external_ast_lines
