import numpy

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


words = ["hicha", "hishu", "hisa", "hivu"]

distractors = ["hichu", "hisha", "hisu", "hiva"]


sessions = ['passive1', 'passive2']


tmin = -410
tmax = 615

integ_ms = 5 # 1, 5, 25

t_len = (tmax - tmin)//integ_ms


n_voxels = 20484


data_path = "/net/server/data/programs/razoral/platon_pmwords/target/stc-basecorr/{}_{}_{}_integ{}-lh.stc" 
																		                # name_session_stimul_integ-hemisphere.stc






