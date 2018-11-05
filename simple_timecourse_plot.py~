import sys
import os
import numpy as np
import mne
from scipy import stats
from matplotlib import pyplot

target = "/data/programs/razoral/platon_back_up/pmwords/target/stc-avg-cond/{}_{}_integ5-lh.stc"

tmin = -410
tmax = 615
integ_ms = 5
time_range = np.arange(tmin, tmax, integ_ms)



sessions = ["passive1", "passive2"]

sti_words = ["hicha", "hishu", "hisa", "hivu"]
sti_distractors = ["hichu", "hisha", "hisu", "hiva"]



for session in sessions:


	for word in sti_words:
		
		stc_cur = mne.read_source_estimate(target.format(session, word))		
		
		#print(stc_cur.tmin)
		#print(stc_cur.tstep)

		data = np.mean(stc_cur.data, axis = 0)

		pyplot.figure(1)
		pyplot.title("Timecourse_stc-avg-cond:{}_words_integ5-lh ".format(session))
		pyplot.xlabel("time [ms]")
		pyplot.ylabel("intensity")
		pyplot.xlim(tmin, tmax)
		pyplot.plot(time_range, data, label = word)
		pyplot.legend(loc = "upper right", framealpha = 0.5)
		pyplot.grid()
		pyplot.axvline(0, color="#888888")
		pyplot.axhline(0, color="#888888")
	pyplot.savefig("/data/programs/razoral/platon_back_up/pmwords/target/stc-avg-cond/plot_check/{}_words_integ5-lh.png".format(session))
	pyplot.savefig("/data/programs/razoral/platon_back_up/pmwords/target/stc-avg-cond/plot_check/{}_words_integ5-lh.pdf".format(session))
	

	for distr in sti_distractors:

		stc_cur = mne.read_source_estimate(target.format(session, distr))		
		
		#print(stc_cur.tmin)
		#print(stc_cur.tstep)

		data = np.mean(stc_cur.data, axis = 0)

		pyplot.figure(2)
		pyplot.title("Timecourse_stc-avg-cond:{}_distractors_integ5-lh ".format(session))
		pyplot.xlabel("time [ms]")
		pyplot.ylabel("intensity")
		pyplot.xlim(tmin, tmax)
		pyplot.plot(time_range, data, label = word)
		pyplot.legend(loc = "upper right", framealpha = 0.5)
		pyplot.grid()
		pyplot.axvline(0, color="#888888")
		pyplot.axhline(0, color="#888888")
	pyplot.savefig("/data/programs/razoral/platon_back_up/pmwords/target/stc-avg-cond/plot_check/{}_distractors_integ5-lh.png".format(session))
	pyplot.savefig("/data/programs/razoral/platon_back_up/pmwords/target/stc-avg-cond/plot_check/{}_distractors_integ5-lh.pdf".format(session))
	
	pyplot.show()









