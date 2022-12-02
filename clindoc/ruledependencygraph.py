from .astprogram import *
import graphviz


class RuleDependencyGraph:
    def __init__(self,astprogram:ASTProgram) -> None:
        self.astprogram = astprogram
        g = graphviz.Digraph('G', filename='RuleDependencyGraph',format='svg')
        
        def pretty_display(al:ASTLine) -> str:
            ret = ""
            if al.type == ASTLineType.Constraint:
                ret += f"constraint#{al.id}"
            else :

                for define in al.define:
                    ret += define.signature + " "

            ret += f" | Position (line;{al.ast.location.begin.line})"
            return ret

        pool = []
        for a in self.astprogram.ast_lines:
            if a.type == ASTLineType.Rule or a.type == ASTLineType.Constraint or a.type == ASTLineType.Fact:
                pool.append(a) 
        edges = set()
        for n in pool:
            g.node(pretty_display(n),href=n._location_link)
        for a in pool:
            for b in pool:
                if a != b:
                    for define in a.define:
                        for depends in b.dependencies:
                            if define.signature == depends.signature:
                                edges.add((pretty_display(a),pretty_display(b)))

        g.edges(edges)
        g.attr(label='Rule Dependency Graph')
        g.attr(fontsize='20')  
        g.render(view=False)
        
        