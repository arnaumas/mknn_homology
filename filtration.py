import numpy as np
import networkx as nx
from itertools import combinations

from .clique import Clique, Chain 
from .cloud import Cloud

    
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
        cliques = {Clique([i], 0, 0) for i in range(self.cloud.size)}

        for k in range(1, self.cloud.size):
            # Construct the mutual kNN graph
            graph = self.cloud.mknn_graph(k)

            # Gather all the maximal cliques
            new_cliques = {Clique(c, k, 
                # Computes the diameter of the clique inline
                max([0] + [self.cloud.dist_matrix[p] for p in combinations(c, 2)]))
                for c in nx.find_cliques(graph)}

            # Add the new cliques
            cliques |=  new_cliques

        self.complex = sorted(cliques, key = lambda c:(c.k, c.size, c.diameter)) 
       

