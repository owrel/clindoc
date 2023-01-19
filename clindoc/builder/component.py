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
        self.check_parameters()
    
    
    def check_parameters(self):
        if not self.name in self.parameters: 
            self.parameters[self.name] = {}
            
        if not 'exclude' in self.parameters[self.name]:
            self.parameters[self.name]['exclude'] = False
            


    @abstractmethod
    def build_rst_file(self) -> None:
        pass

    def write_rst_file(self):
        if self._sio.getvalue():  # Things have been written
            with open(os.path.join(self.parameters['doc_dir'], self.name + ".rst"), 'w') as file:
                file.write(self._sio.getvalue())

    def _get_name(self, astline: ASTLine):
        if len(self.builder.astprograms) > 1:
            return astline.prefix + astline.identifier
        
        return astline.identifier

    def _get_location(self, astline: ASTLine):
        if astline.location.begin.line != astline.location.end.line:
            return f"{astline.location.begin.line}-{astline.location.end.line}"
        else:
            return f"{astline.location.begin.line}"

    def _include_code(self, astline: ASTLine):
        
        self.document.directive('literalinclude', 
                                arg=f'/{astline.location.begin.filename}',
                                fields=[('language','prolog'),
                                        ('lines' , f'{self._get_location(astline)}')])
        
        self.document.newline()

    def _include_comments(self, astline: ASTLine):
        if astline.comments:
            for comment in astline.comments:
                self.document.directive('note',content=f"↳ {comment}")
            
            self.document.newline()

    def _include_source(self, astprogram: ASTProgram):
        
        
        self.document.directive('literalinclude', 
                                arg=f'/{astprogram._path}',
                                fields=[('language','prolog'),
                                        ('linenos' , '')])
        self.document.newline()

        



class Index(Component):
    name = 'index'

    @classmethod
    def cmdline_documentation(cls, parser: ArgumentParser) -> ArgumentParser:
        return 


    def __init__(self, builder, parameters) -> None:
        super().__init__(builder, parameters)


    def check_parameters(self):
        super().check_parameters()

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
        
    def check_parameters(self):
        super().check_parameters()
        if not 'exclude_file' in self.parameters[self.name]:
            self.parameters[self.name]['exclude_file']= False


    def build_rst_file(self) -> None:
        self.document.title('Source Code')
        self.document.newline()

        for astprogram in self.builder.astprograms:
            self.document.h2(
                astprogram._path[self.parameters['src_dir'].rindex('/')+1:])
            self.document.newline()
            self._include_source(astprogram)
            self.document.newline()
