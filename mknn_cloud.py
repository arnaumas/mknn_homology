from simplex import Simplex, Chain
import numpy as np
import networkx as nx
from scipy import sparse
import operator
from functools import reduce

class Cloud():
    """
    Cloud of N points with n characteristics

    Required arguments:
    points     --- Set of N points of with n characteristics (np.array with shape (N,n))
    """

    def __init__(self, points):
        self.points = points
        self.size, self.dimension = points.shape

    def __str__(self):
        return "<Cloud of  %d points in R^%d>" % (self.size, self.dimension)

    def dist_matrix(self):
        # Use broadcasting to get an array of shape (N,N,n) with the differences of every
        # possible point in points
        differences = self.points[np.newaxis,:] - points[:, np.newaxis]

        # Calculate the squares of the distances by summing along the last axis
        return (differences**2).sum(axis = -1)
