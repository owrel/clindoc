from ..astprogram import *
from .component import Component, ArgumentParser
from typing import Dict
from ..utils import create_dir, path_from_source
import graphviz
import os



class DependencyGraph(Component):
    name = "dependencygraph"
    parse_group_description = "Dependency graph parameters"

    @classmethod
    def cmdline_documentation(cls, parser: ArgumentParser) -> ArgumentParser:
        group = super().cmdline_documentation(parser)

        group.add_argument('--dependencygraph.format', action='store', default="svg", help="Format of the graphs ")



    def __init__(self, builder,parameters:Dict) -> None:
        super().__init__(builder,parameters)
        self.parameters = parameters
        # Checking parameters
        if not parameters[self.name].get('format'):
            self.parameters[self.name]['format'] = 'svg'


    def build_rst_file(self) -> None:
        # Create folder for graphs
        create_dir(os.path.join(self.parameters['doc_dir'], "img"))
        self._build_rule_dependency_graph()
        self._build_definition_dependency_graph()

        self.document.title('Dependency Graphs')
        self.document.newline()
        for astprogram in self.builder.astprograms:
            self.document.h2(path_from_source(
                self.parameters['src_dir'], astprogram._path).replace('.lp', ''))
            self.document.newline()
            self.document.directive('image', os.path.join( "img",
                                    path_from_source(self.parameters['src_dir'], astprogram._path).replace('.lp', ''), "rdg."+ self.parameters[self.name]['format']))
            self.document.newline()
            self.document.directive('image', os.path.join( "img",
                                    path_from_source(self.parameters['src_dir'], astprogram._path).replace('.lp', ''), "ddg."+ self.parameters[self.name]['format']))

    def _build_rule_dependency_graph(self):
        for astprogram in self.builder.astprograms:
            g = graphviz.Digraph('G', format=self.parameters[self.name]['format'])
            pool = []
            for a in astprogram.ast_lines:
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
            g.render(filename=os.path.join(self.parameters['doc_dir'], "img", path_from_source(
                self.parameters['src_dir'], astprogram._path).replace('.lp', ''), "rdg"), view=False)

    
    def _build_definition_dependency_graph(self):
        for astprogram in self.builder.astprograms:
            g = graphviz.Digraph('G',format=self.parameters[self.name]['format'])
            for al in astprogram.ast_lines:
                if al.type == ASTLineType.Output:
                    if al.ast.ast_type == ASTType.ShowTerm:
                        g.node(f"{al.ast.term.name}/{len(al.ast.term.arguments)}",shape='Mdiamond')
                    else:
                        g.node(f"{al.ast.name}/{al.ast.arity}",shape='Mdiamond')

            with g.subgraph(name='clusterA') as c:
                c.attr(style='filled', color='lightgrey')
                c.node_attr.update(style='filled', color='white')


                for al in astprogram.ast_lines:
                    if al.type == ASTLineType.Fact:
                        for define in al.define:
                            c.node(define.signature)
                c.attr(label='Facts')

            with g.subgraph(name='clusterB') as c:
                c.attr(style='filled', color='lightgrey')
                c.node_attr.update(style='filled', color='white')
                for al in astprogram.ast_lines:
                    if al.type == ASTLineType.Input:
                        c.node(f"{al.ast.name}/{al.ast.arity}")
                c.attr(label='Inputs')



            with g.subgraph(name='clusterC') as c:
                c.attr(style='filled', color='lightgrey')
                c.node_attr.update(style='filled', color='white')

                edges = set()
                for al in astprogram.ast_lines:
                    if al.type == ASTLineType.Rule:
                        for define in al.define:
                            for depend in al.dependencies:
                                edges.add((depend.signature,define.signature))
                c.edges(edges)
                c.attr(label='Rules')

            with g.subgraph(name='clusterD') as c:
                c.attr(style='filled', color='lightgrey')
                c.node_attr.update(style='filled', color='white')

                edges = set()
                for al in astprogram.ast_lines:
                    if al.type == ASTLineType.Constraint:
                        for depend in al.dependencies:
                            edges.add((depend.signature,f"constraint#{al.id}"))

                c.edges(edges)
                c.attr(label='Constraints')
            g.attr(label='Definition Dependency Graph')
            g.attr(fontsize='20')  
            g.render(filename=os.path.join(self.parameters['doc_dir'], "img", path_from_source(
                self.parameters['src_dir'], astprogram._path).replace('.lp', ''), "ddg"), view=False)
            