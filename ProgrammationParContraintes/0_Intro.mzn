% NOM_ETUDIANT_1 (MATRICULE_1)
% NOM_ETUDIANT_2 (MATRICULE_2)

include "globals.mzn";

%-----------------------------------------------------------------------------%
% Variables de décisions
%-----------------------------------------------------------------------------%

% Nombre devant satisfaire les critères
var 1000..9999: nombre;

% Décomposition du nombre en un ensemble de chiffres
% Les digits sont dans l'intervalle de 1 a 9 donc pas de 0 pour la contrainte 2
array[1..4] of var 1..9: chiffres;

%-----------------------------------------------------------------------------%
% Objectif
%-----------------------------------------------------------------------------%

% Variable à minimiser
% Contrainte 8 : Le produit des 3 derniers chiffres (chiffre à la position des centaines×chiffre à la position des dizaines × chiffre à la position des unités) doit être minimisé.
var int: p = chiffres[2] * chiffres[3] * chiffres[4];

%-----------------------------------------------------------------------------%
% Partie étudiant
%-----------------------------------------------------------------------------%
constraint nombre = chiffres[1] * 1000 + chiffres[2] * 100 + chiffres[3] * 10 + chiffres[4];
% Contrainte 1 : C'est un nombre Paire
constraint chiffres[4] in {2, 4, 6, 8};
% Contrainte 2 : Pas de 0. Voir plus haut
% Contrainte 3 : Les 4 chiffres sont différents.
constraint all_different(chiffres);
% Contrainte 4 : Le chiffre à la position des milliers est supérieur à celui à la position des centaines.
constraint chiffres[1] >  chiffres[2];
% Contrainte 5 : Le chiffre à la position des dizaines est inférieur à celui à la position des unités.
constraint chiffres[3] <  chiffres[4];
% Contrainte 6 : Le chiffre à la position des centaines est supérieur à celui à la position des unités.
constraint chiffres[2] >  chiffres[4];
% Contrainte 7 : La somme des 4 chiffres est supérieure à 15.
constraint sum(chiffres) > 15;
% Contrainte 8 : Le produit des 3 derniers chiffres (chiffre à la position des centaines×chiffre à la position des dizaines × chiffre à la position des unités) doit être minimisé.
solve minimize p;
%-----------------------------------------------------------------------------%

output [
  show(nombre)
];

