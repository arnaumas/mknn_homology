import numpy as np
from functools import reduce
from operator import add
from matplotlib import pyplot as plt
from matplotlib import ticker

from . import clique
from .clique import Clique, Chain 

from . import cloud
from .cloud import Cloud

from . import homology_dict
from .homology_dict import HomDict

from . import homology
from .homology import HomologyClass

class Filtration():
    """
    Simplicial filtration indexed by k built from a cloud of points by computing the
    maximal cliques of the mutual k-nearest-neighbours of the cloud

    Required arguments:
        cloud -- Data cloud containing the points
    """

    def __init__(self, cloud = None, *args, **kwargs):
        if cloud:
            self.cloud = cloud
        else:
            self.cloud = Cloud(kwargs.get("data"))
            
        self.complex = []
        self.k_max = self.cloud.size - 1
        self.homology = HomDict()
        self.generators = [[] for _ in range(self.cloud.dim)]

    def build_complex(self):
        cliques = set([Clique([i], 0, 0) for i in range(self.cloud.size)])

        # TODO: Determine a good stopping point
        # k = 1

        for k in range(1, self.k_max + 1):
            print(f"Processing step {k} out of {self.k_max}...", end = "")
            # Construct the mutual kNN graph
            print(f"\n\tCalculating MkNN graph...", end = "")
            graph = self.cloud.mknn_graph(k)
            print(f"\n\tDone!", end = "")
            
            # Add the new maximal cliques and their faces
            print(f"\n\tGathering cliques...", end = "")
            cliques = cliques.union(set([Clique(c, k) for c in
                   graph.edges]))
            print(f" Done! There are {len(cliques)} cliques", end = "\n")

        self.complex = sorted(set(cliques), key = lambda c:(c.k, c.size, c.diameter)) 

    def compute_persistent_homology(self):
        n = 1

        self.build_complex()

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
        self.lifetimes = [(g.death - g.birth)/self.k_max if g.is_dead else 1 for g in
                self.generators[0]]
        self.sizes = [len(g.representatives)/self.cloud.size for g in self.generators[0]]

    def plot_persistence(self, filename):
        fig, ax = self.persistence_plot()
        
        fig.savefig(filename, bbox_tight = 'tight')

    def persistence_plot(self):
        self.compute_persistence()
        lifetimes = np.array(self.lifetimes)
        sizes = np.array(self.sizes)
        outlierness = lifetimes/sizes

        fig = plt.figure(figsize = (8,6))
        ax = fig.subplots()
        mappable = ax.scatter(lifetimes, sizes, c = lifetimes/sizes, cmap = "cool", zorder = 2)

        k = 1
        for xy in zip(self.lifetimes, self.sizes):
            plt.annotate(f"{k}", xy, bbox = dict(facecolor = 'white', edgecolor = 'white',
                alpha = 0.5, zorder = 1))
            k += 1

        colorbar = fig.colorbar(mappable)
        colorbar.set_ticks([outlierness.max(), outlierness.min()])
        colorbar.set_ticklabels(["100%", "0%"])

        ax.set_xlabel('Lifetime (normalised)')
        ax.xaxis.set_major_formatter(ticker.PercentFormatter(xmax = 1))
        ax.set_ylabel('Size (normalised)')
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax = 1))
        
        return fig, ax

    def reset(self):
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
