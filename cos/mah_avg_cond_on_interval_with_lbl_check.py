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

def calc_mah_distance(X, S, inv_covS):
# X, S - matrices, shape(20K,time_interval_len) >> vectorized operation
	mah = np.zeros((n_voxels))	
	for i in range(0, n_voxels):
		mah[i] = spatial.distance.mahalanobis(X[i,:], S[i, :], inv_covS)
	return(mah)



def calc_S1_W2_D2_IcovS(time_lbl_inds):

	S1 = []; W2 = []; D2 = []; S1_sample = []; S1_cov = [];

	mah_S1_W2 = np.zeros((n_voxels))
	mah_S1_D2 = np.zeros((n_voxels))

	w1 = np.zeros((4, n_voxels, int(time_lbl_inds[1]-time_lbl_inds[0]))) 
	#print('w1_zeros shape: ', w1.shape)
	w2 = np.zeros((4, n_voxels, int(time_lbl_inds[1]-time_lbl_inds[0]))) 
	d1 = np.zeros((4, n_voxels, int(time_lbl_inds[1]-time_lbl_inds[0])))  
	d2 = np.zeros((4, n_voxels, int(time_lbl_inds[1]-time_lbl_inds[0])))
	
	for w_id, word in enumerate(words):
			
		stc = mne.read_source_estimate(grand_avg.format("passive1", word, integ_ms))
		#print('stc shape: ', stc.data.shape)
		#print('w1_lbl shape: ', stc.data[lbl_inds, :].shape)				
		w1[w_id,:,:] = stc.data[:, int(time_lbl_inds[0]):int(time_lbl_inds[1])]
			
		stc = mne.read_source_estimate(grand_avg.format("passive2", word, integ_ms))
		w2[w_id,:,:] = stc.data[:, int(time_lbl_inds[0]):int(time_lbl_inds[1])]

		stc = mne.read_source_estimate(grand_avg.format("passive1", distractors[w_id], integ_ms))
		d1[w_id,:,:] = stc.data[:, int(time_lbl_inds[0]):int(time_lbl_inds[1])]

		stc = mne.read_source_estimate(grand_avg.format("passive2", distractors[w_id], integ_ms))
		d2[w_id,:,:] = stc.data[:, int(time_lbl_inds[0]):int(time_lbl_inds[1])]


	S1 = np.mean(w1+d1, axis = 0)/2
	print(S1.shape)
	W2 = np.mean(w2, axis = 0)
	print(W2.shape)
	D2 = np.mean(d2, axis = 0)
	print(D2.shape)
############# mah 
	
	# var1
	#S1_sample = np.reshape(np.append(w1, d1, axis = 0), (n_voxels*8, S1.shape[1]))
	#S1_cov = np.cov(S1_sample, rowvar=False)
	
	#var2
	#S1_sample = np.append(w1, np.append(d1 , np.append(w2, d2, axis = 0), axis = 0), axis = 0)
	#S1_cov = np.cov(np.reshape(S1_sample, (n_voxels*16, S1.shape[1])), rowvar=False)
	#print(S1_cov.shape)

	#var3
	S1_sample = np.append(S1, np.append(W2, D2, axis = 0), axis = 0)
	#print(S1_sample.shape)
	S1_cov = np.cov(S1_sample, rowvar=False)

	#var4
	#S1_sample = S1
	#S1_cov = np.cov(S1_sample, rowvar=False)

	SI = np.linalg.inv(S1_cov) 
		
	return(S1, W2, D2, SI, w1, d1, w2, d2)


### directoties

ttest_result = '/net/server/data/programs/razoral/platon_pmwords/target/cos/{}_mahS1W2_vs_mahS1D2_{}'

lbls_path = '/net/server/data/programs/razoral/platon_pmwords/lbls/ttest/otladka/'

img_path = '/net/server/data/programs/razoral/platon_pmwords/target/manual_ttest/144_362ms/circular_insula_check/S1_W2_D2/'

table_path = '/net/server/data/programs/razoral/platon_pmwords/target/cos/mah_tables/'

### params

#timings = ["144_362ms", "144_217ms", "226_362ms"]
#time_intervals = [[145, 362], [145, 217], [226, 362]] 

time_lbls = ["144_362ms"]
time_intervals = np.array([[145, 362]])


### code

stc_test = mne.read_source_estimate(data_path.format(subjects[0], "passive1", words[0], integ_ms ))


time_intervals_inds = calc_time_indices(time_intervals, data_path.format(subjects[0], "passive1", words[0], integ_ms ), integ_ms)


lbls_list = [lbl for lbl in os.listdir(lbls_path) if '.label' in lbl]
print('\n labels in folder: ', len(lbls_list))
print('\n labels :')
for i in range(0, len(lbls_list)):
	print('\n', str(i+1)+'.', lbls_list[i])
	




for t, time_interval in enumerate(time_intervals):
	
	print('calulations performed in  ', time_lbls[t])


	S1, W2, D2, SI, w1, d1, w2, d2 = calc_S1_W2_D2_IcovS(time_intervals_inds[t])
		
		
	mah_sw = calc_mah_distance(W2, S1, SI)
	mah_sd = calc_mah_distance(D2, S1, SI)
	

	mah = mne.SourceEstimate(np.array([mah_sw-mah_sd]).T, vertices = stc_test.vertices, tmin = time_intervals[t][0], tstep = integ_ms)
	#p_val_stc.save(ttest_result.format("vec_p-val", time_lbl, lbl_name))
	mah.save(ttest_result.format("mah_avg", time_lbls[t]))

	

'''	mah_s1 = np.zeros((8, 8, n_voxels))
	mah_s2 = np.zeros((8, 8, n_voxels))
		
	stim1 = np.append(w1, d1, axis = 0)
	stim2 = np.append(w2, d2, axis = 0)
	print('stim1_shape', stim1.shape)

	for i in range(0,8):
		for j in range(0,8):
			mah_s1[i,j,:] = calc_mah_distance(stim1[i,:], stim1[j,:], SI)
			mah_s2[i,j,:] = calc_mah_distance(stim2[i,:], stim2[j,:], SI)


	for l, lbl in enumerate(lbls_list):
		lbl_name = re.sub('-[lr]h.label', '', lbls_list[l])
		print('\n calculating', lbl_name)

		ROIinds = get_lbl_active_indices(lbls_path+lbls_list[l])
		print('\n len(lbl) = ', len(ROIinds))

		lbl_mah_sw = np.nanmean(mah_sw[ROIinds])
		lbl_mah_sd = np.nanmean(mah_sd[ROIinds])

		lbl_mah_s1 = np.zeros((8,8))
		lbl_mah_s2 = np.zeros((8,8))
			
		for i in range(0,8):
			for j in range(0,8):
				lbl_mah_s1[i,j] = np.nanmean(mah_s1[i,j, ROIinds])
				lbl_mah_s2[i,j] = np.nanmean(mah_s2[i,j, ROIinds])
	
	###form tables
		os.makedirs(table_path, exist_ok=True)

		f = open(table_path+"var1_{}_{}_{}.tsv".format(time_lbls[t], lbl_name, "passive1"), 'w+')
		f.write("stimul")
		for sti in stims:
			f.write("\t{0}_passive1".format(sti))
		f.write("\n")
		for sti_ind, sti in enumerate(stims):
			f.write("{}".format(sti))
			for i in range(0,8):
				f.write("\t{:e}".format(lbl_mah_s1[sti_ind, i]))
			f.write("\n")
		f.write("\n\n mah_sw = {:e}".format(lbl_mah_sw))		
		f.write("\n\n mah_sd = {:e}".format(lbl_mah_sd))	
		f.close()


		f = open(table_path+"var1_{}_{}_{}.tsv".format(time_lbls[t], lbl_name, "passive2"), 'w+')
		f.write("stimul")
		for sti in stims:
			f.write("\t{0}_passive2".format(sti))
		f.write("\n")
		for sti_ind, sti in enumerate(stims):
			f.write("{}".format(sti))
			for i in range(0,8):
				f.write("\t{:e}".format(lbl_mah_s2[sti_ind, i]))
			f.write("\n")
		f.write("\n\n mah_sw = {:e}".format(lbl_mah_sw))		
		f.write("\n\n mah_sd = {:e}".format(lbl_mah_sd))		
		f.close()'''


	





































