import numpy as np
import random
import os

scenarios = sorted(os.listdir("solved_scenarios"))

sol = [0.085, 30.0, 30.0, 6.99]
confs = 0
for sc in scenarios:
	os.system("Ocaml_func/_build/check_confs_incert.byte solved_scenarios/{} {} {} {} {} > temp.txt".format(sc, sol[0], sol[1], sol[2], sol[3]))
	with open("temp.txt", 'r') as f:
		confs += len(f.readlines())
print(confs)