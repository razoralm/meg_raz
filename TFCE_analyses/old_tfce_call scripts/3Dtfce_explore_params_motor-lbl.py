# Explore mode for labeled data witin time interval. worked 19August18 for motor_smtp

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

TFCE_data_path = '/net/server/data/programs/razoral/platon_pmwords/target/data_for_TFCE/labeled/motor_smtp_an/test/{0}_{1}_{2}_{3}_integ5_{4}-lbl-{5}.stc'
#Arkhipova_Elena_passive1_hicha_200_400ms_integ5_active2hisa-lbl-rh.stc

real_data =1 # flag which type of data

TFCE_files = []

outputTFCE_files = "results/TFCE_{0}_{1}_integ5-{2}.stc"

output_lh = []
output_rh = []

if real_data==1:

	# set time period on what TFCE calculated 

	time_lbl = '200_400ms'
	#time_lbl = '226_362ms'
	#time_lbl = '0_500ms'
	#time_lbl = ''

	# set lbl_name on what TFCE calculated 

	#lbl_name = 'ant_temporal_sulc'
	#lbl_name = 'inf_operculum'
	#lbl_name = 'low_precentral_sulc'
	lbl_name = 'active2hisa'

	word = 'hisa'

	for subject in subjects:
		#print(subject)
		#print(time_lbl)
		  
		TFCE_files.append(TFCE_data_path.format(subject, "passive1", word, time_lbl, lbl_name, "lh"))
		TFCE_files.append(TFCE_data_path.format(subject, "passive1", word, time_lbl, lbl_name, "rh"))
		TFCE_files.append(TFCE_data_path.format(subject, "passive2", word, time_lbl, lbl_name, "lh"))
		TFCE_files.append(TFCE_data_path.format(subject, "passive2", word, time_lbl, lbl_name, "rh"))
	
	output_lh = outputTFCE_files.format(time_lbl, lbl_name,"lh")	
	output_rh = outputTFCE_files.format(time_lbl, lbl_name,"rh")
	
	args = [
	"./libtfce",
	"--explore",	
	"--e-max", "2", "--e-step", "0.1",
	"-e", "0",
	"--h-max", "2", "--h-step", "0.1",
	"-h", "0",
	"--permutation-count", "100", 
	"--type", "mesh-time",
	"--source-space", "/net/server/data/programs/razoral/platon_pmwords/freesurfer/avg/bem/avg-ico-5p-src.fif",
	"--input-stcs"] + TFCE_files + ["--output-stcs", output_lh, output_rh]

	# call libtfce binary
	subprocess.call(args)





    