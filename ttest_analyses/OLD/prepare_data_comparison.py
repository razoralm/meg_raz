# prepare dD and dW arrays for TFCE with timecut

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
	"Yarmolova_Elena"]

sti_words = ["hicha", "hishu", "hisa", "hivu"]

sti_distractors = ["hichu", "hisha", "hisu", "hiva"]

tmin = -410
tmax = 615

timings =["144_362ms"] #original_version: ["144_217ms", "226_362ms"] # list          for 5 ms it is:
time_intervals = numpy.array([[145, 360]]) #original_version: numpy.array([[144, 217], [226, 362]]) 
                                                                          # [[145-215], [225-360]] left do not include

integ_ms = 5

target_files_format = "/net/server/data/programs/razoral/platon_pmwords/target/stc-basecorr/{}_{}_{}_integ5-lh.stc" 
																							# name_session_stimul_integ-hemisphere.stc
save_result_format = "/net/server/data/programs/razoral/platon_pmwords/target/data_for_TFCE/{}_{}_{}_integ5" 
																							# name_differenceType_timeInterval_integ[-hemisphere.stc]-auto

n_voxels = 20484
time_length = tmax - tmin
t_len = time_length//integ_ms
print('t_len', t_len)
	
# stc initialization
time_intervals_inds = numpy.zeros(shape = time_intervals.shape)
#print ('time_intervals_inds', time_intervals_inds)	


stc1 = mne.read_source_estimate(target_files_format.format(subjects[0], "passive1", sti_words[0]))
#print(stc1.data.shape)
#print(stc1.tmin, stc1.tstep)
ambg_ind = int(abs(stc1.tmin//stc1.tstep))
print("ambg_point: %s" % (ambg_ind))
	
# time intervals recalculation
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

print (time_intervals_inds)

#
dw = numpy.zeros(shape = (n_voxels, t_len))
#print('data_array:', dw.shape)
dd = numpy.zeros(shape = (n_voxels, t_len))
#print('stc_data_shape:', stc1.data.shape)

for subject_idx, subject in enumerate(subjects):
	print("\n({:2}/{:2}) reading {}\n".format(subject_idx+1, len(subjects), subject))
	
	#
	dw = numpy.zeros(shape = (n_voxels, t_len))
	dd = numpy.zeros(shape = (n_voxels, t_len))	
	#

	for word in sti_words:
			
		w1 = mne.read_source_estimate(target_files_format.format(subject, "passive1", word)).data
		w2 = mne.read_source_estimate(target_files_format.format(subject, "passive2", word)).data
		dw += (w1 - w2)
		
	dw_stc = mne.SourceEstimate(dw/len(sti_words), vertices = stc1.vertices, tmin = stc1.tmin, tstep = stc1.tstep)
	#print(dw_stc.data.shape)
	#print(dw_stc.tmin)
	#print(dw_stc.tstep)
	
	#save_all_data_interval	
	#dw_stc.save(save_result_format.format(subject, 'dW', ''))

	for distractor in sti_distractors:
		d1 = mne.read_source_estimate(target_files_format.format(subject, "passive1", distractor)).data
		d2 = mne.read_source_estimate(target_files_format.format(subject, "passive2", distractor)).data  
		dd += (d1 - d2)
		
	dd_stc = mne.SourceEstimate(dd/len(sti_distractors), vertices = stc1.vertices, tmin = stc1.tmin, tstep = stc1.tstep)

	#save_all_data_interval			
	#dd_stc.save(save_result_format.format(subject, 'dD', ''))


	# drop time
	for timing_idx, time_interval_inds in enumerate(time_intervals_inds):
		print("\n({:2}/{:2}) cut {}\n".format(timing_idx+1, len(time_intervals), timings[timing_idx]))
		
		dt = int(time_interval_inds[1] - time_interval_inds[0])


		
		#print('tmin=', time_intervals[timing_idx][0]/1000)

		dw_timecut_stc = mne.SourceEstimate(dw_stc.data[:, time_interval_inds[0]:time_interval_inds[1]], vertices = stc1.vertices, tmin =  time_intervals[timing_idx][0]/1000, tstep = stc1.tstep)
		#print(dw_timecut_stc.data.shape)

		dd_timecut_stc = mne.SourceEstimate(dd_stc.data[:, time_interval_inds[0]:time_interval_inds[1]], vertices = stc1.vertices, tmin =  time_intervals[timing_idx][0]/1000, tstep = stc1.tstep)
		#print(dd_timecut_stc.data.shape)
			
		dw_timecut_stc.save(save_result_format.format(subject, 'dW', timings[timing_idx]))
		dd_timecut_stc.save(save_result_format.format(subject, 'dD', timings[timing_idx]))
		