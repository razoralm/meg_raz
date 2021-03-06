import re
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),"..", "basics"))

# from ti mecourse_an_config import * <--- included in calc_lbl_timecourse

from calc_time_indices import *
from prepare_ttest_results import *

from scipy import stats
from scipy import spatial
import numpy as np
import mne

from cos_an_config import *



### funcs

def calc_cos_distance(A, B):
# A, B - matrices, shape(20K,time_interval_len) >> vectorized operation
	COS = np.zeros((n_voxels))	
	for i in range(0, n_voxels):
		COS[i] = spatial.distance.cosine(A[i,:], B[i, :])
	return(COS)



def calc_s1_w2_d2(subject, time_lbl_inds):

	w1 = np.zeros((n_voxels, int(time_lbl_inds[1]-time_lbl_inds[0]))) 
	#print('w1_zeros shape: ', w1.shape)
	w2 = np.zeros((n_voxels, int(time_lbl_inds[1]-time_lbl_inds[0]))) 
	d1 = np.zeros((n_voxels, int(time_lbl_inds[1]-time_lbl_inds[0])))  
	d2 = np.zeros((n_voxels, int(time_lbl_inds[1]-time_lbl_inds[0])))
	
	for w_id, word in enumerate(words):
			
		stc = mne.read_source_estimate(data_path.format(subject, "passive1", word, integ_ms))
		#print('stc shape: ', stc.data.shape)
		#print('w1_lbl shape: ', stc.data[lbl_inds, :].shape)				
		w1 += stc.data[:, int(time_lbl_inds[0]):int(time_lbl_inds[1])]
			
		stc = mne.read_source_estimate(data_path.format(subject, "passive2", word, integ_ms))
		w2 += stc.data[:, int(time_lbl_inds[0]):int(time_lbl_inds[1])]

		stc = mne.read_source_estimate(data_path.format(subject, "passive1", distractors[w_id], integ_ms))
		d1 += stc.data[:, int(time_lbl_inds[0]):int(time_lbl_inds[1])]

		stc = mne.read_source_estimate(data_path.format(subject, "passive2", distractors[w_id], integ_ms))
		d2 += stc.data[:, int(time_lbl_inds[0]):int(time_lbl_inds[1])]

	S1 = (w1+d1)/8

	W1 = w1/4

	D1 = d1/4

	W2 = w2/4

	D2 = d2/4

#	return(S1, W2, D2)
	return(W1, D1, W2, D2)


### directoties

ttest_result = '/net/server/data/programs/razoral/platon_pmwords/target/cos/{}_cosW1W2_vs_cosD1D2_{}'

### params

#time_lbls = ["144_362ms", "144_217ms", "226_362ms"]
#time_intervals = np.array([[145, 362], [145, 217], [226, 362]])

time_lbls = ["144_362ms"]
time_intervals = np.array([[145, 362]])

#time_lbls = ["144_217ms", "226_362ms"]
#time_intervals = np.array([[145, 217], [226, 362]])

### code

stc_test = mne.read_source_estimate(data_path.format(subjects[0], "passive1", words[0], integ_ms ))

time_intervals_inds = calc_time_indices(time_intervals, data_path.format(subjects[0], "passive1", words[0], integ_ms ), integ_ms)


for t, time_interval in enumerate(time_intervals):
	
	print('calulations performed in  ', time_lbls[t])

	sub_cos_sw = np.zeros((len(subjects), n_voxels))
	sub_cos_sd = np.zeros((len(subjects), n_voxels))

	for subject_idx, subject in enumerate(subjects):

		print("\n\t({:2}/{:2}) processing {}\n".format(subject_idx+1, len(subjects), subject))

#		S1, W2, D2 = calc_s1_w2_d2(subject, time_intervals_inds[t])
		W1, D1, W2, D2 = calc_s1_w2_d2(subject, time_intervals_inds[t])
		
#		sub_cos_sw[subject_idx, :] = calc_cos_distance(S1, W2)
#		sub_cos_sd[subject_idx, :] = calc_cos_distance(S1, D2)

		sub_cos_sw[subject_idx, :] = calc_cos_distance(W1, W2)
		sub_cos_sd[subject_idx, :] = calc_cos_distance(D1, D2)


	t_stat, p_val = stats.ttest_rel(sub_cos_sw, sub_cos_sd, axis=0)

	t_stat_data, p_val_data = prepare_ttest_results(t_stat, p_val)

	p_val_stc = mne.SourceEstimate(p_val_data, vertices = stc_test.vertices, tmin = time_intervals[t][0], tstep = integ_ms)
	#p_val_stc.save(ttest_result.format("vec_p-val", time_lbl, lbl_name))
	p_val_stc.save(ttest_result.format("vec_p-val", time_lbls[t]))

	t_stat_stc = mne.SourceEstimate(t_stat_data, vertices = stc_test.vertices, tmin = time_intervals[t][0], tstep = integ_ms)
	#t_stat_stc.save(ttest_result.format("vec_t-stat", time_lbl, lbl_name))
	t_stat_stc.save(ttest_result.format("vec_t-stat", time_lbls[t]))
	






































