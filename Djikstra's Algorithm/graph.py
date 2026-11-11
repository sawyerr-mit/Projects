"""
graph.py
Rocko Graziano, University of Maine at Augusta, 2026

This implements a simple class Graph in adjacency list format

The graph is undirected and weighted

A vertex id is an integer >= 0.

The client program is responsible for ensuring that (a) the
vertex ids are unique (b) they are added to the graph in
monotonic order such that the ids for n vertices are (0,1,2,3,..., n-1)


"""

class Graph():
    def __init__(self, isDirected=False):
        self.V = []
        self.isDirected= isDirected # directed (True) or undirected (False) graph

    class Vertex:
        def __init__(self, id: int, tags: dict | None):
            self.id = id
            self.tags = dict(tags)
            self.edges = set()

        def __str__(self) -> str:
            edgeset = ''
            for edge in self.edges:
                edgeset += f'{edge}, '
            return (f'{self.id} {self.tags} Edges: {edgeset[:-2]}')

        def ID(self) -> int:
            return self.id

    class Edge:
        def __init__(self, s: int, t: int, w: int | float | None = None):
            self.s = s
            self.t = t
            self.weight = w

        def __str__(self) -> str:
            return f'({self.s}-{self.t}) [{self.weight}]'

    def sizeV(self) -> int:
        return len(self.V)

    def addVertex(self, v: int, tags: dict | None ) -> None:
        self.V.append(self.Vertex(v, tags))

    def addEdge(self, s: int, t: int, w: int | float) -> None:
        """ adds edge (s,t) of weight w to the graph.
            Precondition: both s & t exist as vertices in the graph """
        self.V[s].edges.add(self.Edge(s, t, w))

    def getTags(self, s: int) -> dict:
        return self.V[s].tags

    def edgesOf(self, v: int) -> list[Edge]:
        edges = []
        for edge in self.V[v].edges:
            edges.append(edge)
        return edges

    def getVertices(self) -> list[Vertex]:
        verts = []
        for v in self.V:
            verts.append(v)
        return verts

def main():
    """ simple smoke test"""

    G = Graph()

    G.addVertex(0, {"lat": 1, 'lon': 2, 'label': 'alpha'})
    G.addVertex(1, {"lat": 3, 'lon': 4, 'label': 'beta'})
    G.addVertex(2, {"lat": 5, 'lon': 6, 'label': 'charlie'})

    G.addEdge(0, 1, 10)
    G.addEdge(0, 2, 5)
    G.addEdge(1, 0, 10)
    G.addEdge(2, 0, 5)

    print(f'There are {G.sizeV()} Nodes')

    for v in G.getVertices():
        print(v)
        for e in G.edgesOf(v.id):
            print(e)


if __name__ == "__main__":  main()
