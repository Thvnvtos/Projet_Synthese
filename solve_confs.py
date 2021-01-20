'''

Script de résolution de scénarios de conflits

'''
import os

scenarios = os.listdir("scenarios")
debug = False

if debug:
	os.system("rm -rf logs/*")

os.system("rm -rf solved_scenarios/*")

for sc in sorted(scenarios):
	print("===> Solving {} ... ".format(sc))
	os.system("AG_TD/agopt scenarios/{} solved_scenarios/{} > temp.txt".format(sc, sc))
	os.system("Ocaml_func/_build/check_confs.byte solved_scenarios/{} > temp.txt".format(sc))
	with open("temp.txt", 'r') as f:
		if f.readlines() == []:
			print(sc + " Done !!\n")
		else:
			if debug:
				os.system("echo {} >> logs/solve_confs_logs.txt".format(sc))
				os.system("Ocaml_func/_build/check_confs.byte solved_scenarios/{} >> logs/solve_confs_logs.txt".format(sc))
			print("No solution found for " + sc +"\n")
			os.system("rm solved_scenarios/{}".format(sc))

os.system("rm temp.txt")