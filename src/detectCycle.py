# Python Program to detect cycle in an undirected graph
from collections import defaultdict
from detectCyclePaths import CyclicGraph
import numpy as np
import math

# This class represents a undirected
# graph using adjacency list representation


class Graph:

    def __init__(self, vertices):

        # No. of vertices
        self.V = vertices  # No. of vertices

        # Default dictionary to store graph
        self.graph = defaultdict(set)
        self.edges = set()
        # Function to add an edge to graph

    def add_edge(self, v, w):

        # Add w to v_s list
        self.graph[v].add(w)

        # Add v to w_s list
        self.graph[w].add(v)

        self.edges.add((v, w))

    def __str__(self):
        return f"{self.graph}"

    # A recursive function that uses
    # visited[] and parent to detect
    # cycle in subgraph reachable from vertex v.
    def is_cyclic_util(self, v, visited, parent):

        # Mark the current node as visited
        visited[v] = True

        # Recur for all the vertices
        # adjacent to this vertex
        for i in self.graph[v]:

            # If the node is not
            # visited then recurse on it
            if not visited[i]:
                if self.is_cyclic_util(i, visited, v):
                    return True
            # If an adjacent vertex is
            # visited and not parent
            # of current vertex,
            # then there is a cycle
            elif parent != i:
                return True

        return False

    # Returns true if the graph
    # contains a cycle, else false.
    def is_cyclic(self):

        # Mark all the vertices
        # as not visited
        visited = [False] * self.V

        # Call the recursive helper
        # function to detect cycle in different
        # DFS trees
        for i in range(self.V):

            # Don't recur for u if it
            # is already visited
            if not visited[i]:
                if self.is_cyclic_util(i, visited, -1):
                    return True

        return False

    def get_average_bond_length(self, corners_array):
        bond = int(np.mean(np.array([math.hypot(corners_array[i][0] - corners_array[j]
                                                [0], corners_array[i][1] - corners_array[j][1]) for i, j in self.edges])))
        return bond

    def get_all_cycles(self):
        if self.is_cyclic():
            return self.convert_to_cyclic_graph_object()
        else:
            print("Graph is not cyclic")
            return None

    def convert_to_cyclic_graph_object(self):
        # pairs = {(0, 1), (0, 1), (1, 0), (1, 2), (1, 0), (2, 1)}
        self.edges = set((a, b) if a <= b else (b, a) for a, b in self.edges)
        cyclic_graph = CyclicGraph(self.edges)
        return cyclic_graph.find_all_cycles()
