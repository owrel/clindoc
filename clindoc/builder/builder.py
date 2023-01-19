from ..astprogram import ASTProgram
from .component import Component, Index, Source
from .contributodocumentation import ContributorDocumentation
from .graphs import DependencyGraph
from .userdocumentation import UserDocumentation
from typing import List, Dict
import traceback


class Builder:
    cls_components: List[Component] = [
        Index,
        UserDocumentation,
        ContributorDocumentation,
        DependencyGraph,
        Source
    ]

    def __init__(self, astprograms: List[ASTProgram],
                 parameters: Dict) -> None:

        self.parameters = parameters
        self.astprograms = astprograms
        self.components = self._initialize_component()
        self.all_tags = self._unit_tags()
        
    def _unit_tags(self)->dict:
        all_tags = {}
        for astprogram in self.astprograms:
            for key in astprogram._tags:
                if key in all_tags:
                    all_tags[key] += astprogram._tags[key]
                else:
                    all_tags[key] = astprogram._tags[key]
        return all_tags
    

    def _initialize_component(self) -> List[Component]:
        component_list = []
        for cls_component in Builder.cls_components:
            component = cls_component(self, self.parameters)
            component_list.append(component)
            print(f'Components {component.name} loaded')
        return component_list

    def build(self):
        for c in self.components:
            build = True
            if (c.name != 'index') and self.parameters[c.name]['exclude']:
                build = False

            if build:
                # try:
                    c.build_rst_file()
                    c.write_rst_file()
                # except Exception as e:
                #     print(f'Woops, something went wrong while building rst files from component {c.name}')
                #     print(f'Error: {e}')
                #     print(f'Trace: {e.with_traceback()}')

