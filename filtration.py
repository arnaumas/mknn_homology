from clique import Clique, Chain 
import numpy as np
import networkx as nx
from scipy import sparse

    
class Filtration():
    """
    Simplicial filtration indexed by k built from a cloud of points by computing the
    maximal cliques of the mutual k-nearest-neighbours of the cloud

    Required arguments:
        points -- Data cloud
    """

    def __init__(points):
        self.points = points
        self.complex = []

    def build_complex(self):
        dist_matrix = self.points.compute_dist_matrix()
        cliques = set()

        for k in range(1, self.points.dimension):
            # Construct the mutual kNN graph
            graph = mknn_graph(k, dist_matrix)

            # Gather all the maximal cliques
            new_cliques = {Clique(c,k) for c in nx.find_cliques(graph) 
                    if c.size <= max_size}

            # Add the new cliques
            cliques |=  new_cliques

        self.complex = sorted(cliques, key = lambda c:(c.k, c.size, c.diameter)) 
       

