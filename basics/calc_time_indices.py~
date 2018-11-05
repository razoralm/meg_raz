import mne 
import numpy as np

def calc_time_indices(time_intervals, stc_sample_path, integ_ms):

	time_intervals_inds = np.zeros(shape = time_intervals.shape)

	stc_sample = mne.read_source_estimate(stc_sample_path)

	ambg_ind = int(abs(stc_sample.tmin//stc_sample.tstep))
	print("ambg_point: %s" % (ambg_ind))	
	

	for time_lbl_idx, time_interval in enumerate(time_intervals):
		
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
	
		time_intervals_inds[time_lbl_idx][:] = [t0_ambg, t1_ambg]
		print ('time intervals inds', time_intervals_inds)

	return time_intervals_inds
