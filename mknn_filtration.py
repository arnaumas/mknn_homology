from simplex import Simplex, Chain
import numpy as np

class Clique():
    """
    Model for a clique of n points of a cloud.
    """

    def __init__(self, points):
        self.points = points
        self.size = len(points)
        self.diameter = max([0] + [dist(*p) for p in combinations(points, 2)])
    
def dist(x,y):
    return sum((np.array(x) - np.array(y))**2)

def compute_k_cliques(points, k):
    # TODO: implement this function
    return 0

def create_clique_filtration(points):
    # Maximum size of clique to allow
    max_size = len(points[0])
    
    filtration = [Clique(p) for p in points]
    for k in range(1, len(points)):
        # Add all of the new cliques
        k_cliques = [c for c in compute_k_cliques(points, k) if c is not in filtration and  c.size <= max_size]
        cliques.extend(k_cliques)
        
    # Sort the cliques by size and then by diameter
    filtration.sort(key = lambda c:(c.size, c.diameter))

    # Transform cliques into simplexes
    return [Simplex(c) for c in filtration]


        

        

        
