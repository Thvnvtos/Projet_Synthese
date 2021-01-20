import numpy as np
import random
import os

scenarios = sorted(os.listdir("solved_scenarios"))
dt = 30.0

def check_incert(incert):
	confs = 0
	for sc in scenarios:
		os.system("Ocaml_func/_build/check_confs_incert.byte solved_scenarios/{} {} {} {} {} > temp.txt".format(sc, incert[0], incert[1], incert[2], incert[3]))
		with open("temp.txt", 'r') as f:
			confs += len(f.readlines())
	return confs

def binary_search(incert, i, eps=1e-3):
	if i == 0: l,r = 0.0, 2.0
	else: l,r = 0.0,40.0

	while (r - l) > eps:
		incert[i] = (l+r)/2.
		confs = check_incert(incert)
		if confs == 0:
			l = incert[i]
		else:
			r = incert[i]
	incert[i] = (l+r)/2.
	return incert


max_dv_incert = binary_search([0.0, dt, dt, 0.0], 0, eps = 1e-4)
N_points = 10
ddv = max_dv_incert[0]/N_points

pareto_front = [max_dv_incert]
print("Initial pareto_front : ", pareto_front)
for i in range(1, N_points+1):
	incert = pareto_front[i-1].copy()
	print("##############")
	print(i)
	incert[0] = max(incert[0] - ddv - 1e-10, 0)
	found_incert = binary_search(incert, 3, eps=1e-2)
	print("found incert : ", found_incert)
	pareto_front.append(found_incert)


with open("pareto_front.txt", 'w') as f:
	for incert in pareto_front:
		f.write("{} {} {} {}\n".format(incert[0], incert[1], incert[2], incert[3]))








