# Python Program to detect cycle in an undirected graph
from collections import defaultdict


# This class represents a undirected
# graph using adjacency list representation
class Graph:

    def __init__(self, vertices):

        # No. of vertices
        self.V = vertices  # No. of vertices

        # Default dictionary to store graph
        self.graph = defaultdict(list)

        # Function to add an edge to graph

    def add_edge(self, v, w):

        # Add w to v_s list
        self.graph[v].append(w)

        # Add v to w_s list
        # self.graph[w].append(v)

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
