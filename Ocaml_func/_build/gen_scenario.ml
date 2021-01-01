(*size je pense que c'est la taille de la fenetre, je l'ai pris de simu.ml, c'est utilisée dans Acft.random *)
let size = 0.47 *. 800. /. 10.


(*nombre de scénarios à générer *)
let n_sc = int_of_string Sys.argv.(1)

(*nombre d'avion dans tous les scénarios *)
let n = int_of_string Sys.argv.(2)

(*les incertitudes : v, t0, t1, h *)
let incert = [|float_of_string Sys.argv.(3); float_of_string Sys.argv.(4); float_of_string Sys.argv.(5); float_of_string Sys.argv.(6)|]

(* chemin ou les fichiers vont etre enregistrés *)
let path_save = Sys.argv.(7)

(* prefix des noms des fichers : name_save + "_i.txt" *)
let name_save = Sys.argv.(8)

(* 
Utilisation : 

gen_scenario.byte n_scenario n_avions delta_v delta_t0 delta_t1 delta_h path_save path_name

*)

let main = 
	Printf.printf "========> Generating %d scenarios : \n" n_sc;
	Printf.printf "# Number of airplanes per scenario : %d\n" n;
	Printf.printf "# delta_v = %f, delta_t0 = %f, delta_t1 = %f, delta_h = %f\n" incert.(0) incert.(1) incert.(2) incert.(3);
	Printf.printf "Saving %s_i.txt to %s\n" name_save path_save;
	Printf.printf "========> Done !\n";
	for i = 1 to n_sc do
		let a = Acft.random size n in
		Acft.save (Printf.sprintf "%s/%s_%d.txt" path_save name_save i) a incert;
	done
	