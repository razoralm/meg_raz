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


TFCE_data_path = '/net/server/data/programs/razoral/platon_pmwords/target/data_for_TFCE/labeled/normalized_sti/normalized_sti_{0}_{1}_{2}_integ5_{3}-lh.stc'

ttest_result = '/net/server/data/programs/razoral/platon_pmwords/target/manual_ttest/{}_sub24_normalized_sti_dW_vs_dD_{}_integ5_{}'

#time_lbl = '144_217ms'
#time_lbl = '226_362ms'
time_lbl = '144_362ms'

lbl_name = 'presylvian'

stc_test = mne.read_source_estimate(TFCE_data_path.format(subjects[0], "dD",  time_lbl, lbl_name))
s = stc_test.data.shape

dw_per_sub = numpy.zeros(shape=(len(subjects), s[0]))
dd_per_sub = numpy.zeros(shape=(len(subjects), s[0]))

for subject_idx, subject in enumerate(subjects):

	stc_d = mne.read_source_estimate(TFCE_data_path.format(subject, 'dD', time_lbl, lbl_name))
	#print('dD')
	#print(stc_d.data[26,:])
	#print(stc_d.data[1,:])
	#print('\n')
	dd_per_sub[subject_idx,:] = numpy.mean(stc_d.data, axis=1)
		

	stc_w = mne.read_source_estimate(TFCE_data_path.format(subject, 'dW', time_lbl, lbl_name))
	#print('dW')	
	#print(stc_w.data[26,:])
	#print(stc_w.data[1,:])
	#print('\n')
	dw_per_sub[subject_idx,:] = numpy.mean(stc_w.data, axis=1)	

	stc_d = []
	stc_w = []

t_stat, p_val = stats.ttest_rel(dw_per_sub, dd_per_sub, axis=0)
print('p_val')
print(p_val[26])
print(p_val[1])
print('\n')

#p_val inversion for STC Viewer
p_val = 1-p_val
print('1-p_val')
print(p_val[26])
print(p_val[1])
print('\n')

#binarize p_val
#p_val[p_val < 0.95] = 0 # significance threshold
#p_val[p_val > 0.95] = 1
#print('p_val_threshold')
#print(p_val[26])
#print(p_val[1])
#print('\n')

# get rid of nans
t_stat = numpy.nan_to_num(t_stat)
p_val = numpy.nan_to_num(p_val)

#p_val sign assertion
t_sign = numpy.sign(t_stat)
p_val_signed = numpy.multiply(p_val, t_sign)
print('p_val_signed')
print(p_val_signed[26])
print(p_val_signed[1])
print('\n')

#p_val_integ = numpy.sum(p_val_signed, axis =1)
#print('p_val_integ')
#print(p_val_integ.shape)

#p_val_stc = mne.SourceEstimate(p_val_signed.T, vertices = stc_test.vertices)
#p_val_stc.save(ttest_result.format("vec_p-val", time_lbl, lbl_name))	

print('\n')
frame = numpy.zeros(p_val_signed.shape)

p_val_data = numpy.array([p_val_signed, frame])
print(p_val_data.T)

p_val_stc = mne.SourceEstimate(p_val_data.T, vertices = stc_test.vertices, tmin = 0.144, tstep = 0.073)
p_val_stc.save(ttest_result.format("vec_p-val", time_lbl, lbl_name))

	
