import numpy as np
import random
import os

scenarios = sorted(os.listdir("solved_scenarios"))

def gen_sol():
	return [np.random.normal(0.1, 0.05), np.random.normal(30., 15.), np.random.normal(30., 15.), np.random.normal(5., 2.5)]

def init_pop(n):
	return [gen_sol() for i in range(n)]

def fitness(sol):
	flag = True
	for sc in scenarios:
		os.system("Ocaml_func/check_confs_incert.byte solved_scenarios/{} {} {} {} {} > temp.txt".format(sc, sol[0], sol[1], sol[2], sol[3]))
		with open("temp.txt", 'r') as f:
			if f.readlines() != []:
				flag = False
				break
	if not flag:
		return 0
	return 10*sol[0] + 0.033 * (sol[1] + sol[2]) + 0.2 * sol[3]


def selection(pop, k):
	pop_fit = sorted([(fitness(sol), sol) for sol in pop], reverse = True)
	return pop_fit[:k], pop_fit[0]

def crossover_mutation(elite, n, proba_mut):
	mean = []
	for i in range(4):
		mean.append(np.mean([x[1][i] for x in elite]))

	new_pop = []
	for i in range(n):
		if random.random() < proba_mut:
			new_pop.append([np.random.normal(mean[0], 0.01), np.random.normal(mean[1], 0.5), np.random.normal(mean[2], 0.5), np.random.normal(mean[3], 0.2)])
		else:
			new_pop.append([mean[0], mean[1], mean[2], mean[3]])
	return new_pop



if __name__ == "__main__":
	N = 50
	N_elite = 5
	max_iter = 300
	itr = 0
	eps = 1e-6
	fit = 0
	prev_fit = -1
	proba_mut = 0.2

	pop = init_pop(N)

	os.system("rm logs.txt")
	f = open("logs.txt", "w")

	while itr < max_iter:
		elite, best = selection(pop, N_elite)
		pop = crossover_mutation(elite, N, proba_mut)
		print("iteration {} : Best = {}".format(itr,best))
		f.write("{} {} {} {} {}\n".format(best[0], best[1][0], best[1][1], best[1][2], best[1][3]))
		itr += 1
	f.close()
	os.system("rm temp.txt")