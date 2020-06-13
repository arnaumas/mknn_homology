import numpy as np
import networkx as nx
from math import floor
from functools import reduce
from operator import add


from clique import Clique, Chain 
from cloud import Cloud
from homology_dict import HomDict
from homology import HomologyClass

    
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
        self.k_max = 0
        self.homology = HomDict()
        self.generators = [[] for _ in range(self.cloud.dim)]

    def build_complex(self):
        cliques = [Clique([i], 0, 0) for i in range(self.cloud.size)]

        # TODO: Determine a good stopping point
        # k = 1

        for k in range(1, self.k_max):
            # Construct the mutual kNN graph
            graph = self.cloud.mknn_graph(k)
            
            # Add the new maximal cliques and their faces
            cliques += [Clique(c, k, self.cloud.dist_matrix) for c in
                    nx.enumerate_all_cliques(graph) if len(c) <= 2]

        self.complex = sorted(set(cliques), key = lambda c:(c.k, c.size, c.diameter)) 

    def compute_persistent_homology(self):
        n = 1

        for k in range(self.k_max + 1): 
            for c in self[k]:
                # Give the clique a homology class (it is not homologous to anything other
                # than itself since it is not the face of anything as of now)
                print(f"\rProcessing clique {n} out of {len(self.complex)}", end = "")
                n += 1
                self.homology[c] = HomologyClass(c.dim, Chain([c]), c.points, k)
                faces = c.faces(self.complex)


                if c.dim == 0 or reduce(add, [self.homology[f] for f in faces]).is_zero:
                    # This clique closes a cycle
                    self.generators[c.dim].append(self.homology[c])

                else:
                    # Processing is different for the case of dimension 0
                    if c.dim == 1:
                        small, large = sorted(faces,
                                key = lambda c:len(self.homology[c].representatives))
                        self.homology[large].representatives |= self.homology[small].representatives
                        self.homology[small].kill(k)
                        self.homology[small] = self.homology[large]

                    else:
                        # The youngest face is declared homologous to the sum of the other faces
                        youngest, *faces_other = sorted(faces, key = lambda f:(f.k, f.size,
                            f.diameter), reverse = True)
                        # Store the persistence data of the class to be killed
                        # if homology[youngest].dimension == 0:
                        #     persistence += [(

                        self.homology[youngest].kill(k)
                        self.homology[youngest] = reduce(add, [self.homology[f] for f in faces_other])

    def compute_persistence(self):
        lifetimes = [(g.death - g.birth)/self.k_max if g.is_dead else 1 for g in
                self.generators]
        sizes = [len(g.representatives) for g in self.generators]

        self.persistence = zip(lifetimes, sizes)

    def reset(self):
        self.complex = []
        self.homology = HomDict()
        self.generators = [[] for _ in range(self.cloud.dim)]

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
            
