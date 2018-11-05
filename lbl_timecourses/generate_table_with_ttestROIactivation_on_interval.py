import re
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),"..", "basics"))

from timecourse_an_config import * # <--- included in calc_lbl_timecourse

from calc_time_indices import *
from get_lbl_indices import*

from calc_lbl_timecourse import *


### params
activation_type = 'voxel with max significance within ROI'
#activation_type = 'averaged within ROI'

th_h = 1

time_lbls = ["190ms_integ35", "265ms_integ35", "325ms_integ35" ]
time_intervals = np.array([[180, 205], [255, 280],[315, 340]]) # 35 msaround peaks 

if activation_type == 'averaged within ROI':

	print('MODE: ', activation_type)

	### directories
	lbls_path = '/net/server/data/programs/razoral/platon_pmwords/lbls/ttest/190peak_lbls/'

	ttest_stc = '/net/server/data/programs/razoral/platon_pmwords/target/manual_ttest/vec_ttest_on_RMS-interval/min_p-val_7frame_ttest/bin_vec_p-val_sub24_integ5_dW_vs_dD_peak190ms_integ35ms_presylvian-lh.stc'

	table_path = '/net/server/data/programs/razoral/platon_pmwords/target/ROI_source-space_timecourses/190peak_lbls'
	os.makedirs(table_path, exist_ok=True)



	### code

	time_intervals_inds = calc_time_indices(time_intervals, data_path.format(subjects[0], "passive1", words[0], integ_ms ), integ_ms)


	lbls_list = [lbl for lbl in os.listdir(lbls_path) if '.label' in lbl]
	print('\n labels in folder: ', len(lbls_list))
	print('\n labels :')
	for i in range(0, len(lbls_list)):
		print('\n', str(i+1)+'.', lbls_list[i])
	

	for l, lbl in enumerate(lbls_list):

		lbl_name = re.sub('-[lr]h.label', '', lbl)
		print('\n', lbl_name)

		ROIinds = get_ttestROI_indices(lbls_path+lbl, ttest_stc, th_h)
		print(len(ROIinds))
		#print(ROIinds)

		for t, time_lbl in enumerate(time_lbls):

			table_lbl_time_avg_by_sub(ROIinds, lbl_name, time_intervals_inds[t], time_lbl, table_path)

elif activation_type == 'voxel with max significance within ROI':
	### directories

	print('\n MODE: ', activation_type)

	lbls_path = '/net/server/data/programs/razoral/platon_pmwords/lbls/ttest/325peak_lbls/'
	
	#!
	ttest_stc = '/net/server/data/programs/razoral/platon_pmwords/target/manual_ttest/vec_ttest_on_RMS-interval/min_p-val_7frame_ttest/vec_p-val_sub24_integ5_dW_vs_dD_peak325ms_integ35ms_presylvian-lh.stc'

	table_path = '/net/server/data/programs/razoral/platon_pmwords/target/ROI_source-space_timecourses/325peak_lbls'
	os.makedirs(table_path, exist_ok=True)



	### code

	time_intervals_inds = calc_time_indices(time_intervals, data_path.format(subjects[0], "passive1", words[0], integ_ms ), integ_ms)


	lbls_list = [lbl for lbl in os.listdir(lbls_path) if '.label' in lbl]
	print('\n labels in folder: ', len(lbls_list))
	print('\n labels :')
	for i in range(0, len(lbls_list)):
		print('\n', str(i+1)+'.', lbls_list[i])
	

	for l, lbl in enumerate(lbls_list):

		lbl_name = re.sub('-[lr]h.label', '', lbl)
		print('\n', lbl_name)

		vox_ind = get_max_singnif_vox_ind(lbls_path+lbl, ttest_stc)
		print('\n vox_ind:')
		print(vox_ind)
		
		for t, time_lbl in enumerate(time_lbls):

			table_max_significace_voxel_time_avg_by_sub(vox_ind, lbl_name, time_intervals_inds[t], time_lbl, table_path)

else:

	print('What do you want from me?')


	


	
