import operator
from functools import reduce
from itertools import combinations

class Clique():
    """
    Model for a clique of n points of a cloud.

    Required arguments:
        points -- points that make up the clique
    Optional arguments:
        k -- the clique appears when computing mutual k-nearest neighbours
    """

    def __init__(self, points, k = None, dist_matrix = None):
        self.points = list(points)
        self.k = k
        self.size = len(points)
        self.dim = self.size - 1
        self.dist_matrix = dist_matrix
        self.diameter = (max([0] + [dist_matrix[p] for p in combinations(self.points, 2)])
                if dist_matrix is not None else None)

    @property
    def faces(self):
        """ Returns a list of the faces of the clique """
        if self.dim == 0:
            return []
        else:
            return [Clique([q for q in self.points if q != p], 
                self.k if self.k is not None else None,
                self.dist_matrix if self.dist_matrix is not None else None)
                for p in self.points]

    def faces(self, filtration):
        if self.dim == 0:
            return []

        else:
            faces_points = [[q for q in self.points if q != p] for p in self.points]
            return [f for f in filtration if f.points in faces_points]
            

    @property
    def boundary(self):
        return Chain(self.faces)

    # def faces_all(self):
    #     """ Returns a list of all of the cells of the clique """
    #     faces = []
    #     for d in range(1,self.dim + 1):
    #        faces += [Clique(list(p),
    #             self.k if self.k is not None else None,
    #             self.dist_matrix if self.dist_matrix is not None else None)
    #             for p in combinations(self.points, d)]
    #     return faces

    def __eq__(self, other):
       return (set(self.points) == set(other.points))

    def __hash__(self):
        # TODO: find a better hash since hash(n) = n for integer n
        return reduce(operator.xor, [hash(p) for p in self.points], 0)

    def __repr__(self):
        return "C" + str(self.points)

    def __str__(self):
        return (f"{self.dim}-clique with points " 
                + str(self.points) 
                + f" born at k = {self.k}" if self.k is not None else "")

class Chain():
    """
    Chain of n-cliques.

    Required arguments:
        cliques -- list of simplices of the chain
    """
    def __init__(self, cliques):
        if not all([c.dim == cliques[0].dim for c in cliques]):
            raise ValueError("All simplices of the chain should have the same dimension")
        self.cliques = set(cliques)

    @property
    def dim(self):
        """ Dimension of the chain"""
        return list(self.cliques)[0].dim

    @property
    def boundary(self):
        return sum([Chain(c.faces) for c in list(self.cliques)], Chain([]))
    
    @property
    def is_cycle(self):
        return len(self.boundary.cliques) is 0

    def __add__(self, other):
        return Chain(list(self.cliques ^ other.cliques))

    def __repr__(self):
        if len(self.cliques) is 0:
            return "C[]"
        else:
            return " + ".join([repr(c) for c in list(self.cliques)])

    def __str__(self):
        return f"Chain of {self.dim}-cliques: " + repr(self)
        
        
