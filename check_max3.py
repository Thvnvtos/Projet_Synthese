import numpy as np
import random
import os

scenarios = sorted(os.listdir("solved_scenarios"))
dt = 20.0

def check_incert(incert):
	confs = 0
	for sc in scenarios:
		os.system("Ocaml_func/_build/check_confs_incert.byte solved_scenarios/{} {} {} {} {} > temp.txt".format(sc, incert[0], incert[1], incert[2], incert[3]))
		with open("temp.txt", 'r') as f:
			confs += int(len(f.readlines()) > 0)
	return confs

def binary_search(incert, i, eps=1e-4):
	if i == 0: l,r = 0.0, 2.0
	else: l,r = 0.0,40.0

	while (r - l) > eps:
		incert[i] = (l+r)/2.
		confs = check_incert(incert)
		if confs == 0:
			l = incert[i]
		else:
			r = incert[i]
	incert[i] = l
	return incert


max_dv_incert = binary_search([0.0, 0.0, dt, 0.0], 0, eps = 1e-4)
N_points = 7
ddv = max_dv_incert[0]/(2*N_points)

max_dv_incert_eps = max_dv_incert.copy()
max_dv_incert_eps[0] += max_dv_incert_eps[0]/1e2
max_dv_incert_eps[1] += max_dv_incert_eps[1]/1e2
max_dv_incert_eps[3] += max_dv_incert_eps[3]/1e2

max_dv_incert_eps1 = max_dv_incert.copy()
max_dv_incert_eps1[0] += max_dv_incert_eps1[0]/10
max_dv_incert_eps1[1] += max_dv_incert_eps1[1]/10
max_dv_incert_eps1[3] += max_dv_incert_eps1[3]/10

max_dv_incert.append(check_incert(max_dv_incert))
max_dv_incert_eps.append(check_incert(max_dv_incert_eps))
max_dv_incert_eps1.append(check_incert(max_dv_incert_eps1))


pareto_front = [max_dv_incert+max_dv_incert_eps+max_dv_incert_eps1]
print("Initial pareto_front : ", pareto_front)
for i in range(1, N_points+1):
	
	incert = pareto_front[-1][:4].copy()
	print("##############")
	print(i)

	if i == N_points/2:
		ddv = incert[0]/(N_points-i)

	incert[0] = max(incert[0] - ddv - 1e-10, 0)
	found_incert = binary_search(incert, 1, eps=1e-3)

	found_incert_eps = found_incert.copy()
	found_incert_eps[0] += found_incert_eps[0]/1e2
	found_incert_eps[1] += found_incert_eps[1]/1e2
	found_incert_eps[3] += found_incert_eps[3]/1e2

	found_incert_eps1 = found_incert.copy()
	found_incert_eps1[0] += found_incert_eps1[0]/10
	found_incert_eps1[1] += found_incert_eps1[1]/10
	found_incert_eps1[3] += found_incert_eps1[3]/10

	found_incert.append(check_incert(found_incert))
	found_incert_eps.append(check_incert(found_incert_eps))
	found_incert_eps1.append(check_incert(found_incert_eps1))
	
	print("dv = {}, dt = {}, dh = {}, confs = {}".format(found_incert[0],found_incert[1],found_incert[3],found_incert[4]))
	print("dv1 = {}, dt1 = {}, dh1 = {}, confs1 = {}".format(found_incert_eps[0],found_incert_eps[1], found_incert_eps[3],found_incert_eps[4]))
	print("dv2 = {}, dt2 = {}, dh2 = {}, confs2 = {}".format(found_incert_eps1[0],found_incert_eps1[1], found_incert_eps1[3],found_incert_eps1[4]))

	pareto_front.append(found_incert + found_incert_eps + found_incert_eps1)

	ddt0 = found_incert[1]/(2*N_points)

	for j in range(1, N_points+1):

		incert = pareto_front[-1][:4].copy()
		print("##############")
		print("i = {}, j={}".format(i,j))

		if j == N_points/2:
			ddt0 = incert[1]/(N_points-j)
		

		incert[1] = max(incert[1] - ddt0 - 1e-10, 0)
		found_incert = binary_search(incert, 3, eps=1e-3)

		found_incert_eps = found_incert.copy()
		found_incert_eps[0] += found_incert_eps[0]/1e2
		found_incert_eps[1] += found_incert_eps[1]/1e2
		found_incert_eps[3] += found_incert_eps[3]/1e2

		found_incert_eps1 = found_incert.copy()
		found_incert_eps1[0] += found_incert_eps1[0]/10
		found_incert_eps1[1] += found_incert_eps1[1]/10
		found_incert_eps1[3] += found_incert_eps1[3]/10

		found_incert.append(check_incert(found_incert))
		found_incert_eps.append(check_incert(found_incert_eps))
		found_incert_eps1.append(check_incert(found_incert_eps1))
		
		print("dv = {}, dt = {}, dh = {}, confs = {}".format(found_incert[0],found_incert[1],found_incert[3],found_incert[4]))
		print("dv1 = {}, dt1 = {}, dh1 = {}, confs1 = {}".format(found_incert_eps[0],found_incert_eps[1], found_incert_eps[3],found_incert_eps[4]))
		print("dv2 = {}, dt2 = {}, dh2 = {}, confs2 = {}".format(found_incert_eps1[0],found_incert_eps1[1], found_incert_eps1[3],found_incert_eps1[4]))

		pareto_front.append(found_incert + found_incert_eps + found_incert_eps1)



with open("pareto_front.txt", 'w') as f:
	for incert in pareto_front:
		f.write("{} {} {} {} {} {} {} {} {} {} {} {} \n".format(incert[0],incert[1], incert[3], incert[4], 
													  incert[5],incert[6], incert[8], incert[9],
													  incert[10],incert[11], incert[13],incert[14]))








