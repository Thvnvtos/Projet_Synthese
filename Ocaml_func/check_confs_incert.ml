
(*chemin du ficher texte de la résolution d'un scénario*)
let path = Sys.argv.(1)

(*les incertitudes : v, t0, t1, h *)
let incert = [|float_of_string Sys.argv.(2); float_of_string Sys.argv.(3); float_of_string Sys.argv.(4); float_of_string Sys.argv.(5)|]

let main = 
	let sc = Acft.load path in      (*Load scénario depuis path*)
	let a = (snd sc) in 			(* 2eme composant est le tableau d'avions*)
	let n = Array.length a in 		(* Nombre d'avions *)
	let t = fst (Acft.route a.(0)).(0) in (* le temps pris en compte par l'AG de resolution de conflit comme temps de debut*)
	(for i = 0 to n-1 do
		Acft.set_time a.(i) t;
		Acft.set_man incert a.(i);
		Acft.set_traj a.(i) incert;
	done);
	(for j = 0 to n-1 do
		let traj = Acft.get_traj a.(j) in
		let conf = Acft.detect_traj incert a j in
		Array.iteri (fun t (xyzs, _, _) ->
		if conf.(t) then Printf.printf "%d %d \n" j t;
			) traj;
	done);