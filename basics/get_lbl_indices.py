# basic operations with mne prepared labels (masking, ROI correction, etc.)


import os
import numpy as np
import mne



def get_lbl_active_indices(lbl_filename):
	
	lbl = mne.read_label(lbl_filename)
	
	max_lh_vertex_ind = 10242
	max_rh_vertex_ind = 20484

	if lbl_filename.split("-")[-1] == "rh.label":
		
		return np.array(lbl.vertices[(lbl.vertices >= max_lh_vertex_ind) & (lbl.vertices < max_rh_vertex_ind)])           
    
	elif lbl_filename.split("-")[-1] == "lh.label":
		
		#print(lbl_filename.split("-")[-2], 'active indices: ')
		#print(np.array(lbl.vertices[lbl.vertices < max_lh_vertex_ind]))
		return np.array(lbl.vertices[lbl.vertices < max_lh_vertex_ind])
   		
	else:
		print("Error")
		return 0



def get_ttestROI_indices(template_lbl, ttest_stc, th_h):

	tempROIinds = get_lbl_active_indices(template_lbl)
	#print('temp lbl :', tempROIinds)
	print('tmp lbl:', len(tempROIinds))

	stc_data = mne.read_source_estimate(ttest_stc).data
	#print(stc_data.shape)

	lbl_data = np.zeros(stc_data.shape) 

	lbl_data[tempROIinds, :] = stc_data[tempROIinds, :] 

	return np.array(np.where(abs(lbl_data) >= th_h)[0]) # <--- will work only with one frame stc !! 



def get_max_singnif_vox_ind(template_lbl, ttest_stc):

	tempROIinds = get_lbl_active_indices(template_lbl)
	#print('temp lbl :', tempROIinds)
	#print('tmp lbl:', len(tempROIinds))

	stc_data = mne.read_source_estimate(ttest_stc).data
	#print(stc_data.shape)
	#print(np.unique(stc_data))	

	lbl_data = np.zeros(stc_data.shape) 

	lbl_data[tempROIinds, :] = abs(stc_data[tempROIinds, :]) 
	#print('max_sgnf:')
	#print(max(abs(lbl_data)))
	return np.array(np.where(lbl_data == max(lbl_data))[0]) # <--- will work only with one frame stc !! 



def merge_lbls_indices(lbls_path):
	
	lbls_list = [lbl for lbl in os.listdir(lbls_path) if '.label' in lbl]
	print('\n labels in folder: ', len(lbls_list))
	print('\n labels : \n', len(lbls_list))

	merged_lbls_inds = []																			

	for l, lbl in enumerate(lbls_list):

		cur_inds = get_label_active_indices(lbls_path+lbl)

		merged_lbls_inds = np.concatenate((merged_lbls_inds, cur_inds)).astype(int)

	return np.unique(merged_lbls_inds)



def subtract_2lbls_indices(lbl, sub_lbl):
	
	tempROIinds = get_lbl_active_indices(lbl)
	
	subROIinds = get_lbl_active_indices(sub_lbl)

	return np.delete(tempROIinds, np.where(np.ind1d(tempROIinds, subROIinds)))


