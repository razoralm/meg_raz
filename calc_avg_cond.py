import numpy as np
import mne

from avg_an_config import *

avg_cond_path = '/net/server/data/programs/razoral/platon_pmwords/target/stc_avg_cond/{}_{}_integ{}'

stc_test = mne.read_source_estimate(data_path.format(subjects[0], "passive1", words[0], integ_ms )) 
stc_shape = stc_test.data.shape

for session in sessions:

	for w_id, word in enumerate(words):

		w = np.zeros((stc_shape[0], stc_shape[1])) 
		d = np.zeros((stc_shape[0], stc_shape[1]))

		for subject_idx, subject in enumerate(subjects):
			
			stc = mne.read_source_estimate(data_path.format(subject, session, word, integ_ms))
			#print('stc shape: ', stc.data.shape)
			#print('w1_lbl shape: ', stc.data[lbl_inds, :].shape)				
			w += stc.data
			
			stc = mne.read_source_estimate(data_path.format(subject, session, distractors[w_id], integ_ms))
			d += stc.data

		avg_w = mne.SourceEstimate(w/len(subjects), vertices = stc_test.vertices, tmin = stc_test.tmin, tstep = stc_test.tstep)
		avg_d = mne.SourceEstimate(d/len(subjects), vertices = stc_test.vertices, tmin = stc_test.tmin, tstep = stc_test.tstep)

		avg_w.save(avg_cond_path.format(session, word, integ_ms))
		avg_d.save(avg_cond_path.format(session, distractors[w_id], integ_ms))
	
