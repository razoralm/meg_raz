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



def calc_mah_distance_cov_by_vox(subject, time_lbl_inds, lbl_inds):

	S1 = []; W2 = []; D2 = []; S1_sample = []; S1_cov = [];

	#mah_S1_W2 = np.zeros((n_voxels))
	#mah_S1_D2 = np.zeros((n_voxels))

	mah_S1_W2 = np.zeros((len(lbl_inds)))
	mah_S1_D2 = np.zeros((len(lbl_inds)))
	#print(mah_S1_W2.shape)

	w1 = np.zeros((4, n_voxels, int(time_lbl_inds[1]-time_lbl_inds[0]))) 
	#print('w1_zeros shape: ', w1.shape)
	w2 = np.zeros((4, n_voxels, int(time_lbl_inds[1]-time_lbl_inds[0]))) 
	d1 = np.zeros((4, n_voxels, int(time_lbl_inds[1]-time_lbl_inds[0])))  
	d2 = np.zeros((4, n_voxels, int(time_lbl_inds[1]-time_lbl_inds[0])))
	
	for w_id, word in enumerate(words):
			
		stc = mne.read_source_estimate(data_path.format(subject, "passive1", word, integ_ms))
		#print('stc shape: ', stc.data.shape)
		#print('w1_lbl shape: ', stc.data[lbl_inds, :].shape)				
		w1[w_id,:,:] = stc.data[:, int(time_lbl_inds[0]):int(time_lbl_inds[1])]
			
		stc = mne.read_source_estimate(data_path.format(subject, "passive2", word, integ_ms))
		w2[w_id,:,:] = stc.data[:, int(time_lbl_inds[0]):int(time_lbl_inds[1])]

		stc = mne.read_source_estimate(data_path.format(subject, "passive1", distractors[w_id], integ_ms))
		d1[w_id,:,:] = stc.data[:, int(time_lbl_inds[0]):int(time_lbl_inds[1])]

		stc = mne.read_source_estimate(data_path.format(subject, "passive2", distractors[w_id], integ_ms))
		d2[w_id,:,:] = stc.data[:, int(time_lbl_inds[0]):int(time_lbl_inds[1])]


	S1 = np.nan_to_num(np.mean(w1+d1, axis = 0)/2)

	W2 = np.nan_to_num(np.mean(w2, axis = 0))

	D2 = np.nan_to_num(np.mean(d2, axis = 0))

##mah 
	#S12_sample = np.append(w1, np.append(d1 , np.append(w2, d2, axis = 0), axis = 0), axis = 0)
	S_sample = np.nan_to_num(np.append(w1, d1, axis = 0))

	for i, ind in enumerate(lbl_inds):
		#print(ind)				
		#print(type(ind))			

		S_cov=[]; SI =[];

		S_cov = np.abs(np.nan_to_num(np.log(np.cov(S_sample[:,int(ind),:], rowvar=False))))
		#print('\n cov_',  ind, ' = \n', np.diag(S_cov))
		print('\n cov_',  ind, ' = \n', S_cov)
	
		SI = np.linalg.inv(S_cov)
		print('\n inv_cov_',  ind, ' = \n', np.diag(SI))

		mah_S1_W2[i] = spatial.distance.mahalanobis(W2[int(ind),:], S1[int(ind),:], SI)
		
		mah_S1_D2[i] = spatial.distance.mahalanobis(D2[int(ind),:], S1[int(ind),:], SI)
		
		
	return(mah_S1_W2, mah_S1_D2)



### directoties

ttest_result = '/net/server/data/programs/razoral/platon_pmwords/target/cos/{}_mahS1W2_vs_mahS1D2_{}'

lbls_path = '/net/server/data/programs/razoral/platon_pmwords/lbls/ttest/otladka/'

img_path = '/net/server/data/programs/razoral/platon_pmwords/target/manual_ttest/144_362ms/circular_insula_check/S1_W2_D2/'

ttest_stc = '/net/server/data/programs/razoral/platon_pmwords/target/manual_ttest/144_362ms/vec_p-val_sub24_dW_vs_dD_144_362ms_integ5-lh.stc'

### params

#timings = ["144_362ms", "144_217ms", "226_362ms"]
#time_intervals = [[145, 362], [145, 217], [226, 362]] 

time_lbls = ["185_195ms"]
time_intervals = np.array([[185, 225]])


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

ROIinds = get_ttestROI_indices(lbls_path+lbls_list[0], ttest_stc, 0.9)
print(len(ROIinds))
#print(type(ROIinds))

voxels_in_an = np.arange(0,n_voxels)
#print(type(voxels_in_an))


for t, time_interval in enumerate(time_intervals):
	
	print('calulation on  ', time_lbls[t], 'interval')

	#sub_mah_sw = np.zeros((len(subjects), n_voxels))
	#sub_mah_sd = np.zeros((len(subjects), n_voxels))

	#sub_mah_sw = np.zeros((len(subjects),len(voxels_in_an)))
	#sub_mah_sd = np.zeros((len(subjects), len(voxels_in_an)))

	sub_mah_sw = np.zeros((len(subjects),len(ROIinds)))
	sub_mah_sd = np.zeros((len(subjects), len(ROIinds)))


	for subject_idx, subject in enumerate(subjects):
		print("\n\t({:2}/{:2}) processing {}\n".format(subject_idx+1, len(subjects), subject))
		
		sub_mah_sw[subject_idx,:], sub_mah_sd[subject_idx,:] = calc_mah_distance_cov_by_vox(subject, time_intervals_inds[t], ROIinds)
		
		print('\n dist_sw_'+ lbl_name + '_' + subject + ' =', np.nanmean(sub_mah_sw[subject_idx]))
		#print('\n examples ', sub_mah_sw[subject_idx, ROIinds[10:16]] )
		print('\n examples ', sub_mah_sw[subject_idx, 10:16] )
	 
		print('\n dist_sd_'+ lbl_name + '_' + subject + ' =', np.nanmean(sub_mah_sd[subject_idx]))
		#print('\n examples ', sub_mah_sd[subject_idx, ROIinds[10:16]] )
		print('\n examples ', sub_mah_sd[subject_idx, 10:16] )


'''		distance_type = 'mah'

		time_range = np.arange(time_intervals_inds[t][0], time_intervals_inds[t][1])


		pyplot.figure(subject_idx+100)
		pyplot.title(subject + 'cov_by_vox')
		pyplot.xlabel("mah_S1W2")
		pyplot.ylabel("n_vox")
		pyplot.hist(sub_mah_sw[subject_idx, :])
		pyplot.savefig(img_path + 'mah_hist/S1cov_by_vox/' + subject + '_'+ distance_type+'_dist_sw' + '.png')		

		pyplot.figure(subject_idx+200)
		pyplot.title(subject + 'cov_by_vox')
		pyplot.xlabel("mah_S1D2")
		pyplot.ylabel("n_vox")
		pyplot.hist(sub_mah_sd[subject_idx, :])
		pyplot.savefig(img_path + 'mah_hist/S1cov_by_vox/'+ subject + '_'+ distance_type + '_dist_sd' + '.png')


	pyplot.figure(subject_idx+300)
	pyplot.title('cov_by_vox')
	pyplot.xlabel("mah_S1W2")
	pyplot.ylabel("n_vox")
	pyplot.hist(np.mean(sub_mah_sw, axis = 0))
	pyplot.savefig(img_path + 'mah_hist/S1cov_by_vox/'+'voxS1_'+ distance_type +'_dist_sw' + '.png')		

	pyplot.figure(subject_idx+400)
	pyplot.title('cov_by_vox')
	pyplot.xlabel("mah_S1D2")
	pyplot.ylabel("n_vox")
	pyplot.hist(np.mean(sub_mah_sd, axis = 0))
	pyplot.savefig(img_path + 'mah_hist/S1cov_by_vox/'+ 'vox_S1' + distance_type +'_dist_sd' + '.png')


	t_stat, p_val = stats.ttest_rel(sub_mah_sw, sub_mah_sd, axis=0)

	t_stat_data, p_val_data = prepare_ttest_results(t_stat, p_val)

	p_val_stc = mne.SourceEstimate(p_val_data, vertices = stc_test.vertices, tmin = time_intervals[t][0], tstep = integ_ms)
	#p_val_stc.save(ttest_result.format("vec_p-val", time_lbl, lbl_name))
	p_val_stc.save(ttest_result.format("vec_p-val", time_lbls[t]))

	t_stat_stc = mne.SourceEstimate(t_stat_data, vertices = stc_test.vertices, tmin = time_intervals[t][0], tstep = integ_ms)
	#t_stat_stc.save(ttest_result.format("vec_t-stat", time_lbl, lbl_name))
	t_stat_stc.save(ttest_result.format("vec_t-stat", time_lbls[t]))'''
	






































