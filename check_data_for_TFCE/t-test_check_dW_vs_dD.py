import sys
import os
import numpy
import mne
from scipy import stats

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

#timings = ["226_362ms"] 	  # list 					  for 5 ms it is:
#time_intervals = [226, 362]

integ_ms = 5

target_files_format = "/data/programs/razoral/platon_pmwords/target/data_for_TFCE/{}_{}_{}_integ5-lh.stc" 
																							# name_differenceType_timeInterval_integ[-hemisphere.stc]-auto
save_result_format = "/data/programs/razoral/platon_pmwords/target/manual_ttest/data_for_TFCE_check/{}_{}_integ5_{}"
																							# StatisticsType_nSub_timeInterval_integ[-hemisphere.stc]-auto
#time_length = 26
t_len = 205

n_voxels = 20484

stc1 = mne.read_source_estimate(target_files_format.format(subjects[0], "dW", ''))

dw_per_sub = numpy.zeros(shape=(len(subjects), n_voxels, t_len))
dd_per_sub = numpy.zeros(shape=(len(subjects), n_voxels, t_len))

for subject_idx, subject in enumerate(subjects):
	print("({:2}/{:2}) reading {}".format(subject_idx+1, len(subjects), subject))
		
	dW_stc = mne.read_source_estimate(target_files_format.format(subjects[subject_idx], "dW", ''))
	dw_per_sub[subject_idx,:,:] = dW_stc.data 

	dD_stc = mne.read_source_estimate(target_files_format.format(subjects[subject_idx], "dD", ''))
	dd_per_sub[subject_idx,:,:] = dD_stc.data

t_stat, p_val = stats.ttest_rel(dw_per_sub, dd_per_sub, axis=0)
  
# STC Viewer normalisation
t_sign = numpy.sign(t_stat)
p_val_inv = numpy.multiply((1 - p_val), t_sign)

t_stat_stc = mne.SourceEstimate(t_stat, vertices = stc1.vertices, tmin = stc1.tmin, tstep = stc1.tstep)
p_val_stc = mne.SourceEstimate(p_val_inv, vertices = stc1.vertices, tmin = stc1.tmin, tstep = stc1.tstep)

t_stat_stc.save(save_result_format.format("t-stat", subject_idx+1, ''))
p_val_stc.save(save_result_format.format("p-val", subject_idx+1, ''))

