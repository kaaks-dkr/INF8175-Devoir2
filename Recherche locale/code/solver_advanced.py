# KARAKI 2402594
# LUQUET 2402133

from schedule import Schedule
import random
import math
import solver_naive

""" Ce problème correspond au problème connu de coloriage de graphe pour lequel on ne connaît pas d'algorithme
    capable de le résoudre en temps polynômial.
    
    Il existe plusieurs approches pour résoudre ce problème comme vu dans le cours INF8775
    
    L'approche que l'on utilise est de commencer par colorier notre graphe avec une approche vorace, puis essayer
    de faire des améliorations locales dans des voisinages intéressants.
    
    Nos candidats pour l'approche vorace sont les sommets ayant le plus grand ndegré de saturation
    On s'inspire de l'algorithme D-satur pour implémenter cette approche gloutonne dans un premier temps
"""

def solve(schedule):
    """
    Your solution of the problem
    :param schedule: object describing the input
    :return: a list of tuples of the form (c,t) where c is a course and t a time slot. 
    """

    #Test avec greedy et simulatedAnnealing
    solution_greedy = greedy(schedule)
    solution_greedy_Annealing, greedy_annealing_cost = simulatedAnnealing(schedule, solution_greedy)

    # Test avec restart et simulatedAnnealing*
    print("Local search avec restart et simulated Annealing (cela peut prendre un peu de temps (max_iteration_restart = 50 et Annealing max_iter=100000))")
    solution_restart, restart_cost = local_restart_Annealing(schedule)

    #La meilleur solution reste avec le programme gready (et Annealing).
    if greedy_annealing_cost <= restart_cost:
        print("Greedy is better (with a little help of simulated Annealing)")
        return solution_greedy_Annealing
    else:
        print("It's a win for Local search Algo")
        return solution_restart


"""
Cette fonction retourne une solution gloutonne au problème de coloriage de graphe
Elle utilise l'algorithme D-SATUR vu en cours de INF8775 afin de résoudre le problème

Source: wikipedia: D-SATUR
Ordonner les sommets par ordre décroissant de degrés.
Colorer un sommet de degré maximum avec la couleur 1.
Choisir un sommet avec DSAT maximum. En cas d'égalité, choisir un sommet de degré maximal.
Colorer ce sommet avec la plus petite couleur possible.
Si tous les sommets sont colorés alors stop. Sinon aller en 3.
"""
def greedy(schedule: Schedule):
        
    """On commence par trier les nodes dans l'ordre décroissant de leur degré"""
    nodes_sorted = sorted(schedule.conflict_graph.degree, key=lambda x: x[1], reverse=True)
    nodes = [nodes_sorted[i][0] for i in range(len(nodes_sorted))]
    
    solution = dict()
        
    colors = {}
    colors[nodes[0]] = 1
    nodes = nodes[1:]
        
    while nodes:
        dsat_nodes = {}
        for node in nodes:
            dsat_nodes[node] = dsat(node, schedule, colors)
        
        target_node = max(dsat_nodes, key=dsat_nodes.get)
        neighbor_colors = []
        for neighbor in schedule.get_node_conflicts(target_node):
            if(neighbor in colors):
                if(colors[neighbor] not in neighbor_colors):
                    neighbor_colors.append(colors[neighbor])
        if not neighbor_colors:
            colors[target_node] = 1
        else:
            colors[target_node] = find_smallest(neighbor_colors)
        nodes.remove(target_node)
            
    for node in schedule.course_list:
        solution[node] = colors[node]
        
    return solution

"""
Cette fonction essaie de trouver des améliorations locales pour une solution courante
Elle utilise le simulated anealing vu en cours pour sélectionner des solutions permettant d'échapper à des minima locaux
"""
def simulatedAnnealing(schedule: Schedule, solution, t0=1, t_min=1e-4, alpha=0.995, max_iter=100000, max_no_improve=5000):
    """
    :param solution: initial solution
    :param t0:  Temperature initial
    :param t_min: Temperature Min
    :param alpha: Taux de decroissance (entre 0.8 et 0.99)
    :param max_iter: Max iterations
    :param max_no_improve: max d'itérations sans amélioration
    :return: la meilleur solution et son cout
    """
    no_improve_count = 0   # La solution ne s'améliore pas pendant max_no_improve itérations, on arrête

    current_solution = solution
    best_solution = solution.copy()
    # Cout Initial 
    current_cost = cost(schedule, current_solution)
    best_cost = current_cost

    t = t0
    iter = 0

    while t > t_min and iter < max_iter:
        iter += 1
        course, new_creaneau = fonction_voisinage(schedule, current_solution)
        # Pas de changement ==> next
        if new_creaneau == current_solution[course]:
            continue  
            
        # Creation d'une nouvelle solution
        new_solution = current_solution.copy() 
        new_solution[course] = new_creaneau
            
        # Calcule du cout de cette nouvelle solution
        new_cost = cost(schedule, new_solution)
        delta = new_cost - current_cost

        # Sélection en cas de non-dégradation ou dégradation avec une certaine probabilité
        if delta < 0 or random.random() < math.exp(-delta / t):
            current_solution = new_solution
            current_cost = new_cost
            # Si on a la meilleur solution on la garde
            if current_cost < best_cost:
                best_solution = new_solution.copy()
                best_cost = current_cost
            else:
                no_improve_count += 1
        else:
            no_improve_count += 1

        # Arrêt anticipé si aucune amélioration 
        if no_improve_count >= max_no_improve:
            break
        # Mise a jour de la temperature
        t = alpha * t
    return best_solution, best_cost
    
# Local search avec restart et simulatedAnnealing
def local_restart_Annealing(schedule: Schedule, max_iteration_restart = 50): 

    best_solution_restart = random_solution(schedule, withConflicts=True)
    best_cost_restart = cost(schedule, best_solution_restart)

    for _ in range(max_iteration_restart):
        # generate first Solution 
        first_solution = random_solution(schedule, withConflicts=True)
        # executer un recherche par recuit simulé 
        solution, simul_cost = simulatedAnnealing(schedule, first_solution)

        if simul_cost < best_cost_restart:
            best_solution_restart = solution.copy()
            best_cost_restart = simul_cost
    return best_solution_restart, best_cost_restart

# Fonction de Cout (nombre de creneau + une constant fois le nombre de conflit)  
def cost(schedule: Schedule, solution, const_conflicts = 10):
    nb_conflicts = 0
    # On compte le nombre de conflit
    for course in schedule.course_list:
        for conflict in schedule.get_node_conflicts(course):
            if solution[course] == solution.get(conflict, -1):
                nb_conflicts += 1
    cost = schedule.get_n_creneaux(solution) + const_conflicts * nb_conflicts
    return cost
    
# Fonction de voisinage
def fonction_voisinage(schedule: Schedule, solution):
    course = random.choice(list(schedule.course_list))
    last_creaneau = max(solution.values())
    new_creaneau = random.randint(1, last_creaneau)

    return course, new_creaneau
    
# Solution aleatoire 
def random_solution(schedule: Schedule, withConflicts = False):
    # Gerneation d'une solution aleatoire 
    solution = dict()

    # Liste des cours à assigner
    nodes = list(schedule.course_list)

    # Pour chaque cours, assigner un créneau horaire aléatoire
    for course in nodes:
        # On génère un créneau aléatoire, entre 1 et le nombre de cours
        creneau = random.randint(1, len(nodes))

        # Si on ne veut une soliton sans conflit
        if not withConflicts :
            # Tant que le créneau est déjà utilisé par un cours en conflit, on génère un nouveau créneau
            conflicts = schedule.get_node_conflicts(course)

            still_conflict = True
            while still_conflict:
                still_conflict = False
                # On verifie si le creneau est deja utiliser par un cours en conflit
                for conflict in conflicts:
                    if conflict in solution and solution[conflict] == creneau:
                        still_conflict = True
                        break
                if still_conflict:
                    # On genere un nouveau creneau
                    creneau = random.randint(1, len(nodes))

        solution[course] = creneau

    return solution

"""
Cette fonction trouve la plus petite couleur qu'il est possible de donner à un sommet ayant des voisins
de couleurs différentes
"""
def find_smallest(neighbours : list[int]) -> int:
    neighbours.sort()
    color = 1
    for neighbour in neighbours:
        if(neighbour > color):
            return color
        color +=1
    return color
    
"""
Cette fonction est l'implémentation de la fonction Dsat:
DSAT(v)= nombre de couleurs différentes dans les sommets adjacents à v 
source: Wikipedia D-SATUR
"""
def dsat(node, schedule: Schedule, colors) -> int:
    colors_tested = []
    neighbors = schedule.get_node_conflicts(node)
    for neighbor in neighbors:
        if neighbor in colors:
            if colors[neighbor] not in colors_tested:
                colors_tested.append(colors[neighbor])
    return len(colors_tested)
    