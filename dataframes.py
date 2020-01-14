import numpy as np

points = np.genfromtxt('Immuno_RNASeq_radScore.csv', skip_header = 1,
        usecols = range(5, 11), delimiter = ';')

