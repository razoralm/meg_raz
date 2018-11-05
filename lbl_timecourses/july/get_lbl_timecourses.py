import sys
import os
import numpy as np
import mne
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot

#from plot_stat_comparison import *
#from tfce import tfce_1d

#### funcs
def get_label_active_indices(label_filename):
	label = mne.read_label(label_filename)
	max_stc_vertex_ind = 10242
	return label.vertices[label.vertices<max_stc_vertex_ind]

#### params
subjects = [
	"Arkhipova_Elena",
	"Biryukov_Aleksey",
	"Budulev_Nikita",
	"Filimonov_Rodion",
	"Galyuta_Ilia",
	"Gniteeva_Lyudmila",
	"Goyaeva_Dzerassa",
	"Kovalev_Dmitriy",
	"Kozlov_Alexey",
	"Lashkov_Andrey",
	"Lomakin_Dmitriy",
	"Masleniy_Evgeniy",
	"Nazarova_Maria",
	"Rekubratskiy_Vitaliy",
	"Shaballin_Konstantin",
	"Shulga_Kirill",
	"Skokova_Julia",
	"Skovorodko_Olga",
	"Slobodskoy_Yaroslav",
	"Spiridonov_Arseniy",
	"Timonov_Evgeniy",
	"Trufanova_Zhenya",
	"Vlasova_Roza",
	"Yarmolova_Elena"
]

words = ["hicha", "hishu", "hisa", "hivu"]
distractors = ["hichu", "hisha", "hisu", "hiva"]

timecourse_type = ["dW-dD"]

n_voxels = 20484

tmin = -410
tmax = 615
time_length = tmax - tmin

integ_ms = 5

img_path = '/data/programs/razoral/platon_pmwords/target/ROI_source-space_timecourses/'
																	   # Arkhipova_Elena_dD_0_600ms_integ5-lh.stc
target_files_format = "/net/server/data/programs/razoral/platon_pmwords/target/data_for_TFCE/{}_{}__integ5-lh.stc"
stc_test = mne.read_source_estimate(target_files_format.format(subjects[0], "dW"))

dW = np.zeros((len(subjects), stc_test.data.shape[1]))
dD = np.zeros((len(subjects), stc_test.data.shape[1]))


## folders with labels
lbls_path = '/data/programs/razoral/platon_pmwords/lbls/{}'

#lbls_type = ["ttest","alena", "HP", "Kimpa", "test_lbls"] cycle??
lbls_type =  "TFCE/lateral/hide/"
label_path = lbls_path.format(lbls_type)


save_timecourse_in = "/net/server/data/programs/razoral/platon_pmwords/target/ROI_source-space_timecourses/"
os.makedirs(save_timecourse_in, exist_ok=True)



file_list = os.listdir(label_path)
lbls_list = [lbl for lbl in file_list if '.label' in lbl]
#print('\n labels in folder:',lbls_list)


for l, label in enumerate(lbls_list):

	print("\n({:2}/{:2}) preparing {}\n".format(l+1, len(lbls_list), label))	

	lbl_cur_inds = get_label_active_indices(label_path+label)

	lbl_name = label.replace('.label', '')

	for subject_idx, subject in enumerate(subjects):
		print("\n({:2}/{:2}) reading {}\n".format(subject_idx+1, len(subjects), subject))

		w_stc = mne.read_source_estimate(target_files_format.format(subject, "dW"))
		d_stc = mne.read_source_estimate(target_files_format.format(subject, "dD"))

		dW[subject_idx,:] = np.mean(w_stc.data[lbl_cur_inds,:], axis=0)
		dD[subject_idx,:] = np.mean(d_stc.data[lbl_cur_inds,:], axis=0)
	
	np.save(save_timecourse_in+lbl_name+"_dW",dW)
	np.save(save_timecourse_in+lbl_name+"_dD",dD)

	# save double-difference mean comparison plot with tfce significance
	
	time_range = np.arange(tmin, tmax, integ_ms)

	pyplot.figure(l)
	pyplot.title('check '+lbl_name)
	pyplot.xlabel("time [ms]")
	pyplot.ylabel("avg_intensity")
	pyplot.xlim(tmin, tmax-integ_ms)
	pyplot.plot(time_range, np.mean(dW, axis=0), linewidth = 1, color = "b", label = "before_learning")
	pyplot.plot(time_range, np.mean(dD, axis=0), linewidth = 1, color = "r", label = "after_learning")	
	pyplot.plot(time_range, np.mean(dW-dD, axis=0), linewidth = 1.5, color = "g", label = "double_difference")
	pyplot.legend(loc = "upper right", framealpha = 0.5)
	pyplot.grid()
	pyplot.axvline(0, color="#888888")
	pyplot.axhline(0, color="#888888")
	pyplot.savefig(img_path + lbl_name + 'integ5_control.png')
	
pyplot.show()
	


		


	
	

