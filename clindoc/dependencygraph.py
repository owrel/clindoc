from .astprogram import ASTProgram
from clingo.ast import ASTType
import clingraph


class DependencyGraph:
    def __init__(self,ast:ASTProgram) -> None:
        self.fb = clingraph.Factbase()
        self.name = ast._path
        self.nodes = []
        self.edges = []
        self._create_graph(ast)
        self.fb.add_fact_string(self._graph_to_fact())
        self.render_graph()


    def _create_graph(self,ast:ASTProgram):
        for node in ast.astnodes:
            if node.type == ASTType.Rule:

                ## fact 
                if node._child_keys_separation['head'] and not node._child_keys_separation['body']:
                    for signature in node._child_keys_separation['head']:
                        if not signature in self.nodes:
                            self.nodes.append(signature)

                ## rule
                elif node._child_keys_separation['head'] and node._child_keys_separation['body']:

                    for signature in node._child_keys_separation['head']:
                        if not signature in self.nodes:
                            self.nodes.append(signature)

                    for t in node._child_keys_separation['body']:
                        for f in node._child_keys_separation['head']:
                            c = (f,t)
                            if not c in self.edges:
                                self.edges.append(c)




    def _graph_to_fact(self):
        ret = f'graph("{self.name}").'
        for node in self.nodes:
            ret += f'node("{node}","{self.name}").\n'

        for edge in self.edges:
            ret += f'edge(("{edge[0]}","{edge[1]}"),"{self.name}").\n'
        return ret

    def render_graph(self, output="./graph"):
        graphs = clingraph.graphviz.compute_graphs(self.fb)
        clingraph.graphviz.render(graphs,directory="./", name_format=output)