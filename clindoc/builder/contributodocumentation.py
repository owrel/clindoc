
from .component import Component
from ..east import  ASTLine

from argparse import ArgumentParser


class ContributorDocumentation(Component):
    parse_group_description = 'Contributor Documentation parameters'
    name = 'contributordoc'

    @classmethod
    def cmdline_documentation(cls, parser: ArgumentParser):
        parser_group = super().cmdline_documentation(parser)

        parser_group.add_argument(
            f'--{cls.name}.group-by',
            action="store",
            default="section",
            help='How the contributor documentation will group the different elements. "section" or "type"'
        )

        parser_group.add_argument(
            f'--{cls.name}.hide-uncommented',
            action="store_true",
            help='(flag) hide non-commented or non-defined variable, rules...'
        )

        parser_group.add_argument(
            f'--{cls.name}.hide-code',
            action="store_true",
            help='(flag) hide source code'
        )


    def __init__(self, builder, parameters) -> None:
        super().__init__(builder, parameters)

    def _include_code(self, astline: ASTLine):
        if not self.parameters[self.name]['hide_code']:
            return super()._include_code(astline)
        
    def check_parameters(self):
        super().check_parameters()
        if not 'group_by' in  self.parameters[self.name]:
            self.parameters[self.name]['group_by'] = 'section'

        if not 'hide_uncommented' in self.parameters[self.name]:
            self.parameters[self.name]['hide_uncommented'] = False
        
        if not 'hide_code' in self.parameters[self.name]:
            self.parameters[self.name]['hide_code'] = False

    def _factory(self, astline: ASTLine):
        if self.parameters[self.name]['hide_uncommented'] and not astline.comments:
            return False

        self.document.h4(f"{self._get_name(astline)}")
        self.document.newline()

        if 'predicate' in self.builder.all_directives:
            for directive in self.builder.all_directives['predicate']:

                if directive.parameters[0] == astline.identifier:
                    self.document.content(f'{directive.parameters[1]} -> {directive.description}')
                    self.document.newline()
        
        
        if astline.dependencies:
            self.document.h5(f"Dependencies:")
            d_done = []
            for d in astline.dependencies:
                if d.signature not in d_done:
                    self.document.li(d.signature)
                    d_done.append(d.signature)
            self.document.newline()
        
        self.document.content(
            f"Location: Line {self._get_location(astline)}")
        self.document.newline()
        self._include_code(astline)
        self._include_comments(astline)
        self.document.newline()
        return True
        
        

    def _build_variable_table(self):
        self.document.h2('Variables')
        self.document.newline()
        terms = self.builder.all_directives.get('term')
        data = []
        if terms:
            for term in terms:
                data.append([term.parameters[0],term.description])

        self.document.table(['Variable', 'Definition'], data=data)
        self.document.newline()

    def build_rst_file(self):

        self.document.title("Contributor Documentation")
        self.document.newline()
        self.document.content("*Understand the encoding*")
        self.document.newline()
        self.document.table_of_contents('Contents', depth=3)
        self.document.newline()
        self._build_variable_table()
        self.document.h2(f'Encoding decomposition')

        if self.parameters[self.name]['group_by'] == "type":
            self.document.content("*Ordered by type*")
            self.document.newline()
            types = {}
            for east in self.builder.easts:
                for astline in east.ast_lines:
                        if astline.type not in types:
                            types[astline.type] = [astline]
                        else:
                            types[astline.type].append(astline)
                            
            for t in types:
                self.document.h3(f'Type: {t}')
                self.document.newline()
                for astline in types[t]:
                    self._factory(astline)
            
        elif self.parameters[self.name]['group_by'] == "section":
            self.document.content("*Ordered by section*")
            self.document.newline()

            sections = {}
            no_section = []
            for east in self.builder.easts:
                for astline in east.ast_lines:
                    if astline.section != None:
                        for key in sections:
                            if key.parameters[0] == astline.section.parameters[0]:
                                sections[key] .append(astline)
                                break
                        else:
                            sections[astline.section] = [astline]
                    else:
                        no_section.append(astline)

            if not sections:
                print('Warning: No section detected and using group by "section"')

            for section in sections:
                self.document.h3(f'Section: {section.parameters[0]}')
                self.document.newline()
                if section.description:

                    self.document.content(section.description)
                    self.document.newline()
                for astline in sections[section]:
                    self._factory(astline)

            if no_section:
                self.document.h1('No section')
                self.document.newline()
                for astline in no_section:
                    self._factory(astline)

        else:
            raise ValueError(f"invalid groupby value: {self.groupby}")
