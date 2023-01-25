from .component import Component

from argparse import ArgumentParser

class UserDocumentation(Component):
    parse_group_description = 'User Documentation parameters'
    name = 'userdoc'

    @classmethod
    def cmdline_documentation(cls, parser: ArgumentParser):
        parser_group = super().cmdline_documentation(parser)


    def __init__(self, builder, parameters) -> None:
        super().__init__(builder, parameters)
    
    def check_parameters(self):
        super().check_parameters()
    
    
    def build_rst_file(self):
        self.document.title("User Documentation")
        self.document.newline()
        self.document.content("*Using the encoding*")
        self.document.newline()
        self.document.table_of_contents('Contents', depth=2)
        self.document.newline()
        self._build_usage()

    def _build_usage(self):
        directives= {}
        for east in self.builder.easts:
            directives.update(east.directives)


        if directives.get('installation'):
            self.document.h2('Installation')
            self.document.newline()
            
            for directive in directives.get('installation'):
                self.document.content(directive.description)
                self.document.newline()

                self.document.directive('code-block',content=directive.parameters[0], arg = directive.parameters[1],indent =2)
                self.document.newline(3 )

        
        if directives.get('usage'):
            self.document.h2('Usage')
            self.document.newline()
            
            for directive in directives.get('usage'):
                self.document.content(directive.description)
                self.document.newline()
                self.document.directive('code-block',content=directive.parameters[0],arg = directive.parameters[1],indent=2)
                self.document.newline(3)

        

        if directives.get('example'):
            self.document.newline()

            self.document.h2('Example')
            self.document.newline()
            
            for directive in directives.get('example'):
                self.document.content(directive.description)
                self.document.newline()
                self.document.directive('code-block',content=directive.parameters[0],arg = directive.parameters[1],indent=2)

                self.document.newline(3)

        

        