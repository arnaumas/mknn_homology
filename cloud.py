import numpy as np
import networkx as nx
from scipy import sparse

class Cloud():
    """
    Cloud of N points with n characteristics

    Required arguments:
    points     --- Set of N points of with n characteristics (np.array with shape (N,n))
    """

    def __init__(self, points):
        self.points = points
        self.size, self.dim = points.shape
        self.dist_matrix = self.compute_dist_matrix()

    def compute_dist_matrix(self):
        """
        Computes the distance matrix and assigns it to self.dist_matrix
        """
        # Use broadcasting to get an array of shape (N,N,n) with the differences of every
        # possible pair of points
        differences = self.points[np.newaxis,:] - self.points[:, np.newaxis]

        # Calculate the squares of the distances by summing along the last axis
        return (differences**2).sum(axis = -1)

    def mknn_graph(self,k):
        """
        Computes the mutual k-nearest neighbours graph of the cloud and returns it as a
        NetworkX graph
        
        Required arguments:
            k --- integer, will compute mutual kNN graph

        Return:
            a NetworkX representation of the mutual kNN graph
        """
        # Sort the distance matrix so that the i-th row shows the nodes ordered by their
        # distance to node i
        dist_matrix_sorted = self.dist_matrix.argsort(axis = -1)

        # Pick out the k nearest neighbours of every node
        nearest_neighbours = np.array([(i, dist_matrix_sorted[i,j+1]) for i in
            range(self.size) for j in range(k)])

        # Build the adjacency matrix of the directed kNN graph
        adj_directed = sparse.coo_matrix(([1] * k * self.size, (nearest_neighbours[:, 0],
            nearest_neighbours[:, 1])), shape = (self.size, self.size)).toarray()

        # Construct the adjacency matrix of the mutual kNN graph
        adj = adj_directed * adj_directed.T

        # Return a NetworkX graph built from the adjacency matrix
        return nx.from_numpy_matrix(adj)

    def retrieve_clique(self, clique):
        """
        Returns the coordinates of the points corresponding to the given clique
        """
        return [self.points[i] for i in clique.points]

    def __str__(self):
        return "<Cloud of %d points in R^%d>" % (self.size, self.dim)
