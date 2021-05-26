import numpy as np
import networkx as nx
from scipy import sparse

def vprint(verbose, *args, **kwargs):
    if verbose:
        print(*args, **kwargs)

class Cloud():
    """
    Cloud of N points with n characteristics

    Required arguments:
    points     --- Set of N points of with n characteristics (np.array with shape (N,n))
    """

    def __init__(self, points):
        self.points = points
        self.size, self.dim = points.shape
        self.dist_matrix = self.compute_dist_matrix().argsort(axis = -1)

    def compute_dist_matrix(self):
        """
        Computes the distance matrix and assigns it to self.dist_matrix
        """
        # Use broadcasting to get an array of shape (N,N,n) with the differences of every
        # possible pair of points
        differences = self.points[np.newaxis,:] - self.points[:, np.newaxis]

        # Calculate the squares of the distances by summing along the last axis
        return (differences**2).sum(axis = -1)

    def mknn_graph(self,k,verbose):
        """
        Computes the mutual k-nearest neighbours graph of the cloud and returns it as a
        NetworkX graph
        
        Required arguments:
            k --- integer, will compute mutual kNN graph
            verbose --- whether the program prints out logs

        Return:
            a NetworkX representation of the mutual kNN graph
        """
        # Pick out the k nearest neighbours of every node
        vprint(verbose, f"\n\t\tPicking out the nearest neighbours...", end = "")
        nearest_neighbours = np.array([(i, self.dist_matrix[i,j+1]) for i in
            range(self.size) for j in range(k)])
        vprint(verbose, f" Done!", end = "")

        # Build the adjacency matrix of the directed kNN graph
        vprint(verbose, f"\n\t\tBuilding the adjacency matrix...", end = "")
        adj_directed = sparse.coo_matrix(([1] * k * self.size, (nearest_neighbours[:, 0],
            nearest_neighbours[:, 1])), shape = (self.size, self.size)).toarray()

        # Construct the adjacency matrix of the mutual kNN graph
        adj = adj_directed * adj_directed.T
        vprint(verbose, f" Done!", end = "")

        # Return a NetworkX graph built from the adjacency matrix
        return nx.from_numpy_matrix(adj)

    def retrieve_clique(self, clique):
        """
        Returns the coordinates of the points corresponding to the given clique
        """
        return [self.points[i] for i in clique.points]

    def __str__(self):
        return "<Cloud of %d points in R^%d>" % (self.size, self.dim)

