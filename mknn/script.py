import mknn
import numpy as np
import matplotlib.pyplot as plt
import nrrd

# Read the files
energy_raw, header = nrrd.read('19495691_150518_abd_original_glcm_JointEnergy.nrrd')
entropy_raw, header = nrrd.read('19495691_150518_abd_original_glcm_JointEntropy.nrrd')
contrast_raw, header = nrrd.read('19495691_150518_abd_original_glcm_Contrast.nrrd')

# Select data
energy = energy_raw[int(energy_raw.shape[0]/2),:,:]
entropy = entropy_raw[int(entropy_raw.shape[0]/2),:,:]
contrast = contrast_raw[int(contrast_raw.shape[0]/2),:,:]

# Put the non NaN values into lists
energy_ravel = energy[~np.isnan(energy)]
energy_idx = np.argwhere(~np.isnan(energy))

entropy_ravel = entropy[~np.isnan(entropy)]
entropy_idx = np.argwhere(~np.isnan(entropy))

contrast_ravel = entropy[~np.isnan(contrast)]
contrast_idx = np.argwhere(~np.isnan(contrast))

data = np.column_stack((energy_ravel, entropy_ravel, contrast_ravel))

# Homology computation
filt = mknn.Filtration(data = data)
filt.build_complex()
filt.compute_persistent_homology()
