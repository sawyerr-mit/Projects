"""
search.py

BFS, Dijkstra and A* graph searches.

Adapted from CIS 454 (AI and Advanced Python) Assignment 6, University of Maine at Augusta,
Spring 2026. Original starter code by Rocko Graziano.
"""

import math
import pickle
from collections import deque

from IndexMinPQ import *
from graph import Graph


def BFS(G: Graph, s: int, t: int, debug: bool=False) -> tuple[list[int], int, int]:
    """
    Find the path with the fewest edges from s to t in an unweighted search.
    The target is considered found when it is first encountered, not when it is popped.

    return:  path        - a list of the nodes from s to t, including both
             path length - the number of edges in the path
             popcount    - the number of pops from the search frontier
    """

    popcount = 0

    print(f'\nUsing BFS to find path from {s} to {t}')

    # Initialize explored and prior.
    explored = {}               # Stores explored nodes
    prior = {}                  # Stores previous nodes visited
    explored[s] = True          # Source node starts explored
    prior[s] = None             # Source node doesn't have a prior node
    frontier = deque([s])

    # Loop over the graph until a path is found, or there are no more nodes
    while frontier:

        # Pop the first node off and save,
        # the first iteration returns the source node
        v = frontier.popleft()
        popcount += 1

        # Iterate over all the edges connected to the current node (breadth)
        for edge in G.edgesOf(v):
            u = edge.t

            # Iterate over only nodes that haven't been explored
            if not explored.get(u, False):

                # Mark the node as explored, and update where it was reached from
                explored[u] = True
                prior[u] = v

                # Checks if the current node is the target node
                if u == t:

                    # Now that the target is found, reconstruct the path by
                    # Iterating over the nodes that came before it in the list
                    # of priors until the source is reached (node == Node).
                    path = []
                    node = t
                    while node is not None:
                        path.append(node)
                        node = prior[node]

                    # Reverse the path back to normal, and return the solution
                    path.reverse()
                    return path, len(path) - 1, popcount

                # If u was not the solution, append it to
                # the frontier deque, and keep searching
                frontier.append(u)

    # Return flag data in case of error
    return [], -1, popcount


def Dijkstra(G: Graph, s: int, t: int, debug: bool=False) -> tuple[list[int], int, int]:
    """
    Find the shortest path (by edge weights) from s to t in a weighted graph.

    return:  path     - a list of the nodes from s to t, including both
             distance - the sum of the edge weights from s to t
             popcount - the number of pops from the search frontier
    """

    popcount = 0

    print(f'\nUsing Dijkstra to find path from {s} to {t}')

    # Initialize n, prior, and pathcost
    prior = {}                          # Stores previous nodes visited
    pathcost = {}                       # Stores the path costs, as graphs are weighted
    prior[s] = None                     # Source node doesn't have a prior node
    pathcost[s] = 0                     # Nothing's been explored, so no edges have been explored
    frontier = IndexMinPQ(G.sizeV())    # Now frontier is a Min Priority Queue. The argument is the size of the graph.

    # Loop over all the nodes, and initialize all nodes except for the source to inf
    # They have not been explored yet, and the path to each is not currently known
    for v in G.getVertices():
        if v.id == s:
            frontier.push(v.id, 0)
        else:
            frontier.push(v.id, math.inf)

    # Iterate over all nodes until a solution is found or all nodes have been checked
    while not frontier.isEmpty():

        # Store the current node, and its cost
        v, cost = frontier.pop()
        popcount += 1

        # Checks if the current node is the target node. Because the frontier
        # is a min priority queue, the node popped is only equal to t once
        # the cheapest path has been found
        if v == t:

            # Now that the target is found, reconstruct the path by
            # Iterating over the nodes that came before it in the list
            # of priors until the source is reached (node == Node).
            path = []
            node = t
            while node is not None:
                path.append(node)
                node = prior.get(node)

            # Reverse the path back to normal, and return the solution
            path.reverse()
            return path, pathcost[t], popcount

        # If the last node popped was not the solution, iterate over its neighbors
        # to see if any new nodes can be reached, or if going through the last node
        # was the new cheapest way to get there. This then updates the prior and
        # pathcost lists.
        for edge in G.edgesOf(v):

            # Assign u a new cost
            u = edge.t
            new_cost = pathcost.get(v, math.inf) + edge.weight

            # If that cost is smaller than what is currently known, update frontier
            if new_cost < pathcost.get(u, math.inf):
                prior[u] = v
                pathcost[u] = new_cost
                if frontier.contains(u):
                    frontier.update(u, new_cost)

    # Return flag data in case of error
    return [], -1, popcount


def aStar(G: Graph, s: int, t: int, debug: bool=False) -> tuple[list[int], int, int]:
    """
    Find the shortest path (by edge weights) from s to t in a weighted graph,
    guided by a euclidean-distance heuristic on each vertex's lat/lon.

    return:  path     - a list of the nodes from s to t, including both
             distance - the distance from s to t
             popcount - the number of pops from the search frontier
    """

    def H(u: int, v: int) -> float:
        """ Euclidean distance between the lat/lon of vertices u and v. """

        # Access tags
        tags_u = G.getTags(u)
        tags_v = G.getTags(v)

        # Access latitude and longitude
        lat_u, lon_u = tags_u['lat'], tags_u['lon']
        lat_v, lon_v = tags_v['lat'], tags_v['lon']

        # Pythagorean theorem! I knew Freshman year geometry would one day come in handy.
        return math.sqrt((lat_u - lat_v) ** 2 + (lon_u - lon_v) ** 2)

    popcount = 0

    print(f'\nUsing A* to find path from {s} to {t}')

    # Initialize n, prior, and pathcost
    prior = {}  # Stores previous nodes visited
    pathcost = {}  # Stores the path costs, as graphs are weighted
    prior[s] = None  # Source node doesn't have a prior node
    pathcost[s] = 0  # Nothing's been explored, so no edges have been explored
    frontier = IndexMinPQ(G.sizeV())  # Now frontier is a Min Priority Queue. The argument is the size of the graph.

    # Loop over all the nodes, and initialize all nodes except for the source to inf
    # They have not been explored yet, and the path to each is not currently known
    # the only difference here between Djikstra's and A* is that the starting node
    # has a starting value of its heuristic element, not 0
    for v in G.getVertices():
        if v.id == s:
            frontier.push(v.id, H(s, t))    # Heuristic instead of 0
        else:
            frontier.push(v.id, math.inf)

    # Iterate over all nodes until a solution is found or all nodes have been checked
    while not frontier.isEmpty():

        # Store the current node, and its cost
        v, cost = frontier.pop()
        popcount += 1

        # Checks if the current node is the target node. Because the frontier
        # is a min priority queue, the node popped is only equal to t once
        # the cheapest path has been found
        if v == t:

            # Now that the target is found, reconstruct the path by
            # Iterating over the nodes that came before it in the list
            # of priors until the source is reached (node == Node).
            path = []
            node = t
            while node is not None:
                path.append(node)
                node = prior.get(node)

            # Reverse the path back to normal, and return the solution
            path.reverse()
            return path, pathcost[t], popcount

        # If the last node popped was not the solution, iterate over its neighbors
        # to see if any new nodes can be reached, or if going through the last node
        # was the new cheapest way to get there. This then updates the prior and
        # pathcost lists.
        for edge in G.edgesOf(v):

            # Assign u a new cost
            u = edge.t
            new_cost = pathcost.get(v, math.inf) + edge.weight

            # If that cost is smaller than what is currently known, update frontier
            if new_cost < pathcost.get(u, math.inf):
                prior[u] = v
                pathcost[u] = new_cost
                # This is the biggest difference! Instead of the cost just being the value in the graph,
                # the cost is increased by a heuristic, in this case, euclidian distance. This is the where
                # the biggest speed-up occurs, because it allows the algorithm to prioritize edges that move
                # toward the end point. In real life, this makes sense because you wouldn't start driving north
                # if you wanted to get to Florida, for example
                new_cost += H(u, t)
                if frontier.contains(u):
                    frontier.update(u, new_cost)

    # Return flag data in case of error
    return [], -1, popcount


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    testcases = [('romania.pickle', 0, 1, False),
                 ('romania.pickle', 13, 4, False),
                 ('kennebec.pickle', 31358, 101336, False),
                 ]

    for testcase in testcases:
        print(f'\nTesting against {testcase[0]}\n')

        G = pickle.load(open(testcase[0], 'rb'))

        print(f'There are {G.sizeV()} nodes in this graph')

        path, pathlength, popcount = BFS(G, testcase[1], testcase[2], debug=testcase[3])
        print(f'BFS Path is {pathlength} edges long; found in {popcount:,d} pops\n{path}')

        path, pathlength, popcount = Dijkstra(G, testcase[1], testcase[2], debug=testcase[3])
        print(f'Dijkstra Path is {pathlength} long in {len(path)-1} edges; found in {popcount:,d} pops\n{path} ')

        path, pathlength, popcount = aStar(G, testcase[1], testcase[2], debug=testcase[3])
        print(f'A* Path is {pathlength} long in {len(path)-1} edges; found in {popcount:,d} pops\n{path} ')
