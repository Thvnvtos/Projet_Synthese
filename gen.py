'''

Script de génération de scénarios de conflits

'''
import os

# dictionnaire contenant le nombre de scénarios a générer pour chaque nombre d'avions
n = {2 : 30, 3 : 30, 4 : 30, 5 : 30}

# incertitudes : 
delta = [0.1, 30., 30., 5.]

os.system("rm -rf scenarios/*")

for n_av in n.keys():
	os.system("Ocaml_func/gen_scenario.byte {} {} {} {} {} {} scenarios sc_av_{}".format(n[n_av], n_av, delta[0], delta[1], delta[2], delta[3], n_av))