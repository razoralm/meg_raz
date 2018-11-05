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


TFCE_data_path = '/net/server/data/programs/razoral/platon_pmwords/target/data_for_TFCE/{0}_{1}_{2}_integ5-lh.stc'

#ttest_result = '/net/server/data/programs/razoral/platon_pmwords/target/manual_ttest/{}_sub24_dW_vs_dD_{}_integ5'
ttest_result = '/net/server/data/programs/razoral/platon_pmwords/target/data_for_TFCE/{0}_avg{1}_{2}_integ5'


time_lbls = ['144_217ms','226_362ms','144_362ms']

#lbl_name = 'presylvian'

for time_lbl in time_lbls:

	stc_test = mne.read_source_estimate(TFCE_data_path.format(subjects[0], "dD",  time_lbl))
	s = stc_test.data.shape

	t_min = int(time_lbl[0:3])

	dw_per_sub = numpy.zeros(shape=(len(subjects), s[0]))
	dd_per_sub = numpy.zeros(shape=(len(subjects), s[0]))

	for subject_idx, subject in enumerate(subjects):

		dd_per_sub = []
		dw_per_sub = []

		stc_d = mne.read_source_estimate(TFCE_data_path.format(subject, 'dD', time_lbl))
		dd_per_sub = numpy.array([numpy.mean(stc_d.data, axis=1)]).T
		print(dd_per_sub.shape)

		dd_vec_stc = mne.SourceEstimate(dd_per_sub, vertices = stc_test.vertices, tmin = t_min, tstep = 0.005)
		dd_vec_stc.save(ttest_result.format(subject, 'dD', time_lbl))
				

		stc_w = mne.read_source_estimate(TFCE_data_path.format(subject, 'dW', time_lbl))
		dw_per_sub = numpy.array([numpy.mean(stc_w.data, axis=1)]).T	
		print(dw_per_sub.shape)		

		dw_vec_stc = mne.SourceEstimate(dw_per_sub, vertices = stc_test.vertices, tmin = t_min, tstep = 0.005)
		dw_vec_stc.save(ttest_result.format(subject, 'dW', time_lbl))


