# KARAKI 2402594
# LUQUET 2402133

from schedule import Schedule
import random
import math
import solver_naive

def solve(schedule):
    """

    :param schedule: object describing the input
    :return: a list of tuples of the form (c,t) where c is a course and t a time slot. 
    """

    # Cout (nombre de creneau + une constant fois le nombre de conflit)  
    def cost(solution):
        const_conflicts = 10
        nb_conflicts = sum(
            1 for course in schedule.course_list
                for conflict in schedule.get_node_conflicts(course)
                    if solution[course] == solution.get(conflict, -1)
        )
        cost = schedule.get_n_creneaux(solution) + const_conflicts * nb_conflicts
        return cost
    
    # Fonction de voisinage
    def fonction_voisinage(solution):

        course = random.choice(list(schedule.course_list))
        last_creaneau = max(solution.values())
        new_creaneau = random.randint(1, last_creaneau)

        return course, new_creaneau
    
    # Solution aleatoire 
    def random_solution(withConflicts = False):
        # Gerneation d'une solution aleatoire 
        solution = dict()

        # Liste des cours à assigner
        nodes = list(schedule.course_list)

        # Pour chaque cours, assigner un créneau horaire aléatoire
        for course in nodes:
            # On génère un créneau aléatoire, entre 1 et le nombre de cours
            creneau = random.randint(1, len(nodes))

            if not withConflicts :
                # Tant que le créneau est déjà utilisé par un cours en conflit, on génère un nouveau créneau
                conflicts = schedule.get_node_conflicts(course)
                while any(solution.get(conflict) == creneau for conflict in conflicts if conflict in solution):
                    creneau = random.randint(1, len(nodes))

            solution[course] = creneau

        return solution

    # Solution greedy
    def greedy():
        # Gerneation du solution greedy 
        gready_solution = dict()
        nodes = list(schedule.course_list)
        
        # Trie décroissant des cours avec le plus de conflits
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                # Si plus de conflit
                if schedule.conflict_graph.degree(nodes[i]) < schedule.conflict_graph.degree(nodes[j]):
                    nodes[i], nodes[j] = nodes[j], nodes[i]
    
        for course in nodes:
            # Pour chaque cours on recuper les cours en conflits avec celui-ci
            creneau_voisin = set()
            conflicts = schedule.get_node_conflicts(course)
            # print("Courses is :", course, "and conflicts ", conflicts)
            # On parcours tout les conflits pour savoir si on a deja assigner des cours ne conflits a la solution.
            # Si on la deja assigner cela veut dire qu'on ne peux utiliser ce creneau pour ce cours
            for c in conflicts:
                if c in gready_solution:  
                    creneau_voisin.add(gready_solution[c]) 

            #  print("     Creneau voisn is ", creneau_voisin)

            # On assigne le premier trou de creneau
            creneau = 1
            while creneau in creneau_voisin:
                creneau += 1
            gready_solution[course] = creneau
        return gready_solution
    
    def simulatedAnnealing(solution, t0=1, t_min=1e-4, alpha=0.995, max_iter=100000, max_no_improve=5000):
        """
        :param solution: initial solution
        :param t0:  Temperature initial
        :param t_min: Temperature Min
        :param alpha: Taux de decroissance (entre 0.8 et 0.99)
        :param max_iter: Max iterations
        :param max_no_improve: max d'itérations sans amélioration
        :return: the best solution found
        """
        no_improve_count = 0   # La solution ne s'améliore pas pendant max_no_improve itérations, on arrête

        current_solution = solution
        best_solution = solution.copy()
        # Cout Initial 
        current_cost = cost(current_solution)
        best_cost = current_cost

        t = t0
        iter = 0

        while t > t_min and iter < max_iter:
            iter += 1
            course, new_creaneau = fonction_voisinage(current_solution)
            # Pas de changement ==> next
            if new_creaneau == current_solution[course]:
                continue  
            
            # Creation d'une nouvelle solution
            new_solution = current_solution.copy() 
            new_solution[course] = new_creaneau
            
            # Calcule du cout de cette nouvelle solution
            new_cost = cost(new_solution)
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
    def local_restart_simulated(max_iteration_restart = 50): 
        best_solution_restart = random_solution(withConflicts=True)
        best_cost_restart = cost(best_solution_restart)

        for _ in range(max_iteration_restart):
            # generate first Solution 
            first_solution = random_solution(withConflicts=True)
            # executer un recherche par recuit simulé 
            solution, simul_cost = simulatedAnnealing(first_solution)

            if simul_cost < best_cost_restart:
                best_solution_restart = solution.copy()
                best_cost_restart = simul_cost
        return best_solution_restart, best_cost_restart

    #Test avec greedy et simulatedAnnealing
    solution_greedy = greedy()
    solution_greedy, greedy_cost = simulatedAnnealing(solution_greedy)

    # Test avec restart et simulatedAnnealing
    solution_restart, restart_cost = local_restart_simulated()

    #La meilleur solution reste avec le programme gready.
    if greedy_cost <= restart_cost:
        print("Greedy is better (with a little help of simulated Annealing)")
        return solution_greedy
    else:
        print("It's a win for Local search Algo")
        return solution_restart
    