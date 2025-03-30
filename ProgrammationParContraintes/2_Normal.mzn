% KARAKI 2402594
% LUQUET 2402133


include "globals.mzn"; 

%-----------------------------------------------------------------------------%
% Données
%-----------------------------------------------------------------------------%

% Nombre de tâches
int: n;
% Durée maximal du projet
int: m;
% Limite de ressources pouvant être partagées entre les tâches en cours
int: limite;

% Durée des tâches
array[1..n] of 1..m: duree_tache;
% Ressources requises par les tâches
array[1..n] of 1..m: ressource_tache;

%-----------------------------------------------------------------------------%
% Variables de décisions
%-----------------------------------------------------------------------------%

array[1..n] of var 1..m: debut_tache; % Début des tâches
array[1..n] of var 1..m: fin_tache; % Fin des tâches

%-----------------------------------------------------------------------------%
% Objectif
%-----------------------------------------------------------------------------%

% Fin du projet
var int: fin_projet = max(fin_tache);

%-----------------------------------------------------------------------------%
% Partie étudiant
%-----------------------------------------------------------------------------%
% Contrainte 1 : Chaque tache possede une durée
constraint forall(i in 1..n)( fin_tache[i] = debut_tache[i] + duree_tache[i]);

% Contrainte  2 : Chaque tâches peut être effectuées dans n’importe quel ordre et en parallèle. 
% Elle a une dureé et un besoin d'energie mais ne doit pas depasser une l'imite d'energie spécifique
constraint cumulative(debut_tache, duree_tache, ressource_tache, limite);

% Contrainte 3 : Pas plus de deux tâches ne démarrent en même temps = nombre de démarrages simultanés est limité à 2
constraint forall(i in 1..m) ( sum([if debut_tache[j] == i then 1 else 0 endif | j in 1..n]) <= 2);

% Contrainte 4 : Minimiser le temps avant la fin du projet
solve minimize fin_projet;
%-----------------------------------------------------------------------------%

output [
  "Envergure du projet  : ", show(fin_projet), "\n",
  "Début des tâches     : ", show(debut_tache), "\n",
  "Fin des tâches       : ", show(fin_tache), "\n",
];