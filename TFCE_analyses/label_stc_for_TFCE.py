import sys
import os
import numpy as np
import mne
import os

#### funcs

def get_label_active_indices(label_filename):
	label = mne.read_label(label_filename)
	max_stc_vertex_ind = 10242
	return label.vertices[label.vertices < max_stc_vertex_ind]



### directories

#TFCE_data_path = '/net/server/data/programs/razoral/platon_pmwords/target/data_for_TFCE/normalized_sti/normalized_sti_{0}_{1}_{2}_integ5-lh.stc'
#TFCE_data_path = '/net/server/data/programs/razoral/platon_pmwords/target/data_for_TFCE/{0}_avg{1}_{2}_integ5-lh.stc'
TFCE_data_path = '/net/server/data/programs/razoral/platon_pmwords/target/data_for_TFCE/cos/{0}_cos{1}_{2}_integ5-lh.stc'
#Arkhipova_Elena_dD_226_362ms_integ5-lh.stc

#target_files_format = '/net/server/data/programs/razoral/platon_pmwords/target/data_for_TFCE/labeled/normalized_sti/normalized_sti_{0}_{1}_{2}_integ5_{3}'
#target_files_format = '/net/server/data/programs/razoral/platon_pmwords/target/data_for_TFCE/labeled/{0}_avg{1}_{2}_integ5_{3}'
target_files_format = '/net/server/data/programs/razoral/platon_pmwords/target/data_for_TFCE/labeled/cos/{0}_cos{1}_{2}_integ5_{3}'

#Arkhipova_Elena_dD_226_362ms_integ5_lbl-lh.stc

## folder with labels
lbl_path = '/net/server/data/programs/razoral/platon_pmwords/lbls/TFCE/lateral/'



### params
integ_ms = 5

subjects = [
	"Arkhipova_Elena"],
'''	"Biryukov_Aleksey",
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
	"Yarmolova_Elena"]'''

difference = ["dW", "dD"]

timings =["144_217ms", "226_362ms", "144_362ms"] # list for 5 ms it is:


file_list = os.listdir(lbl_path)
lbls_list = [lbl for lbl in file_list if '.label' in lbl]
#print('\n labels in folder:',lbls_list)


### code

for l, label in enumerate(lbls_list):

	print("\n({:2}/{:2}) preparing {}\n".format(l+1, len(lbls_list), label))	
	lbl_cur_inds = []

	lbl_cur_inds = get_label_active_indices(lbl_path+label)
	np.array(lbl_cur_inds)	
	print(len(lbl_cur_inds))
	print(lbl_cur_inds)

	lbl_name = label.replace('-lh.label', '')

	for subject_idx, subject in enumerate(subjects):
		#print("\n({:2}/{:2}) reading {}\n".format(subject_idx+1, len(subjects), subject))

		for t, timing in enumerate(timings):
			#print("\n({:2}/{:2}) reading {}\n".format(t+1, len(timings), timing))
			
			for d, difference_type in enumerate(difference):			
				masked_data = []

				stc = mne.read_source_estimate(TFCE_data_path.format(subject, difference_type, timing))
				masked_data = np.zeros(stc.data.shape)
				masked_data[lbl_cur_inds, :] = stc.data[lbl_cur_inds, :]
				
				stc_mask = []
				stc_mask = mne.SourceEstimate(data = masked_data, vertices = stc.vertices, tmin = stc.tmin, tstep = stc.tstep)
				stc_mask.save(target_files_format.format(subject, difference_type, timing, lbl_name))

				




