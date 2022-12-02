from .astprogram import *
import graphviz


class DefinitionDependencyGraph:
    def __init__(self,astprogram:ASTProgram) -> None:
        self.astprogram = astprogram
        g = graphviz.Digraph('G', filename='DefinitionDependencyGraph',format='png')
        for al in self.astprogram.ast_lines:
            if al.type == ASTLineType.Output:
                if al.ast.ast_type == ASTType.ShowTerm:
                    g.node(f"{al.ast.term.name}/{len(al.ast.term.arguments)}",shape='Mdiamond')
                else:
                    g.node(f"{al.ast.name}/{al.ast.arity}",shape='Mdiamond')

        with g.subgraph(name='clusterA') as c:
            c.attr(style='filled', color='lightgrey')
            c.node_attr.update(style='filled', color='white')


            for al in self.astprogram.ast_lines:
                if al.type == ASTLineType.Fact:
                    for define in al.define:
                        c.node(define.signature)
            c.attr(label='Facts')

        with g.subgraph(name='clusterB') as c:
            c.attr(style='filled', color='lightgrey')
            c.node_attr.update(style='filled', color='white')
            for al in self.astprogram.ast_lines:
                if al.type == ASTLineType.Input:
                    c.node(f"{al.ast.name}/{al.ast.arity}")
            c.attr(label='Inputs')



        with g.subgraph(name='clusterC') as c:
            c.attr(style='filled', color='lightgrey')
            c.node_attr.update(style='filled', color='white')

            edges = set()
            for al in self.astprogram.ast_lines:
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
            for al in self.astprogram.ast_lines:
                if al.type == ASTLineType.Constraint:
                    for depend in al.dependencies:
                        edges.add((depend.signature,f"constraint#{al.id}"))

            c.edges(edges)
            c.attr(label='Constraints')
        g.attr(label='Definition Dependency Graph')
        g.attr(fontsize='20')  
        g.render(view=False)
        
        
        


