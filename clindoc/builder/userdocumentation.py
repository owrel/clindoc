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
        all_tag = {}
        for astprogram in self.builder.astprograms:
            all_tag.update(astprogram._tags)


        if all_tag.get('installation'):
            self.document.h2('Installation')
            self.document.newline()
            
            for tag in all_tag.get('installation'):
                self.document.content(tag.description)
                self.document.newline()

                self.document.directive('code-block',content=tag.parameters[0], arg = tag.parameters[1],indent =2)
                self.document.newline(3 )

        
        if all_tag.get('usage'):
            self.document.h2('Usage')
            self.document.newline()
            
            for tag in all_tag.get('usage'):
                self.document.content(tag.description)
                self.document.newline()
                self.document.directive('code-block',content=tag.parameters[0],arg = tag.parameters[1],indent=2)
                self.document.newline(3)

        

        if all_tag.get('example'):
            self.document.newline()

            self.document.h2('Example')
            self.document.newline()
            
            for tag in all_tag.get('example'):
                self.document.content(tag.description)
                self.document.newline()
                self.document.directive('code-block',content=tag.parameters[0],arg = tag.parameters[1],indent=2)

                self.document.newline(3)

        

        