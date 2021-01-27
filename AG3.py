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


def gen_sol():
	return [np.random.uniform(0.0, .3), np.random.uniform(0.0,40.0) , 20., np.random.uniform(0.0, 15.0)]

def init_pop(n):
	pop = []
	for i in range(n):
		sol = gen_sol()
		confs = check_incert(sol)
		while confs:
			sol = [sol[0] - sol[0]/10, sol[1] - sol[1]/10, sol[2], sol[3] - sol[3]/10]
			confs = check_incert(sol)
		j = random.choice([0,1,3])
		sol = binary_search(sol,j,eps=1e-3)
		pop.append(sol)
	return pop

def fitness(sol):
	sol_5 = [x+x/20 for x in sol]
	sol_2 = [x+x/50 for x in sol]
	confs_5 = check_incert(sol_5)
	confs_2 = check_incert(sol_2)

	return confs_2 + confs_5


def selection(pop, k):
	pop_fit = sorted([(fitness(sol), sol) for sol in pop], reverse = True)
	return pop_fit[:k], pop_fit[0]

def crossover_mutation(elite,pop, n, proba_mut, proba_big_mut):
	half = len(elite)//2
	new_gen = []
	for i in range(half):
		sol_1 = elite[:half][i]
		sol_2 = elite[half:][i]
		sol = [max(sol_1[j],sol_2[j]) for j in range(half)]
		confs = check_incert(sol)
		while confs:
			sol = [sol[0] - sol[0]/50, sol[1] - sol[1]/50, sol[2], sol[3] - sol[3]/50]
			confs = check_incert(sol)
		j = random.choice([0,1,3])
		sol = binary_search(sol,j,eps=1e-3)
		new_gen.append(sol)

	pop = elite[:half] + new_gen + pop[2*half:]

	for i in range(n):
		if random.random() < proba_mut:
			j = random.choice([0,1,3])
			pop[i][j] -= pop[i][j]/2
			choices = [0,1,3]
			choices.remove(j)
			k = random.choice(choices)
			pop[i] = binary_search(pop[i],k,eps=1e-3)

	return pop




if __name__ == "__main__":
	N = 25
	N_elite = 5
	max_iter = 100
	itr = 0
	eps = 1e-6
	fit = 0
	prev_fit = -1
	proba_mut = 0.1
	proba_big_mut = 0.1

	pop = init_pop(N)

	os.system("rm logs.txt")

	while itr < max_iter:
		elite, best = selection(pop, N_elite)
		pop = crossover_mutation(elite,pop, N, proba_mut, proba_big_mut)
		score = fitness(best)
		print("iteration {} : Top fitness = {}, incert  = {}".format(itr,score, best))
		with open("logs.txt", 'a') as f:
			f.write("{} {} {} {} {}\n".format(score, best[0], best[1], best[2], best[3]))
		itr += 1
	os.system("rm temp.txt")
