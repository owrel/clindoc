from .astprogram import *
import graphviz


class DefinitionDependencyGraph:
    def __init__(self,astprogram:ASTProgram) -> None:
        self.astprogram = astprogram
        g = graphviz.Digraph('G', filename='DefinitionDependencyGraph',format='png')

        for al in self.astprogram.astlines:
            if al.type == ASTLineType.Output:
                g.node(al.signature,shape='Mdiamond')

        with g.subgraph(name='clusterA') as c:
            c.attr(style='filled', color='lightgrey')
            c.node_attr.update(style='filled', color='white')


            for al in self.astprogram.astlines:
                if al.type == ASTLineType.Fact:
                    for define in al.define:
                        c.node(define.signature)
            c.attr(label='Facts')

        with g.subgraph(name='clusterB') as c:
            c.attr(style='filled', color='lightgrey')
            c.node_attr.update(style='filled', color='white')
            for al in self.astprogram.astlines:
                if al.type == ASTLineType.Input:
                    c.node(al.signature)
                    
                    
            c.attr(label='Inputs')



        with g.subgraph(name='clusterC') as c:
            c.attr(style='filled', color='lightgrey')
            c.node_attr.update(style='filled', color='white')

            edges = set()
            for al in self.astprogram.astlines:
                if al.Type == ASTLineType.Rule:
                    for define in al.define:
                        for depend in al.dependencies:
                            edges.add((depend.signature,define.signature))
            c.edges(edges)
            c.attr(label='Predicate')

        with g.subgraph(name='clusterD') as c:
            c.attr(style='filled', color='lightgrey')
            c.node_attr.update(style='filled', color='white')

            edges = set()
            for al in self.astprogram.astlines:
                if al.Type  == ASTLineType.Constraint:
                    for depend in al.dependencies:
                        edges.add((depend.signature,al.signature()))

            c.edges(edges)
            c.attr(label='Constraints')
        g.attr(label='Definition Dependency Graph')
        g.attr(fontsize='20')  
        g.save('DefinitionDependencyGraph.png')
        
        
        


