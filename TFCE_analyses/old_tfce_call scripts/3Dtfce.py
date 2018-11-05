# first test of binary lubtfce in June18 on real full brain within time interval data and full brain with surrogate effect 
# it worked for surrogated data

import numpy
from array import array
import subprocess
import random
import os
import pickle

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

surrogates = range(30)

### files formats

## real data:

TFCE_data_path = '/net/server/data/programs/razoral/platon_pmwords/target/data_for_TFCE/{0}_{1}_{2}_integ5-{3}.stc'

TFCE_sur_data_path = '/net/server/data/programs/razoral/platon_pmwords/target/data_for_TFCE/surrogate/{0}_{1}_{2}_{3}-{4}.stc'

#Arkhipova_Elena_dD_144_217ms_integ5-lh.stc vs Arkhipova_Elena_dW_144_217ms_integ5-lh.stc
#Arkhipova_Elena_dD_226_362ms_integ5-lh.stc
#Arkhipova_Elena_dD__integ5-lh.stc

## surrogate data:

# /surrogate/{}_{}_{}_{}' 
# D/W_modification_param_n

# Dgauss_mean0.4_var0.1_0-lh.stc
#vs
# Wgauss_add_const_0.1_0-lh.stc
# Wgauss_add_const_0.1_0-lh.stc
# Wgauss_add_const_0.1_0-lh.stc

real_data =1 # flag which type of data

TFCE_files = []

outputTFCE_files = "results/TFCE_{0}_integ5-{1}.stc"

output_lh = []
output_rh = []

if real_data==1:

	# set time period on what TFCE calculated 
	time_lbl = '144_217ms'
	#time_lbl = '226_362ms'
	#time_lbl = ''
	
	for subject in subjects:
		#print(subject)
		#print(time_lbl)
		  
		TFCE_files.append(TFCE_data_path.format(subject, "dW", time_lbl, "lh"))
		TFCE_files.append(TFCE_data_path.format(subject, "dW", time_lbl, "rh"))
		TFCE_files.append(TFCE_data_path.format(subject, "dD", time_lbl, "lh"))
		TFCE_files.append(TFCE_data_path.format(subject, "dD", time_lbl, "rh"))
	
	output_lh = outputTFCE_files.format(time_lbl, "lh")	
	output_rh = outputTFCE_files.format(time_lbl, "rh")
	
	args = [
	"./libtfce",
	"-e", "0.666",
	"-h", "2",
	"--permutation-count", "100", 
	"--type", "mesh-time",
	"--source-space", "/net/server/data/programs/razoral/platon_pmwords/freesurfer/avg/bem/avg-ico-5p-src.fif",
	"--input-stcs"] + TFCE_files + ["--output-stcs", output_lh, output_rh]

	# call libtfce binary
	subprocess.call(args)


else: 
	
	# set surrogate difference type
	difference_type = "add_const" 
	
	if difference_type == "add_const":

		# set sur distractors params
		var = "var0.1" 
		mean = "mean0.4"
		
		difference_variations = ["10.0", "2.5", "1.0", "0.5", "0.2", "0.1", "0.05", "0.01"]

		for dif_var in difference_variations:
		
			for k in surrogates:
				#{ Dgauss }_{ difference_type }_{10}_{k}-{lh}.stc
		# Dgauss_mean0.4_var0.1_0-lh.stc
		#vs
		# Wgauss_add_const_0.1_0-lh.stc  
				TFCE_files.append(TFCE_sur_data_path.format("Wgauss", difference_type, dif_var, k, "lh"))
				TFCE_files.append(TFCE_sur_data_path.format("Wgauss", difference_type, dif_var, k,"rh"))
				TFCE_files.append(TFCE_sur_data_path.format("Dgauss", mean, var, k, "lh"))
				TFCE_files.append(TFCE_sur_data_path.format("Dgauss", mean, var, k, "rh"))

			output_lh = outputTFCE_files.format(difference_type+dif_var, "lh")	
			output_rh = outputTFCE_files.format(difference_type+dif_var, "rh")

			args = [
			"./libtfce",
			"-e", "0.666",
			"-h", "2",
			"--permutation-count", "100", 
			"--type", "mesh-time",
			"--source-space", "/net/server/data/programs/razoral/platon_pmwords/freesurfer/avg/bem/avg-ico-5p-src.fif",
			"--input-stcs"] + TFCE_files + ["--output-stcs", output_lh, output_rh]

			# call libtfce binary
			subprocess.call(args)


    
