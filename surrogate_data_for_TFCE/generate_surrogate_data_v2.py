import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt
import mne
import os
import sys

def get_label_active_indices(label_filename):
    label = mne.read_label(label_filename)
    max_stc_vertex_ind = 10242
    return label.vertices[label.vertices<max_stc_vertex_ind]


def normrnd_add_constant(mean, variance, constant, mod_vertices, time_len):
    
    add_constant = np.random.uniform(low=constant, high=variance/4, size=(len(mod_vertices), time_len))
    
    W = np.random.normal(loc = mean, scale = variance, size = (n_voxels, time_len))
                                     
    W[mod_vertices,:] = W[mod_vertices,:] + add_constant
    
    return(W)


N_inds = 0

surrogate_data_path = '/data/programs/razoral/platon_pmwords/target/data_for_TFCE/surrogate/{}_{}_{}_{}' 
                                                                                 # D/W_modification_param_n

lbl_path = '/data/programs/razoral/platon_pmwords/scripts/raz/surrogate_data_for_TFCE/test_lbls/{}-lh.label'

#lbls = ["prefrontal", "general_ROI", "motor", "insula_opercular", "insula_subcentral", "insula_short", "transvers", "temporal_mini1", "temporal_mini2", "temporal_real", "temporal_long"]

lbls = ["prefrontal", "motor", "insula_opercular", "insula_subcentral", "insula_short", "transvers", "temporal_mini1", "temporal_mini2", "temporal_real"]

for lbl_id, lbl_name in enumerate(lbls):
    
    inds_cur = get_label_active_indices(lbl_path.format(lbl_name))
    
       
    N_inds = N_inds + np.array(list(inds_cur.shape))
    
    if lbl_id == 0:
        lbls_inds = [inds_cur]
    else:
        lbls_inds.append(inds_cur)

print('\nnumber of indeces:', N_inds)
all_lbls_inds = np.concatenate(lbls_inds)

stc1 = mne.read_source_estimate("/data/programs/razoral/platon_pmwords/target/manual_ttest/p-val_24_integ5_dw_vs_dd.stc-rh.stc")


time_len = 10
n_voxels = 20484

difference_variations = np.array([10, 2.5, 1, 0.5, 0.2, 0.1, 0.05, 0.01])
#var = 0.1 mean = 0.4


for n in range(30): # n comparison

    D = np.random.normal(loc = 0.4, scale = 0.1, size = (n_voxels, time_len))
    
    D_stc = mne.SourceEstimate(D, vertices=stc1.vertices, tmin=0, tstep=1)
    D_stc.save(surrogate_data_path.format("Dgauss","mean0.4","var0.1",n))
    # D/W_modification_param_n
    
    for c, constant in enumerate(difference_variations):

        W = normrnd_add_constant(0.4, 0.1, constant, all_lbls_inds, time_len)

        W_stc = mne.SourceEstimate(W, vertices=stc1.vertices, tmin=0, tstep=1)
        W_stc.save(surrogate_data_path.format('Wgauss','add_const', str(constant), n))


