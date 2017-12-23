from utils import txt_to_graph
from utils import all_subgraphs
from utils import get_set_launches_components
from functions import branching_factor
from functions import update_state
from functions import state_in_list
from functions import print_solution
from functions import path_cost_function

def uniform_cost_search(file_, initial_state, possible_actions, goal_function):
    """ Uniform Cost Search"""

    # Initialize frontier and explored list. Frontier is initialized with the initial state
    frontier = [initial_state]
    aux_frontier = [0]
    explored = []

    # Get the graph of the proposed launch and the dictionary of launches
    graph, launch_dict = txt_to_graph(file_)

    # Create a list with all the launches and all the components
    all_launches = list(launch_dict.keys())
    all_components = graph.get_vertices()

    # Define the goal state
    goal_state = set(all_components)

    # All_subgraphs
    possible_subgraphs = all_subgraphs(graph)

    # Flag that is set to active if a goal is found
    solution_found = 0

    # Auxiliary variables to deal with possible repeated values in the frontier
    aux_list_unique_sets = []
    costs_dict = dict()

    # Auxiliary costrs
    aux_cost = 0

    while frontier:

        # Pops a value from the frontier, which is the actual state
        min_index = aux_frontier.index(min(aux_frontier))

        cost = aux_frontier.pop(min_index)
        actual_state = frontier.pop(min_index)

        # Checked that the values being popped are increasing in value
        if cost < aux_cost:
            print("Path costs should be increasing not decreasing")
            exit()

        aux_cost = cost

        # Check if new state is solution
        if goal_function(actual_state, goal_state):

            """print("Found goal state!")
            print("Number of nodes explored: ", len(explored))
            print("Number of nodes still in frontier: ", len(frontier))

            b_factor = branching_factor(len(frontier)+len(explored), len(actual_state), 1)

            print("Branching factor is: ", b_factor)"""

            new_cost = path_cost_function(actual_state)
            solution = (actual_state, new_cost)
        
            print_solution(solution)

            solution_found = 1

            break
        
        # Adds the actual state to the explored list
        explored.append(actual_state)

        # Gets the list of possible actions for the actual state
        actions = possible_actions(graph, actual_state, all_components, 
                                   all_launches, launch_dict, possible_subgraphs)

        # Cycle through all the possible actions for a given state
        for action in actions:
            
            # Defines a new state according to the actual state and the action
            new_state = update_state(action, actual_state)

            # Check if the state is already in the explored
            if state_in_list(new_state, explored):
                continue

            # Calculate the path cost of the new state
            new_state_path_cost = path_cost_function(new_state)

            # Note that is not necessary to check if the state is in the frontier since every state is unique

            # In our state definition, different states may be expanded with the same combinations. So,
            # if this intermediate state is the same as other but has a lower cost, it will always be a
            # better solution. This next if and else represent the part of uniform cost search in which
            # we replace the value of a state in a frontier by one identic with lower cost
            aux_set_new_state = get_set_launches_components(new_state)

            if aux_set_new_state in aux_list_unique_sets:
                
                if costs_dict[frozenset(aux_set_new_state)] > new_state_path_cost:
                    for index, state_ in enumerate(frontier):
                        if get_set_launches_components(state_) == aux_set_new_state:
                            costs_dict[frozenset(aux_set_new_state)] = new_state_path_cost
                            frontier.remove(state_)
                            frontier.append(new_state)
                            del aux_frontier[index]
                            aux_frontier.append(new_state_path_cost)
                            break

            else:
                frontier.append(new_state)
                aux_frontier.append(new_state_path_cost)
                aux_list_unique_sets.append(aux_set_new_state)
                costs_dict[frozenset(aux_set_new_state)] = new_state_path_cost

    if not solution_found:
        print(0)

def decoy_main():
    """ Defining the main just to avoid running anything when importing this """
    pass

if __name__ == '__decoy_main__':

    decoy_main()
