import numpy
import mne
from scipy import stats

subjects = [
	"Arkhipova_Elena"]


sti_words = ["hicha", "hishu", "hisa", "hivu"]
sti_distractors = ["hichu", "hisha", "hisu", "hiva"]



tmin = -410
tmax = 615


timings = ["p145_217ms", "p226_362ms", "p218_459", "a230_280ms", "a465_515ms", "as200_500ms"] # list 					  for 5 ms it is:
time_intervals = numpy.array([[144, 217], [226, 362], [218, 459], [230, 280], [465, 515], [200, 500]]) 

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
