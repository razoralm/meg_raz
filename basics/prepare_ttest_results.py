import numpy as np
import mne

def prepare_ttest_results(t_stat, p_val):

#p_val inversion for STC Viewer
	p_val = 1-p_val


	#binarize p_val
	#p_val[p_val < 0.95] = 0 # significance threshold
	#p_val[p_val > 0.95] = 1
	#print('p_val_threshold')
	#print(p_val[26])
	#print(p_val[1])
	#print('\n')


	# get rid of nans
	t_stat = np.nan_to_num(t_stat)
	p_val = np.nan_to_num(p_val)

	#p_val sign assertion
	p_val = p_val*np.sign(t_stat)

	p_val_data = np.array([p_val]).T
	t_stat_data = np.array([t_stat]).T

	return(t_stat_data, p_val_data)
