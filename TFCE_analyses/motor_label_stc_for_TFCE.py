# prepare labeled data within time interval(s) for 3dTFCE (time_cut and labele applycation realised simultaneously) thus the output can be used as input for TFCE

import sys
import os
import numpy as np
import mne
import os

#### funcs

## caution - applicable for lh only!
def get_label_active_indices(label_filename):
	label = mne.read_label(label_filename)
	max_stc_vertex_ind = 10242
	return label.vertices[label.vertices<max_stc_vertex_ind]



### directories

#TFCE_data_path = '/net/server/data/programs/razoral/platon_pmwords/target/data_for_TFCE/{0}_{1}_{2}_integ5-lh.stc'
#Arkhipova_Elena_dD_226_362ms_integ5-lh.stc
#
## changed for raw data
#Arkhipova_Elena_passive1_hicha_integ5-lh
TFCE_data_path = '/net/server/data/programs/razoral/platon_pmwords/target/stc-basecorr/{0}_{1}_{2}_integ5-lh.stc'

target_files_format = '/net/server/data/programs/razoral/platon_pmwords/target/data_for_TFCE/labeled/motor_smtp_an/test/{0}_{1}_{2}_{3}_integ5_{4}-lbl'
#Arkhipova_Elena_passive1_hicha_lblhicha_integ5-lh.stc


## folder with labels 
## changed for motor_smtp
lbl_path = '/net/server/data/programs/razoral/platon_pmwords/lbls/motor_smtp/'

file_list = os.listdir(lbl_path)
lbls_list = [lbl for lbl in file_list if '.label' in lbl]
#print('\n labels in folder:',lbls_list)



### params

integ_ms = 5


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
	"Yarmolova_Elena"]


words = ['hicha','hishu','hisa','hivu']


#difference = ["dW", "dD"]
difference = ["passive1", "passive2"]


## !! change for only one long interval 0-600
timings =["200_400ms"] # list for 5 ms 

time_intervals = np.array([[200, 400]]) 

#kostil: time intervals recalculation in indeces
######################################################################################################################
time_intervals_inds = np.zeros(shape = time_intervals.shape)
#print ('time_intervals_inds', time_intervals_inds)	

# stc initialization
stc1 = mne.read_source_estimate(TFCE_data_path.format(subjects[0], difference[0], words[0]))
#print(stc1.data.shape)
#print(stc1.tmin, stc1.tstep)
ambg_ind = int(abs(stc1.tmin//stc1.tstep))
print("ambg_point: %s" % (ambg_ind))


for timing_idx, time_interval in enumerate(time_intervals):
	print("\n({:2}/{:2}) calculate indeces for {} \n".format(timing_idx+1, len(time_intervals), timings[timing_idx]))

	t0 = int(time_interval[0]//integ_ms)#+1
	print("t0_int: %s" % (t0))
	t1 = int((time_interval[1]//integ_ms))
	print("t1_int: %s" % (t1))
	dt = int(t1 - t0)
	print("dt: %s\n" % (dt))
		
	t0_ambg = int(ambg_ind + t0)
	print("t0_ambg: %s" % (t0_ambg))
	t1_ambg = int(ambg_ind + t1)
	print("t1_ambg: %s" % (t1_ambg))
	
	time_intervals_inds[timing_idx][:] = [t0_ambg, t1_ambg] # numpy array?

print ('time intervals inds', time_intervals_inds)



###code

for l, label in enumerate(lbls_list):

	print("\n({:2}/{:2}) preparing {}\n".format(l+1, len(lbls_list), label))	
	lbl_cur_inds = []

	lbl_cur_inds = get_label_active_indices(lbl_path+label)
	np.array(lbl_cur_inds)	
	print(len(lbl_cur_inds))
	print(lbl_cur_inds)

	lbl_name = label.replace('-lh.label', '')

	

	for subject_idx, subject in enumerate(subjects):
		print("\n({:2}/{:2}) sub {}\n".format(subject_idx+1, len(subjects), subject))

		for t, timing in enumerate(timings):
			#print("\n({:2}/{:2}) time_cut {}\n".format(t+1, len(timings), timing))
			
			for d, difference_type in enumerate(difference):	

				for w, word in enumerate(words):
					#print("\n({:2}/{:2}) word {}\n".format(w, len(words), word))
					stc_mask = []
					masked_data = []
					stc_data = []

					stc = mne.read_source_estimate(TFCE_data_path.format(subject, difference_type, word))
					stc_data = stc.data[:,time_intervals_inds[t][0]:time_intervals_inds[t][1]]

					masked_data = np.zeros(stc_data.shape)
					masked_data[lbl_cur_inds, :] = stc_data[lbl_cur_inds, :]
				
					
					stc_mask = mne.SourceEstimate(data = masked_data, vertices = stc.vertices, tmin = time_intervals[t][0]/1000, tstep = stc.tstep)
					stc_mask.save(target_files_format.format(subject, difference_type, word, timing,lbl_name))
# check
'''print(masked_data.shape)
print(masked_data[5,0:100])
print(masked_data[1,-100:-1])
print(np.unique(np.nonzero(masked_data)[0]))
print(lbl_cur_inds)
print(len(np.unique(np.nonzero(masked_data)[0]))==len(lbl_cur_inds))'''

				




