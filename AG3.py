import numpy as np
import random
import os

scenarios = sorted(os.listdir("solved_scenarios"))

def gen_sol():
	return [np.random.uniform(0.0, 1.0), np.random.uniform(0.0,50.0) , 20., np.random.uniform(0.0, 15.0)]

def init_pop(n):
	return [gen_sol() for i in range(n)]

def fitness(sol):
	confs_tot = 0
	confs_0 = 0
	confs_2 = 0
	confs_4 = 0
	for sc in scenarios:
		os.system("Ocaml_func/_build/check_confs_incert.byte solved_scenarios/{} {} {} {} {} > temp.txt".format(sc, sol[0], sol[1], sol[2], sol[3]))
		with open("temp.txt", 'r') as f:
			n = len(f.readlines())
			confs += n
			confs_0 += int(n>0)

		os.system("Ocaml_func/_build/check_confs_incert.byte solved_scenarios/{} {} {} {} {} > temp.txt".format(sc, sol[0] + sol[0]/50, sol[1] + sol[1]/50, sol[2], sol[3]+sol[3]/50))
		with open("temp.txt", 'r') as f:
			n = len(f.readlines())
			confs_2 += int(n>0)

		os.system("Ocaml_func/_build/check_confs_incert.byte solved_scenarios/{} {} {} {} {} > temp.txt".format(sc, sol[0] + sol[0]/25, sol[1] + sol[1]/25, sol[2], sol[3]+sol[3]/25))
		with open("temp.txt", 'r') as f:
			n = len(f.readlines())
			confs_4 += int(n>0)

	return confs_2 + confs_4 - 1000 * confs


def selection(pop, k):
	pop_fit = sorted([(fitness(sol), sol) for sol in pop], reverse = True)
	return pop_fit[:k], pop_fit[0]

def crossover_mutation(elite, n, proba_mut, proba_big_mut):
	mean = []
	for i in range(4):
		mean.append(np.mean([x[1][i] for x in elite]))

	new_pop = []
	for i in range(n):
		if random.random() < proba_big_mut:
			new_pop.append([np.random.normal(mean[0], 0.1), mean[1], mean[2], np.random.normal(mean[3], 2)])
		elif random.random() < proba_mut:
			new_pop.append([np.random.normal(mean[0], 0.01), mean[1], mean[2], np.random.normal(mean[3], 0.2)])
		else:
			new_pop.append([mean[0], mean[1], mean[2], mean[3]])
	return new_pop, mean 



if __name__ == "__main__":
	N = 10
	N_elite = 3
	max_iter = 100
	itr = 0
	eps = 1e-6
	fit = 0
	prev_fit = -1
	proba_mut = 0.25
	proba_big_mut = 0.1

	pop = init_pop(N)

	os.system("rm logs.txt")

	while itr < max_iter:
		elite, best = selection(pop, N_elite)
		pop, mean = crossover_mutation(elite, N, proba_mut, proba_big_mut)
		score = fitness(mean)
		print("iteration {} : Top 10% fitness = {}, mean incert  = {}".format(itr,score, mean))
		with open("logs.txt", 'a') as f:
			f.write("{} {} {} {} {}\n".format(score, mean[0], mean[1], mean[2], mean[3]))
		itr += 1
	os.system("rm temp.txt")