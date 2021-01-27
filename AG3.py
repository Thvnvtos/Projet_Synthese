import numpy as np
import random
import os
import tqdm

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
	print("++++++ Initializing the population ++++++")
	pop = []
	for i in tqdm.tqdm(range(n)):
		sol = gen_sol()
		confs = check_incert(sol)
		while confs:
			sol = [sol[0] - sol[0]/5, sol[1] - sol[1]/5, sol[2], sol[3] - sol[3]/5]
			confs = check_incert(sol)
		j = random.choice([0,1,3])
		sol = binary_search(sol,j,eps=1e-3)
		pop.append(sol)
	return pop

def fitness(sol):
	sol_5 = [x+x/20 for x in sol]
	sol_3 = [x+x/30 for x in sol]
	sol_2 = [x+x/50 for x in sol]
	
	sol_5[2] = dt
	sol_3[2] = dt
	sol_2[2] = dt

	confs_5 = check_incert(sol_5)
	confs_3 = check_incert(sol_3)
	confs_2 = check_incert(sol_2)

	return confs_2 + confs_3 + confs_5


def selection(pop, k):
	print("====> Selection process : ")
	pop_fit = []
	for i in tqdm.tqdm(range(len(pop))):
		pop_fit.append((fitness(pop[i]), pop[i]))
	pop_fit = sorted(pop_fit, reverse = True)
	return [x[1] for x in pop_fit[:k]], pop_fit[0]

def crossover_mutation(elite,pop, n, proba_mut, proba_big_mut):
	half = len(elite)//2
	new_gen = []
	print("====> Crossover Process : ")
	for i in tqdm.tqdm(range(half)):
		sol_1 = elite[:half][i]
		sol_2 = elite[half:][i]
		sol = [max(sol_1[j],sol_2[j]) for j in range(len(sol_1))]
		#print(sol_1)
		#print(sol)
		confs = check_incert(sol)
		while confs:
			sol = [sol[0] - sol[0]/50, sol[1] - sol[1]/50, sol[2], sol[3] - sol[3]/50]
			confs = check_incert(sol)
		j = random.choice([0,1,3])
		sol = binary_search(sol,j,eps=1e-3)
		new_gen.append(sol)

	pop = elite[:half] + new_gen + pop[2*half:]

	print("====> Mutation Process : ")
	for i in tqdm.tqdm(range(2*half,n)):
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
	N_elite = 6
	max_iter = 150
	itr = 0
	eps = 1e-6
	fit = 0
	prev_fit = -1
	proba_mut = 0.25
	proba_big_mut = 0.1

	os.system("rm logs.txt")
	
	pop = init_pop(N)
	elite, best = selection(pop, N_elite)

	while itr < max_iter:
		print("+++++++++ Iteration {} ++++++++++".format(itr+1)) 
		print("Top fitness = {}, incert  = {}".format(best[0], best[1]))
		mean = []		
		for i in range(4):	
			mean.append(np.mean([x[i] for x in elite])) 
		print("Mean of Elite population : {}\n".format(mean))
		with open("logs.txt", 'a') as f:
			f.write("{} {} {} {} {}\n".format(best[0], best[1][0], best[1][1], best[1][2], best[1][3]))
		pop = crossover_mutation(elite,pop, N, proba_mut, proba_big_mut)
		elite, best = selection(pop, N_elite)
		itr += 1
	print("+++++++++ Iteration {} ++++++++++".format(itr+1)) 
	print("Top fitness = {}, incert  = {}".format(best[0], best[1]))
	mean = []		
	for i in range(4):	
		mean.append(np.mean([x[i] for x in elite])) 
	print("Mean of Elite population : {}\n".format(mean))
	with open("logs.txt", 'a') as f:
		f.write("{} {} {} {} {}\n".format(best[0], best[1][0], best[1][1], best[1][2], best[1][3]))
	os.system("rm temp.txt")
