import re
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),"..", "basics"))

# from timecourse_an_config import * <--- included in calc_lbl_timecourse



from calc_time_indices import *
from prepare_ttest_results import *
from get_lbl_indices import*

from scipy import stats
from scipy import spatial
import numpy as np
import mne
from matplotlib import pyplot
pyplot.switch_backend('agg')

from cos_an_config import *



### funcs

def calc_cos_distance(A, B):
# A, B - matrices, shape(20K,time_interval_len) >> vectorized operation
	COS = np.zeros((n_voxels))	
	for i in range(0, n_voxels):
		COS[i] = spatial.distance.mahalanobis(A[i,:], B[i, :])
	return(COS)

def calc_mah_distance(X, S, inv_covS):
# A, B - matrices, shape(20K,time_interval_len) >> vectorized operation
	mah = np.zeros((n_voxels))	
	for i in range(0, n_voxels):
		mah[i] = spatial.distance.mahalanobis(X[i,:], S[i, :], inv_covS)
	return(mah)



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

	W2 = w2/4

	D2 = d2/4

	return(S1, W2, D2)



### directoties

ttest_result = '/net/server/data/programs/razoral/platon_pmwords/target/cos/{}_cosS1W2_vs_cosS1D2_{}'#mah

lbls_path = '/net/server/data/programs/razoral/platon_pmwords/lbls/ttest/otladka/'

img_path = '/net/server/data/programs/razoral/platon_pmwords/target/manual_ttest/144_362ms/circular_insula_check/S1_W2_D2/'



### params

#timings = ["144_362ms", "144_217ms", "226_362ms"]
#time_intervals = [[145, 362], [145, 217], [226, 362]] 

time_lbls = ["144_362ms"]
time_intervals = np.array([[145, 362]])

distance_type = 'mah' #'cos' or 'mah'

### code

stc_test = mne.read_source_estimate(data_path.format(subjects[0], "passive1", words[0], integ_ms ))


time_intervals_inds = calc_time_indices(time_intervals, data_path.format(subjects[0], "passive1", words[0], integ_ms ), integ_ms)


lbls_list = [lbl for lbl in os.listdir(lbls_path) if '.label' in lbl]
print('\n labels in folder: ', len(lbls_list))
print('\n labels :')
for i in range(0, len(lbls_list)):
	print('\n', str(i+1)+'.', lbls_list[i])
	

lbl_name = re.sub('-[lr]h.label', '', lbls_list[0])
print('\n', lbl_name)

ROIinds = get_lbl_active_indices(lbls_path+lbls_list[0])
print(len(ROIinds))


for t, time_interval in enumerate(time_intervals):
	
	print('calulations performed in  ', time_lbls[t])

	sub_cos_sw = np.zeros((len(subjects), n_voxels))
	sub_cos_sd = np.zeros((len(subjects), n_voxels))

	for subject_idx, subject in enumerate(subjects):
		print("\n\t({:2}/{:2}) processing {}\n".format(subject_idx+1, len(subjects), subject))
		
		S1 = []; W2 = []; D2 = [];

		S1, W2, D2 = calc_s1_w2_d2(subject, time_intervals_inds[t])
		
		time_range = np.arange(time_intervals_inds[t][0], time_intervals_inds[t][1])

		'''pyplot.figure(subject_idx+1)
		pyplot.title(lbl_name + '_avg_timecourse')
		pyplot.xlabel("time [ms]")
		pyplot.ylabel("avg_activation [nA]")
		pyplot.xlim(time_intervals_inds[t][0], time_intervals_inds[t][1])

		pyplot.plot(time_range, np.mean(S1[ROIinds,:], axis=0), linewidth = 1, color = "g", label = "S1")
		pyplot.plot(time_range, np.mean(W2[ROIinds,:], axis=0), linewidth = 1, color = "r", label = "W2")	
		pyplot.plot(time_range, np.mean(D2[ROIinds,:], axis=0), linewidth = 1, color = "b", label = "D2")
		pyplot.plot(time_range, np.mean((W2[ROIinds,:]-S1[ROIinds,:]), axis=0), linewidth = 1.5,  color = "m", label = "W2-S1")	
		pyplot.plot(time_range, np.mean((D2[ROIinds,:]-S1[ROIinds,:]), axis=0), linewidth = 1.5, color = "c", label = "D2-S1")
	
		pyplot.legend(loc = "upper right", framealpha = 0.5)
		pyplot.grid()
		pyplot.axvline(0, color="#888888")
		pyplot.axhline(0, color="#888888")
		pyplot.savefig(img_path + lbl_name + '_' + subject + '.png')
		#pyplot.show()'''	

		if distance_type == 'cos':		

			sub_dist_sw[subject_idx, :] = calc_cos_distance(S1, W2)
			sub_dist_sd[subject_idx, :] = calc_cos_distance(S1, D2)

		elif distance_type == 'mah':

			sub_dist_sw[subject_idx, :] = calc_mah_distance(S1, W2)
			sub_dist_sd[subject_idx, :] = calc_mah_distance(S1, D2)

		print('\n distance: ', distance_type)
		print('\n dist_sw_'+ lbl_name + '_' + subject + ' =', np.mean(sub_dist_sw[subject_idx,ROIinds]))
		print('\n examples ', sub_dist_sw[subject_idx, ROIinds[20:25]] )
	 
		print('\n dist_sd_'+ lbl_name + '_' + subject + ' =', np.mean(sub_dist_sd[subject_idx,ROIinds]))
		print('\n examples ', sub_dist_sd[subject_idx, ROIinds[20:25]] )


		pyplot.figure(subject_idx+100)
		pyplot.title(lbl_name + 'avg_timecourse')
		pyplot.xlabel("cos_S1W2")
		pyplot.ylabel("n")
		pyplot.hist(sub_dist_sw[subject_idx, :])
		pyplot.savefig(img_path + subject + '_'+ distance_type+'_dist_sw' + '.png')
		pyplot.show()		

		pyplot.figure(subject_idx+200)
		pyplot.title(lbl_name + 'avg_timecourse')
		pyplot.xlabel("cos_S1D2")
		pyplot.ylabel("n")
		pyplot.hist(sub_dist_sd[subject_idx, :])
		pyplot.savefig(img_path + subject + '_'+ distance_type + '_dist_sd' + '.png')


	pyplot.figure(subject_idx+100)
	#pyplot.title(lbl_name + 'avg_timecourse')
	pyplot.xlabel("cos_S1W2")
	pyplot.ylabel("n")
	pyplot.hist(np.mean(sub_dist_sw, axis = 0))
	pyplot.savefig(img_path +'_'+ distance_type +'_dist_sw' + '.png')
	pyplot.show()		

	pyplot.figure(subject_idx+200)
	#pyplot.title(lbl_name + 'avg_timecourse')
	pyplot.xlabel("cos_S1D2")
	pyplot.ylabel("n")
	pyplot.hist(np.mean(sub_dist_sd, axis = 0))
	pyplot.savefig(img_path + '_' + distance_type +'_dist_sd' + '.png')

'''	t_stat, p_val = stats.ttest_rel(sub_cos_sw, sub_cos_sd, axis=0)

	t_stat_data, p_val_data = prepare_ttest_results(t_stat, p_val)

	p_val_stc = mne.SourceEstimate(p_val_data, vertices = stc_test.vertices, tmin = time_intervals[t][0], tstep = integ_ms)
	#p_val_stc.save(ttest_result.format("vec_p-val", time_lbl, lbl_name))
	p_val_stc.save(ttest_result.format("vec_p-val", time_lbls[t]))

	t_stat_stc = mne.SourceEstimate(t_stat_data, vertices = stc_test.vertices, tmin = time_intervals[t][0], tstep = integ_ms)
	#t_stat_stc.save(ttest_result.format("vec_t-stat", time_lbl, lbl_name))
	t_stat_stc.save(ttest_result.format("vec_t-stat", time_lbls[t]))'''
	






































