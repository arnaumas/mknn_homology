import operator
from functools import reduce

class Clique():
    """
    Model for a clique of n points of a cloud.

    Required arguments:
        points -- points that make up the clique
    Optional arguments:
        k -- the clique appears when computing mutual k-nearest neighbours
    """

    def __init__(self, points, k = None, diameter = None):
        self.points = points
        self.k = k
        self.size = len(points)
        self.diameter = diameter

    @property
    def dim(self):
        """ Dimension of the clique """
        return len(self.points)

    @property
    def faces(self):
        """ Returns a list of the faces of the clique """
        if len(self.points) is 1:
            return []
        else:
            return [Clique([q for q in self.points if q != p], self.k if self.k is not
                None else None) for p in self.points]

    def __eq__(self, other):
       return (set(self.points) == set(other.points))

    def __hash__(self):
        # TODO: find a better hash since hash(n) = n for integer n
        return reduce(operator.xor, [hash(p) for p in self.points])

    def __repr__(self):
        return "C" + str(self.points)

    def __str__(self):
        return (f"{self.size}-clique with points " 
                + str(self.points) 
                + " born at k = {self.k}" if self.k is not None else "")

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
        return Chain(self.cliques ^ other.cliques)

    def __repr__(self):
        if len(self.cliques) is 0:
            return "C[]"
        else:
            return " + ".join([repr(c) for c in self.cliques])

    def __str__(self):
        return f"Chain of {self.dim}-cliques: " + str(self.cliques)
        
        

