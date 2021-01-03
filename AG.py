import numpy as np
import os

scenarios = sorted(os.listdir("solved_scenarios"))

def gen_sol():
	return [np.random.normal(0.1, 0.03), np.random.normal(30., 5.), np.random.normal(30., 5.), np.random.normal(5., 2.)]

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
	return 500*sol[0] + (sol[1] + sol[2])/30 + sol[3]

def selection(pop, n):
	pop_fit = sorted([(fitness(sol), sol) for sol in pop], reverse = True)
	return pop_fit[:n], pop_fit[0]

def crossover_mutation(elite, n):
	mean = []
	for i in range(4):
		mean.append(np.mean([x[1][i] for x in elite]))

	return [[np.random.normal(mean[0], 0.003), np.random.normal(mean[1], 0.5), np.random.normal(mean[2], 0.5), np.random.normal(mean[3], 0.2)] for i in range(n)]



if __name__ == "__main__":
	N = 50
	N_elite = 5
	max_iter = 20
	itr = 0
	eps = 1e-6
	fit = 0
	prev_fit = -1


	pop = init_pop(N)

	while itr < max_iter:
		elite, best = selection(pop, N_elite)
		pop = crossover_mutation(elite, N)
		print("iteration {} : Best = {}".format(itr,best))
		itr += 1