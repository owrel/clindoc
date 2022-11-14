from .astprogram import *
import graphviz


class RuleDependencyGraph:
    def __init__(self,astprogram:ASTProgram) -> None:
        self.astprogram = astprogram
        g = graphviz.Digraph('G', filename='RuleDependencyGraph',format='png')

        for a in self.astprogram.astlines:
            print(a.pretty_rule())
        edges = set()
        for a in self.astprogram.astlines:
            for b in self.astprogram.astlines:
                if a != b:
                    for define in a.define:
                        for depends in b.dependencies:
                            if define.signature == depends.signature:
                                edges.add((a.pretty_rule(),b.pretty_rule()))

        g.edges(edges)
        g.attr(label='Rule Dependency Graph')
        g.attr(fontsize='20')  
        g.save('RuleDependency.png')
        
        