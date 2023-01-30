from typing import Dict
import graphviz
import os

from ..astline import ASTLineType
from .component import Component, ArgumentParser
from ..utils import create_dir, filename_from_source



class DependencyGraph(Component):
    name = "dependencygraph"
    parse_group_description = "Dependency graph parameters"

    @classmethod
    def cmdline_documentation(cls, parser: ArgumentParser) -> ArgumentParser:
        group = super().cmdline_documentation(parser)

        group.add_argument('--dependencygraph.format', action='store', default="svg", help="Format of the graphs ")



    def __init__(self, builder,parameters:Dict) -> None:
        super().__init__(builder,parameters)
        
        
    def check_parameters(self):
        super().check_parameters()
        if not 'format' in self.parameters[self.name]:
            self.parameters[self.name]['format'] = 'svg'


    def build_rst_file(self) -> None:
        # Create folder for graphs
        create_dir(os.path.join(self.parameters['doc_dir'], "img"))

        self._build_rule_dependency_graph()
        self._build_definition_dependency_graph()

        self.document.title('Dependency Graphs')
        self.document.newline()
        for east in self.builder.easts:
            self.document.newline()
            self.document.h2(filename_from_source(
                self.parameters['src_dir'], east.filename).replace('.lp', ''))
            self.document.newline()
            self.document.directive('image', '/' + os.path.join( self.parameters['doc_dir'],"img",
                                    filename_from_source(self.parameters['src_dir'], east.filename).replace('.lp', ''), "rdg."+ self.parameters[self.name]['format']).strip())
            self.document.newline()

            self.document.directive('image', '/'+ os.path.join( self.parameters['doc_dir'],"img",
                                    filename_from_source(self.parameters['src_dir'], east.filename).replace('.lp', ''), "ddg."+ self.parameters[self.name]['format']).strip())
            self.document.newline()


    def _build_rule_dependency_graph(self):
        for east in self.builder.easts:
            g = graphviz.Digraph('G', format=self.parameters[self.name]['format'])
            pool = []
            for a in east.ast_lines + east.external_ast_lines:
                if a.type == ASTLineType.Rule or a.type == ASTLineType.Constraint or a.type == ASTLineType.Fact:
                    pool.append(a)

            edges = set()   
            for a in pool:
                for b in pool:
                    if a != b:
                        for define in a.define:
                            for depends in b.dependencies:
                                if define.signature == depends.signature:
                                    edges.add((self._get_name(
                                        a) + '; l' + self._get_location(a), self._get_name(b) + '; l' + self._get_location(b)))


            g.edges(edges)
            g.attr(label='Rule Dependency Graph')
            g.attr(fontsize='20')
            g.render(filename=os.path.join(self.parameters['doc_dir'], "img", filename_from_source(
                self.parameters['src_dir'], east.filename).replace('.lp', ''), "rdg"), view=False)

    
    def _build_definition_dependency_graph(self):
        for east in self.builder.easts:
            g = graphviz.Digraph('G',format=self.parameters[self.name]['format'])
            edges =set()
            for al in east.ast_lines + east.external_ast_lines:
                if al.type == ASTLineType.Output:
                    g.node(f"{al.identifier}",shape='Mdiamond')
                    for depend in al.dependencies:
                        edges.add((depend.signature,f"{al.identifier}"))
                    # edges.add((depend.signature,define.signature))
                    

            with g.subgraph(name='clusterA') as c:
                c.attr(style='filled', color='lightgrey')
                c.node_attr.update(style='filled', color='white')


                for al in east.ast_lines+east.external_ast_lines:
                    if al.type == ASTLineType.Fact:
                        for define in al.define:
                            c.node(define.signature)
                        c.node(al.identifier)
                c.attr(label='Facts')

            with g.subgraph(name='clusterB') as c:
                c.attr(style='filled', color='lightgrey')
                c.node_attr.update(style='filled', color='white')
                for al in east.ast_lines:
                    if al.type == ASTLineType.Input:
                        c.node(f"{al.identifier}")
                c.attr(label='Inputs')



            with g.subgraph(name='clusterC') as c:
                c.attr(style='filled', color='lightgrey')
                c.node_attr.update(style='filled', color='white')

                for al in east.ast_lines +east.external_ast_lines:
                    if al.type == ASTLineType.Rule:
                        for define in al.define:
                            c.node(define.signature)
                            for depend in al.dependencies:
                                edges.add((depend.signature,define.signature))

                c.attr(label='Rules')

            with g.subgraph(name='clusterD') as c:
                c.attr(style='filled', color='lightgrey')
                c.node_attr.update(style='filled', color='white')
                for al in east.ast_lines+east.external_ast_lines:
                    if al.type == ASTLineType.Constraint:
                        for depend in al.dependencies:
                            c.node(f"{al.identifier}")
                            edges.add((depend.signature,f"{al.identifier}"))

                c.attr(label='Constraints')
            g.edges(edges)
            g.attr(label='Definition Dependency Graph')
            g.attr(fontsize='20')  
            g.render(filename=os.path.join(self.parameters['doc_dir'], "img", filename_from_source(
                self.parameters['src_dir'], east.filename).replace('.lp', ''), "ddg"), view=False)
            