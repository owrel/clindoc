from __future__ import annotations
from typing import List, Union
import re


class Directive:
    """
    Represents a directive found in a logic program file comment, used to add additional metadata to program used in the documentation.
    
    .. note:
        Directives are useful for adding additional metadata to a logic program file. They allow you to create a documentation that can be automatically used for documentation. However, the current implementation uses regular expressions to find directives and their parameters, which can be fragile and limited. In the future, using a more formal grammar-based approach would be more robust and powerful, allowing for more complex and expressive directives. For example, a grammar-based approach would allow the use of rst or markdown in the documentation, it would also make the expression of different directives more natural. 
    

    :param name: The name of the directive.
    :param parameters: A list of parameters passed to the directive.
    :param description: A description of the directive, if one was provided.
    :param line_number: The line number in the file where the directive was found.
    :param filename: The filename of the file where the directive was found.
    """

    DIRECTIVE_IDENTIFIER = "@"
    DESCRIPTION_IDENTIFIER = "->"

    def __init__(self,
                 name: str,
                 parameters: List[str],
                 description: Union[str, None],
                 line_number: int,
                 filename: str) -> None:

        self.name = name
        self.parameters = parameters
        self.description = description
        self.line_number = line_number
        self.filename = filename

    def __repr__(self) -> str:
        return self.name + '_' + self.parameters[0]

    @classmethod
    def from_line(cls,  line: str, line_number: int, filename: str):
        """
        Extracts a `Directive` object from a given line of text.

        :param line: The line of text to extract the directive from.
        :param line_number: The line number in the file where the directive was found.
        :param filename: The filename of the file where the directive was found.
        :return: A `Directive` object representing the directive found in the line, or None if no directive was found.
        """
        def _extract_parameters(s):
            result = []
            current_word = ""
            in_parentheses = False
            in_double_quote = False
            for c in s:
                if c == "(":
                    current_word += c
                    in_parentheses = True
                elif c == ")":
                    current_word += c
                    in_parentheses = False
                elif c == '"':
                    if in_double_quote:
                        in_double_quote = False
                    else:
                        in_double_quote = True

                elif c == "," and not in_parentheses:
                    result.append(current_word)
                    current_word = ""
                else:
                    current_word += c
            result.append(current_word)
            return result

        rgx = f" *{cls.DIRECTIVE_IDENTIFIER} *(?P<directive_name>[a-zA-Z]+) *\((?P<parameters>[^\-\>]*)\) *({cls.DESCRIPTION_IDENTIFIER} *(?P<description>[^\\n]*))?"
        match = re.search(rgx, line.strip())
        if not match:
            return

        parameters = _extract_parameters(match['parameters'])
        directive_name = match['directive_name'].strip()
        description = match['description']

        return cls(directive_name, parameters, description, line_number, filename)

    @classmethod
    def extract_directives(cls, file: List[str], filename: str) -> dict:
        """
        Extracts all of the directives from the file, returning a dictionary of lists of the extracted directives, with the keys being the names of the directives. If a directive with the same name and first parameter (correspond to an ID) already exists in the dictionary, the directive's description will be added to the existing directive if it is not already present.

        :return: A dictionary of lists of the extracted directives, with the keys being the names of the directives.
        """
        ret = {}
        for line_number, line in enumerate(file):
            directive = Directive.from_line(line, line_number, filename)
            if directive == None:
                continue

            if not directive.name in ret:
                ret[directive.name] = [directive]
            else:
                for t in ret[directive.name]:
                    if t.parameters[0] == directive.parameters[0]:
                        if not t.description and directive.description:
                            t.description = directive.description
                        break
                else:
                    ret[directive.name].append(directive)

        return ret