#KARAKI Ali 2402594

from schedule import Schedule
from random import choice
from math import exp

""" Ce problème correspond au problème connu de coloriage de graphe pour lequel on ne connaît pas d'algorithme
    capable de le résoudre en temps polynômial.
    
    Il existe plusieurs approches pour résoudre ce problème comme vu dans le cours INF8775
    
    L'approche que l'on utilise est de commencer par colorier notre graphe avec une approche vorace, puis essayer
    de faire des améliorations locales dans des voisinages intéressants.
    
    Nos candidats pour l'approche vorace sont les sommets ayant le plus grand ndegré de saturation
    On s'inspire de l'algorithme D-satur pour implémenter cette approche gloutonne dans un premier temps
"""

def solve(schedule: Schedule):
    """
    Your solution of the problem
    :param schedule: object describing the input
    :return: a list of tuples of the form (c,t) where c is a course and t a time slot. 
    """
    # Add here your agent
    solution_base = greedy(schedule)
    solution_improved = local_improvements(schedule, solution_base)
    return solution_improved


"""
Cette fonction essaie de trouver des améliorations locales pour une solution courante
Elle utilise le simulated anealing vu en cours pour sélectionner des solutions permettant d'échapper à des minima locaux
"""
def local_improvements(schedule: Schedule, initial_solution, temperature = 0.9, cooling_rate = 0.991, it_number = 30000):
    solution = initial_solution
    for _ in range(it_number):
        #choisir autrement que aléatoirement?
        new_node = choice(list(solution.keys()))
        neighbour_colors = set()
        for neighbour in schedule.get_node_conflicts(new_node):
            if(neighbour in solution):
                neighbour_colors.add(solution[neighbour])

        old_color = solution[new_node]
        new_color = find_smallest(list(neighbour_colors))
        old_score = eval(solution, schedule)
        solution[new_node] = new_color
        new_score = eval(solution, schedule)
        
        
        if(new_score == -1):
            solution[new_node] = old_color
        else:
            if(new_score > old_score):
                prob = exp((old_score - new_score)/temperature)
                solution[new_node] = choice([new_color, old_color], [prob, 1-prob])
        temperature *= cooling_rate
    return solution

"""
Cette fonction vérifie si une solution est valide ou non
Elle est tirée de la classe schedule mais implémentée ici pour éviter l'instruction assert 
"""
def verify_solution(solution, schedule: Schedule):
    return sum(solution[a[0]] == solution[a[1]] for a in schedule.conflict_list) == 0

"""
Cette fonction est une fonction d'évaluation de la solution courante
"""
def eval(solution, schedule: Schedule) -> int:
    if(not verify_solution(solution, schedule)):
        return -1
    return schedule.get_n_creneaux(solution)


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