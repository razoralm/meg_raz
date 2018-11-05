import re
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),"..", "basics"))

# from timecourse_an_config import * <--- included in calc_lbl_timecourse

from get_lbl_indices import *

from calc_lbl_timecourse import *

from matplotlib import pyplot


### directories
lbls_path = '/data/programs/razoral/platon_pmwords/lbls/ttest/otladka/'

ttest_stc = '/data/programs/razoral/platon_pmwords/target/manual_ttest/144_362ms/vec_p-val_sub24_dW_vs_dD_144_362ms_integ5-lh.stc'

img_path = '/data/programs/razoral/platon_pmwords/target/manual_ttest/144_362ms/new_script_check/'


### params

th_h = 0.9

sessions = ["passive1", "passive2"]


### code

lbls_list = [lbl for lbl in os.listdir(lbls_path) if '.label' in lbl]
print('\n labels in folder: ', len(lbls_list))
'''print('\n labels :')
for i in range(0, len(lbls_list)):
	print('\n', str(i+1)+'.', lbls_list[i])'''
	

for l, lbl in enumerate(lbls_list):

	lbl_name = re.sub('-[lr]h.label', '', lbl)
	print('\n', lbl_name)

	ROIinds = get_ttestROI_indices(lbls_path+lbl, ttest_stc, th_h)
	print(len(ROIinds))
	#print(ROIinds)

	plot_lbl_timecourse_by_sub(ROIinds, lbl_name, sessions[1], img_path)
	
