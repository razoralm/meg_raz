import numpy
from array import array
import subprocess
import random
import os
import pickle
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
	"Yarmolova_Elena"]


TFCE_data_path = '/net/server/data/programs/razoral/platon_pmwords/target/data_for_TFCE/labeled/{0}_{1}_{2}_{3}_integ5-lh.stc'

time_lbl = '144_217ms'
lbl_name = 'inf_operculum'

stc_test = mne.read_source_estimate(TFCE_data_path.format(subjects[0], "dD",  time_lbl, lbl_name))
s = stc_test.data.shape

dw_per_sub = numpy.zeros(shape=(len(subjects), s[0], s[1]))
dd_per_sub = numpy.zeros(shape=(len(subjects), s[0], s[1]))

for subject_idx, subject in enumerate(subjects):

	stc_d = mne.read_source_estimate(TFCE_data_path.format(subject, 'dD', time_lbl, lbl_name))
	print('dD')
	print(stc_d.data[26,:])
	print(stc_d.data[1,:])
	print('\n')
	dd_per_sub[subject_idx,:,:] = (stc_d.data)
		

	stc_w = mne.read_source_estimate(TFCE_data_path.format(subject, 'dW', time_lbl, lbl_name))
	print('dW')	
	print(stc_w.data[26,:])
	print(stc_w.data[1,:])
	print('\n')
	dw_per_sub[subject_idx,:,:] = (stc_w.data)	

	stc_d = []
	stc_w = []

t_stat, p_val = stats.ttest_rel(dw_per_sub, dd_per_sub, axis=0)
print('t-stat')
print(t_stat[26,:])
print(t_stat[1,:])
print('\n')

print('p-val')
print(p_val[26,:])
print(p_val[1,:])
print('\n')



