import sys
import os
import numpy as np
from pandas import DataFrame
from scipy import stats

words = ["hicha", "hishu", "hisa", "hivu"]
distractors = ["hichu", "hisha", "hisu", "hiva"]

timecourse_types = ["dw_dd", "w1_d1", "w2_d2"]

time_lbls = ["220_495","285_295", "300-360"]
time_periods = [[220, 495], [285, 295], [300, 360]] 

behav_parameters = ["learning_criterion", "false_alarms"]


stc_table_path = "/data/programs/razoral/insula_timecourses/target_timecourses/corr_tables_insula/corr_table_insula_{}_{}.tsv"
behavioral_table_path = "/data/programs/razoral/insula_timecourses/examples/active1_{}_per_subject.tsv"

def calc_corr(beh_table_path, stc_table_path, timecourse_types, behav_parameter, time_period, time_lbl, words):

	corr_table = np.zeros(shape = (len(timecourse_types) , len(words), 2))

	for timecourse_type_id, timecourse_type in enumerate(timecourse_types):

		beh_df = DataFrame.from_csv(beh_table_path.format(behav_parameter), sep = "\t")
		stc_df = DataFrame.from_csv(stc_table_path.format(timecourse_type, time_lbl), sep = "\t")

		# exclude subjects 
		sub_list = beh_df.index
		actual_sub_list = stc_df.index
		sub_to_del = sub_list.difference(actual_sub_list)
		beh_df = beh_df.drop(sub_to_del)

		# calc correlation
		for word_id, word in enumerate(words):
			corr_cur = stats.pearsonr(beh_df[word],stc_df[word])
			corr_table[timecourse_type_id, word_id, :] = corr_cur

		# form corr table

	os.makedirs("/data/programs/razoral/insula_timecourses/target_timecourses/behave_correlations_insula", exist_ok=True)
	f = open("/data/programs/razoral/insula_timecourses/target_timecourses/behave_correlations_insula/pearson_corr_insula_{}_{}.tsv".format(behav_parameter, time_lbl), "w")
	f.write("timecourse_type")
	for word in words:
		f.write("\t{}_corr\t{}_p-val".format(word, word))
	f.write("\n")
	for timecourse_type_id, timecourse_type in enumerate(timecourse_types):
		f.write("{}".format(timecourse_type))
		for word_id, word in enumerate(words):
			f.write("\t{:e}\t{:e}".format(corr_table[timecourse_type_id, word_id, 0], corr_table[timecourse_type_id, word_id, 1]))
		f.write("\n")
	f.close()


for t, time_period in enumerate(time_periods):
	for behav_parameter in behav_parameters:
		calc_corr(behavioral_table_path, stc_table_path, timecourse_types, behav_parameter, time_period, time_lbls[t], words)





	
