import numpy as np
import networkx as nx
from math import floor

from clique import Clique, Chain 
from cloud import Cloud
# from homology import HomologyClass

    
class Filtration():
    """
    Simplicial filtration indexed by k built from a cloud of points by computing the
    maximal cliques of the mutual k-nearest-neighbours of the cloud

    Required arguments:
        cloud -- Data cloud containing the points
    """

    def __init__(self, cloud):
        self.cloud = cloud
        self.complex = []

    def build_complex(self):
        cliques = [Clique([i], 0, 0) for i in range(self.cloud.size)]

        for k in range(1, self.cloud.size):
            # Construct the mutual kNN graph
            graph = self.cloud.mknn_graph(k)

            # Gather all the cliques
            new_cliques = [Clique(c, k, self.cloud.dist_matrix) for c in
                    nx.enumerate_all_cliques(graph)]
            # Add the new maximal cliques and their faces
            cliques += new_cliques

        self.complex = sorted(set(cliques), key = lambda c:(c.k, c.size, c.diameter)) 

    def reset(self):
        self.complex = []
        self.build_complex()

    def __getitem__(self, n):
        """
        Return an iterable containing all of the cliques inside the n-th step of the
        filtration
        """
        for c in self.complex:
            if c.k < n:
                continue
            elif c.k == n:
                yield c
            else:
                break
            
