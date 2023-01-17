from abc import ABC, abstractmethod
from ..astprogram import ASTLineType, ASTLine, ASTProgram
from typing import List, Tuple
from argparse import ArgumentParser
from rstcloth import RstCloth
import os
from io import StringIO


class Component(ABC):
    parse_group_description = "DEFAULT PARSER GROUP DESCRIPTION"
    name = "DEFAULT_NAME"

    @classmethod
    def cmdline_documentation(cls, parser: ArgumentParser) -> ArgumentParser:
        parser_group = parser.add_argument_group(
            cls.parse_group_description
        )

        parser_group.add_argument(
            f'--{cls.name}.exclude',
            action="store_true",
            help='(flag) component will be excluded from the documentation'
        )        
        return parser_group


    def __init__(self, builder, parameters) -> None:
        self.builder = builder
        self._sio = StringIO()
        self.document = RstCloth(self._sio)
        self.parameters = parameters


    @abstractmethod
    def build_rst_file(self) -> None:
        pass

    def write_rst_file(self):
        if self._sio.getvalue():  # Things have been written
            with open(os.path.join(self.parameters['doc_dir'], self.name + ".rst"), 'w') as file:
                file.write(self._sio.getvalue())

    def _get_name(self, astline: ASTLine):
        prefix = ""
        name = ""
        if len(self.builder.astprograms) > 1:
            prefix = astline.location.begin.filename.replace(
                self.parameters['src_dir'], "")[1:]

            prefix = prefix.replace('/', '.')
            prefix = prefix.replace('.lp', "")
            prefix += '.'

        if astline.type == ASTLineType.Fact:
            name = str(list(astline.define)[0].get_signature())
        elif astline.type == ASTLineType.Rule:
            name = str(list(astline.define)[0].get_signature())
        elif astline.type == ASTLineType.Constraint:
            name = f"Constraint#{astline.id}"
        elif astline.type == ASTLineType.Definition:
            name = f"{astline.ast.name}"
        elif astline.type == ASTLineType.Input:
            name = f"{astline.ast.name}/{astline.ast.arity}"
        elif astline.type == ASTLineType.Output:
            if  'term' in astline.ast.keys():
                name = f"Output: {astline.ast.term}"
            else:
                name = f"Output: {astline.ast.name}"
        else:

            if 'name' in astline.ast.keys():
                name = astline.ast.name
        
        return prefix + name

    def _get_location(self, astline: ASTLine):
        if astline.location.begin.line != astline.location.end.line:
            return f"{astline.location.begin.line}-{astline.location.end.line}"
        else:
            return f"{astline.location.begin.line}"

    def _include_code(self, astline: ASTLine):
        self.document._add(
            f".. literalinclude:: /{astline.location.begin.filename}")
        self.document._add(f" :language: prolog")
        self.document._add(f" :lines: {self._get_location(astline)}")

    def _include_comments(self, astline: ASTLine):
        if astline.comments:
            self.document.content(f"Comment", indent=1)
            for comment in astline.comments:
                self.document.content(f"↳ {comment}", indent=2)

    def _include_source(self, astprogram: ASTProgram):
        self.document._add(
            f".. literalinclude:: /{astprogram._path}")
        self.document._add(f" :language: prolog")
        self.document._add(f" :linenos:")


class Index(Component):
    name = 'index'

    @classmethod
    def cmdline_documentation(cls, parser: ArgumentParser) -> ArgumentParser:
        return 


    def __init__(self, builder, parameters) -> None:
        super().__init__(builder, parameters)

    def _generate_toctree(self):
        self.document._add('.. toctree::')
        self.document._add(' :maxdepth: 2')
        self.document.newline()

        for c in self.builder.components:
            if c.name != self.name:
                self.document._add(" " + c.name)

    def build_rst_file(self) -> None:
        self.document.title(self.parameters['project_name'])
        self.document.newline()
        self.document.content(self.parameters['description'])
        self.document.newline(3)
        self.document.h1("Content")
        self.document.newline()
        self._generate_toctree()



class Source(Component):
    name = "source"
    parse_group_description = "Source files parameters"
    
    @classmethod
    def cmdline_documentation(cls, parser: ArgumentParser) -> ArgumentParser:
        parser_group = super().cmdline_documentation(parser)
        parser_group.add_argument(
            f'--{cls.name}.exclude-file',
            action="store",
            nargs= '*',
            help='source file(s) that will be excluded from source documentation section'
        )   

    def __init__(self, builder, parameters) -> None:
        super().__init__(builder, parameters)
        if not 'exclude_file' in self.parameters[self.name]:
            self.parameters[self.name]['exclude_file']


    def build_rst_file(self) -> None:
        self.document.title('Source Code')
        self.document.newline()

        for astprogram in self.builder.astprograms:
            self.document.h2(
                astprogram._path[self.parameters['src_dir'].rindex('/')+1:])
            self.document.newline()
            self._include_source(astprogram)
            self.document.newline()
