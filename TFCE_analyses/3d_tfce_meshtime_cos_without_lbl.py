import numpy
from array import array
import subprocess
import random
import os
import pickle



### directories
path = '/net/server/data/programs/razoral/platon_pmwords/'

TFCEinput_stc = path + 'target/data_for_TFCE/cos/{}_{}_{}_integ5-{}.stc' 
#TFCEinput_stc = path + 'target/data_for_TFCE/labeled/normalized_sti/normalized_sti_{0}_{1}_{2}_integ5_{3}-{4}.stc'
                                                                        # zamenit' na {0}_{1}_{2}_integ5_{3}-{4}.stc
# file format for comparison example:
							 #Arkhipova_Elena_dD_144_217ms_lbl_integ5-lh.stc vs Arkhipova_Elena_dW_144_217ms_lbl_integ5-lh.stc
							 #Arkhipova_Elena_dD_226_362ms_lbl_integ5-lh.stc

output_meshtime_stc = path + "scripts/raz/TFCE_analyses/meshtime_results/3dTFCE_{}_{}_integ5_{}_e{}h{}n{}-{}.stc"
# output stc file example:
                                #3dTFCE_144_217ms_integ5_presylvian_e1h2n100-lh
                                #type_{time_interval}_integ_{label}_param-e{e}param-h{h}n_perm{n_perm}-{hemisphere}.stc

output_explore = path + "/scripts/raz/TFCE_analyses/explore_results/3dEXPLORE_{}_integ5_{}_{}_e{}-{}_h{}-{}_step{}.txt"
# output explore example:
								 #"3dEXPLORE_144_217ms_integ5_inf_operculum_e0-2_h0-2_step0.1_n100.txt"
    							 #"3dEXPLORE_{time_interval}_integ5_{label}_e{0}-{2}_h{0}-{2}_step{0.1}_n{}.txt"



### TFCE params
e = "0.8"
#e_max = "2"

h = "0.5"
#h_max = "2"

n_perm = "100"

#step = "0.1"



### Analysis params 

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

## set time period on what TFCE calculated 

#time_lbl = '144_217ms'
#time_lbl = '226_362ms'
time_lbl = '144_362ms'
#time_lbl = '0_600ms'
	

## set lbl_name on what TFCE calculated 

#lbl_name = 'ant_temporal_sulc'
#lbl_name = 'inf_operculum'
#lbl_name = 'low_precentral_sulc'
#lbl_name = 'presylvian'
	


### code

TFCE_files = []
output_lh = []
output_rh = []

for subject in subjects:
	#print(subject)
	#print(time_lbl)
		  
	TFCE_files.append(TFCEinput_stc.format(subject, "cosS1W2", time_lbl,"lh"))
	TFCE_files.append(TFCEinput_stc.format(subject, "cosS1W2", time_lbl, "rh"))
	TFCE_files.append(TFCEinput_stc.format(subject, "cosS1D2", time_lbl, "lh"))
	TFCE_files.append(TFCEinput_stc.format(subject, "cosS1D2", time_lbl, "rh"))


## set output stc names (for fixed params in mesh-time mode) 

                                #3dTFCE_144_217ms_integ5_presylvian_e1h2n100-lh
                                #type_{time_interval}_integ_{label}_param-e{e}param-h{h}n_perm{n_perm}-{hemisphere}.stc
output_lh = output_meshtime_stc.format('cosS1W2_vs_cosS1D2', time_lbl, '', e, h, n_perm, "lh")	
output_rh = output_meshtime_stc.format('cosS1W2_vs_cosS1D2', time_lbl, '', e, h, n_perm, "rh")	

										#3dTFCE_{}_{}_integ5_{}_e{}h{}n{}-{}"

args = [
		"./libtfce",
		
		"-e", e,
		
		"-h", h,
		"--permutation-count", n_perm, 
		"--type", "mesh-time",
		"--source-space", "/net/server/data/programs/razoral/platon_pmwords/freesurfer/avg/bem/avg-ico-5p-src.fif",
		"--input-stcs"] + TFCE_files + ["--output-stcs", output_lh, output_rh]

	# call libtfce binary
subprocess.call(args)





    
