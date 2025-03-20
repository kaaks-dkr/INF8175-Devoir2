% NOM_ETUDIANT_1 (MATRICULE_1)
% NOM_ETUDIANT_2 (MATRICULE_2)

include "globals.mzn";

%-----------------------------------------------------------------------------%
% Données
%-----------------------------------------------------------------------------%

% Nombre d'acteurs et de rôles
int: n;
% Couleurs des costumes
enum costumes; 
% Costume démandé pour un rôle i (première dimension) par un acteur j (seconde dimension)
array[1..n,1..n] of costumes: choix_costume;

%-----------------------------------------------------------------------------%
% Variables de décisions
%-----------------------------------------------------------------------------%

% Variables de décision pour assigner un acteur à un rôle
array [1..n] of var 1..n: assignation_role;

%-----------------------------------------------------------------------------%
% Partie étudiant
%-----------------------------------------------------------------------------%
% Contrainte 1 : Attribuer un et un seul rôle à chaque acteur
constraint all_different(assignation_role);
% Contrainte 2 : Chaque acteur a un costume Unique
constraint alldifferent([choix_costume[assignation_role[i], i] | i in 1..n]);
% Contrainte 3 : Deux acteur ne doivent pas etre adjacent
constraint forall(i in 1..n-1)(abs(assignation_role[i] - assignation_role[i+1]) > 1); 
solve satisfy;
%-----------------------------------------------------------------------------%

output	
  ["L'acteur " ++ format(i) ++ 
   " prendra le rôle " ++ format(fix(assignation_role[i])) ++ 
   " (costume " ++ format(choix_costume[fix(assignation_role[i]), i]) ++ ")" ++"\n" 
  | i in 1..n];