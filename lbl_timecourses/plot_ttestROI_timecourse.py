import re
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),"..", "basics"))

# from timecourse_an_config import * <--- included in calc_lbl_timecourse

from get_lbl_indices import *

from calc_lbl_timecourse import *

from matplotlib import pyplot
pyplot.switch_backend('agg')

from scipy.signal import medfilt

### directories
lbls_path = '/net/server/data/programs/razoral/platon_pmwords/lbls/ttest/325peak_lbls/'

ttest_stc = '/net/server/data/programs/razoral/platon_pmwords/target/manual_ttest/vec_ttest_on_RMS-interval/min_p-val_7frame_ttest/bin_vec_p-val_sub24_integ5_dW_vs_dD_peak325ms_integ35ms_presylvian-lh.stc'

img_path = '/net/server/data/programs/razoral/platon_pmwords/target/manual_ttest/vec_ttest_on_RMS-interval/min_p-val_7frame_ttest/325_timecourses/'


### params

th_h = 1

difference_type = "dW_dD" # "before_after" or "dW_dD" or "p1_p2"


### code

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

	a, b, d = calc_lbl_timecourse(ROIinds, difference_type)
	#print(a.shape)

	a = medfilt(a, 35)
	b = medfilt(b, 35)
	d = medfilt(d, 35)

	print('first last')
	print(len(a[41:182]))

	# plot	
	time_range = np.arange(-200, 505, integ_ms)
	print('time_range')
	print(time_range[0])
	print(time_range[-1])
	print(len(time_range))

	pyplot.figure(l)
	pyplot.title('')
	pyplot.xlabel("time [ms]")
	pyplot.ylabel("current [nA]")
	pyplot.xlim(time_range[0], time_range[-1])
	if difference_type == "before_after": 
		pyplot.plot(time_range, a, linewidth = 1, color = "b", label = "before_learning")
		pyplot.plot(time_range, b, linewidth = 1, color = "r", label = "after_learning")	
		pyplot.plot(time_range, d, linewidth = 1.5, color = "g", label = "double_difference")
	elif difference_type == "dW_dD":
		pyplot.plot(time_range, a[41:182], linewidth = 1, color = "b", label = "W1-W2")
		pyplot.plot(time_range, b[41:182], linewidth = 1, color = "r", label = "D1-D2")	
		pyplot.plot(time_range, d[41:182], linewidth = 1.5, color = "g", label = "dW-dD")
	elif difference_type == "p1_p2":
		pyplot.plot(time_range, a, linewidth = 1, color = "g", label = "S1")
		pyplot.plot(time_range, b, linewidth = 1, color = "r", label = "W2")	
		pyplot.plot(time_range, d, linewidth = 1, color = "b", label = "D2")
		pyplot.plot(time_range, b-a, linewidth = 1.5,  color = "m", label = "W2-S1")	
		pyplot.plot(time_range, d-a, linewidth = 1.5, color = "c", label = "D2-S1")
	pyplot.legend(loc = "upper right", framealpha = 0.5)
	pyplot.grid()
	pyplot.axvline(0, color="#888888")
	pyplot.axhline(0, color="#888888")
	pyplot.savefig(img_path + lbl_name + '_' + difference_type + '.png')
pyplot.show()

	


	
