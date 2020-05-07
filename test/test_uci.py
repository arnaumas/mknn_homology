import unittest

import numpy as np
from scipy.io import loadmat

from cloud import Cloud
from filtration import Filtration
from homology import compute_persistent_homology



class TestPersHo(unittest.TestCase):
    def test_iris(self):

        name = 'test/Iris_1_0_8_0.mat'

        mat = loadmat(name)
        data = mat['FeatOutLier']

        #data = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        cloud = Cloud(data[:10,:])
        fil = Filtration(cloud)
        fil.build_complex()

        hom = compute_persistent_homology(fil)

        print(hom)

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
