import numpy as np
from cloud import Cloud
from filtration import Filtration
from homology import compute_persistent_homology

data = np.array([[0,0], [0,1], [1,0], [1,1]])
cloud = Cloud(data)
fil = Filtration(cloud)
fil.build_complex()

hom = compute_persistent_homology(fil)
