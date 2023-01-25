from ..east import EnrichedAST
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

    def __init__(self, easts: List[EnrichedAST],
                 parameters: Dict) -> None:

        self.parameters = parameters
        self.easts = easts
        self.components = self._initialize_component()
        self.all_directives = self.unit_directives()
        
    def unit_directives(self)->dict:
        all_directives = {}
        for east in self.easts:
            for key in east.directives:
                if key in all_directives:
                    all_directives[key] += east.directives[key]
                else:
                    all_directives[key] = east.directives[key]
        return all_directives
    

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
                c.build_rst_file()
                c.write_rst_file()


