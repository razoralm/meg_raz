# prepare labeled data within time interval(s) for 3dTFCE (time_cut and labele applycation realised simultaneously) thus the output can be used as input for TFCE

import sys
import os

import numpy as np
import mne

from scipy import stats
from stc_vec_ttest import *
from calc_time_indices import *

from scipy import stats


### directories

#Arkhipova_Elena_passive1_hicha_integ5-lh
data_path = '/net/server/data/programs/razoral/platon_pmwords/target/stc-basecorr/{0}_{1}_{2}_integ5-lh.stc'
ttest_result = '/data/programs/razoral/platon_pmwords/target/manual_ttest/{0}/vec_{1}_sub24_W_vs_D_{2}_{3}_integ5'


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

distractors = ["hichu", "hisha", "hisu", "hiva"]

#difference = ["dW", "dD"]
difference = ["passive1", "passive2"]


## !! change for only one long interval 0-600
time_lbls = ['144_217ms','226_362ms','144_362ms']# list for 5 ms 
time_intervals = np.array([[145, 217], [226, 362], [145, 362]]) 



###code

# stc initialization
stc_test = mne.read_source_estimate(data_path.format(subjects[0], difference[0], words[0]))

time_intervals_inds = calc_time_indices(time_intervals, data_path.format(subjects[0], difference[0], words[0]), integ_ms)


for t, time_lbl in enumerate(time_lbls):
#print("\n({:2}/{:2}) time_cut {}\n".format(t+1, len(time_lbls), time_lbl))
	
	t_min = int(time_lbl[0:3])	
		
	for d, difference_type in enumerate(difference):	
			
		w_per_sub = np.zeros(shape=(len(subjects), stc_test.data.shape[0]))
		d_per_sub = np.zeros(shape=(len(subjects), stc_test.data.shape[0]))

		for subject_idx, subject in enumerate(subjects):
			print("\n({:2}/{:2}) sub {}\n".format(subject_idx+1, len(subjects), subject))

			for w, word in enumerate(words):
				#print("\n({:2}/{:2}) word {}\n".format(w, len(words), word))

				stc = mne.read_source_estimate(data_path.format(subject, difference_type, word))
				w =+ stc.data[:,time_intervals_inds[t][0]:time_intervals_inds[t][1]]
			
			w_per_sub[subject_idx,:] = np.mean(w, axis=1)/len(words)	

			for d, distractor in enumerate(distractors):
				stc_data = []
				
				stc = mne.read_source_estimate(data_path.format(subject, difference_type, distractor))
				d =+ stc.data[:,time_intervals_inds[t][0]:time_intervals_inds[t][1]]
			
			d_per_sub[subject_idx,:] = np.mean(d, axis=1)/len(words)

			t_stat_data, p_val_data = stc_vec_ttest(w_per_sub, d_per_sub)

			p_val_stc = mne.SourceEstimate(p_val_data, vertices = stc_test.vertices, tmin = t_min, tstep = 0.005)
			p_val_stc.save(ttest_result.format(time_lbl, "p-val", difference_type, time_lbl))

			t_stat_stc = mne.SourceEstimate(t_stat_data, vertices = stc_test.vertices, tmin = t_min, tstep = 0.005)
			t_stat_stc.save(ttest_result.format(time_lbl, "t-stat", difference_type, time_lbl))





