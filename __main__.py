import sys
import numpy as np

from mknn_homology.clique import Clique, Chain 
from mknn_homology.cloud import Cloud
from mknn_homology.filtration import Filtration
from mknn_homology.homology_dict import HomDict
from mknn_homology.homology import HomologyClass

def main():
    if len(sys.argv) == 3:
        data_file = sys.argv[1]
        plot_name = sys.argv[2]
        plot_file = sys.argv[2]
    elif len(sys.argv) == 4:
        data_file = sys.argv[1]
        plot_name = sys.argv[2]
        plot_file = sys.argv[3]

    data = np.genfromtxt(fname = data_file, skip_header = 1)
    cloud = Cloud(data)
    filt = Filtration(cloud)

    filt.build_complex()
    filt.compute_persistent_homology()
    filt.compute_persistence()
    filt.persistence_plot(plot_name, plot_file)

    return


        

