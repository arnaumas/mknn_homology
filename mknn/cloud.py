import numpy as np
import networkx as nx
from scipy import sparse

import torch
import dgl

class Cloud():
    """
    Cloud of N points with n characteristics

    Required arguments:
    points     --- Set of N points of with n characteristics (np.array with shape (N,n))
    """

    def __init__(self, points):
        self.points = points
        self.size, self.dim = points.shape
        self.dist_matrix = torch.artgsort(self.compute_dist_matrix(), axis = 1) 

    def compute_dist_matrix(self):
        """
        Computes the distance matrix and assigns it to self.dist_matrix
        """
        # Use broadcasting to get an array of shape (N,N,n) with the differences of every
        # possible pair of points
        differences = torch.unsqueeze(self.points, 1) - torch.unsqueeze(self.points, 0)

        # Calculate the squares of the distances by summing along the last axis
        return torch.linalg.norm(differences, dim = 2)

    def mknn_graph(self,k):
        """
        Computes the mutual k-nearest neighbours graph of the cloud and returns it as a
        NetworkX graph
        
        Required arguments:
            k --- integer, will compute mutual kNN graph

        Return:
            a NetworkX representation of the mutual kNN graph
        """

        # List the k nearest neighbours of each node
        neighbours = self.dist_matrix[:, 1:k + 1]

        # List all the edges of the kNN graph
        A = torch.stack((
            torch.unsqueeze(torch.arange(self.size), 1).repeat(1, k),
            neighbours
            ), dim = 2).view(-1, 2)

        # List all the edges of the reversed kNN graph
        At = torch.vstack((A[:,1], A[:,0])).transpose(1,0)

        C = torch.unsqueeze(A,0) == torch.unsqueeze(At,1)
        # Lists all the edges that appear in both adjacency matrices
        edge_idx = (C[...,0] & C[...,1]).nonzero()
        adj = A[edge_idx[:,0],:]

        graph = dgl.graph((adj[:,0], adj[:,1]), num_nodes = self.size)

        return graph

        # print(f"\n\t\tPicking out the nearest neighbours...", end = "")
        # print(f" Done!", end = "")

        # print(f"\n\t\tBuilding the adjacency matrix...", end = "")

        # print(f" Done!", end = "")

    def retrieve_clique(self, clique):
        """
        Returns the coordinates of the points corresponding to the given clique
        """
        return [self.points[i] for i in clique.points]

    def __str__(self):
        return "<Cloud of %d points in R^%d>" % (self.size, self.dim)

