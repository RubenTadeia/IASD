import itertools

from classes import Graph

from utils import total_weight
from utils import get_launches_lists

def get_possible_actions(graph, state, components, launches, launch_dict, poss_subg):
    """ Creates the possible states """

    def aux_possible_actions(extra_earth, combination, launches_, last_date):
        """ Function that receives a tuple with a combination of components and returns a list with all the 
        tuples that are possible actions, already including the specific launch and the total cost """
        
        assert isinstance(extra_earth, set)
        assert isinstance(combination, tuple) or isinstance(combination, str)
        assert isinstance(launches_, list)
        assert isinstance(last_date, str)

        aux_list = []

        if combination != "END":
            # Get the total weight of the combination of components
            weight = total_weight(graph, combination)

            # Calculate the payload of the remanescent launches
            payld = 0
            launch_payload_dict = dict()
            for aux_launch in launches_:
                payld += aux_launch[1]
                launch_payload_dict[aux_launch[0]] = aux_launch[1]

            # Calculate the total weight of the remanescent components on earth
            extra_comp_weight = total_weight(graph, tuple(extra_earth))

            # Conver the last date to hours
            last_y = last_date[4:]; last_m = last_date[2:4]; last_d = last_date[0:2]
            last_ = float(last_d) * 24 + float(last_m) * 720 + float(last_y) * 8760

            for launch in launches_:

                # Get the payload value for all the remaining launches
                payld_ = payld - launch_payload_dict[launch[0]]

                # If the weight of all the extra components that stay in earth fit the launches after
                # this one is launched, then this path may contain a solution to the problem
                if extra_comp_weight <= payld_:

                    # If the cargo weight is less than the maximum payload, then we can count this as
                    # a possible action
                    if weight <= launch[1]:
                        # Add the launch date to the combination
                        aux_combination = (launch[0],) + combination
                        # Define the cost of the launch and add it to the combination
                        cost = launch[2] + weight * launch[3]
                        aux_combination += (cost, )

                        # Added constraint: Only append if the date is bigger than the actual data
                        this_y = aux_combination[0][4:]; this_m = aux_combination[0][2:4]; this_d = aux_combination[0][0:2]
                        this_ = float(this_d) * 24 + float(this_m) * 720 + float(this_y) * 8760

                        # Append the extended combination to the auxiliary list
                        if last_ <= this_:
                            aux_list.append(aux_combination)

                    else:
                        # Since the launch list is ordered from the largest payload to the smallest
                        # payload, if a given launch fails to meet this requirement, all the subsequent
                        # will fail as well
                        break

            return aux_list

        else:

            return False

    # Assert that the given variables are correct
    assert isinstance(graph, Graph), "graph variable should be of type Graph"
    assert isinstance(state, list), "state variable should be of type list"
    assert isinstance(components, list), "scomponents variable should be of type list"
    assert isinstance(launches, list), "launches variable should be of type list"
    assert isinstance(launch_dict, dict), "launch_dict variable should be of type dict"

    # List that will contain the list of possible actions based on the current state
    list_possible_actions = []

    # Store actual state latest launch date
    last_date = '00000000'
    #If list has values
    if state:
        last_date = state[-1][0]
    
    # Retrieve information from the states
    space_components = set()
    used_launches = set()

    for action in state:
        already_used_launch = action[0]
        already_sent_space_components = action[1]
        used_launches.add(already_used_launch)
        space_components = space_components | set(already_sent_space_components)

    # Make the list with the earth components. They will be a list that is the difference between
    # the set with every component minus the ones that are already in space
    earth_components = list(set(components).difference(space_components))
    
    # Make the list with the available launches ordered from maximum payload to minimum
    available_launches = list(set(launches).difference(used_launches))
    available_launches = get_launches_lists(available_launches, launch_dict)

    # If there are no launches availbale no need to waste time doing the rest
    if len(available_launches) == 0:
        return []

    # Cycle to obtain the possible states
    for i in range(1, len(earth_components)+1):

        # If there is only one launch available, launches with less than all the number of
        # components are useless, since they won't lead to the goal state
        if len(available_launches) == 1:
            if i != len(earth_components):
                continue

        # Define the function that generates the possible combinations
        component_combinations = itertools.combinations(earth_components, i)

        # Obtain the first combination
        combination = next(component_combinations, "END")

        # Make new auxiliary set with the combination and the space components and check if its possible
        aux_set = set()
        for aux_value in combination:
            aux_set = aux_set | {aux_value}
        aux_set_space = aux_set | space_components

        if aux_set_space in poss_subg:

            # Extra components on earth
            extra_earth_components = set(earth_components).difference(combination)

            # Get an auxiliary list of possible states, already with launches
            aux_list_actions = aux_possible_actions(extra_earth_components, combination, available_launches, last_date)

            # If the auxiliary list of legal possible actions exist, add them to the list of
            # all possible actions that is returned in the end
            if aux_list_actions:

                [list_possible_actions.append(comb) for comb in aux_list_actions]

        # Obtain combinations and possible actions as long as the generator yields them
        while combination != "END":

            combination = next(component_combinations, "END")

            # Make new auxiliary set with the combination and the space components and check if its possible
            aux_set = set()
            for aux_value in combination:
                aux_set = aux_set | {aux_value}

            aux_set_space = aux_set | space_components
            
            if aux_set_space in poss_subg:

                # Extra components on earth
                extra_earth_components = set(earth_components).difference(combination)

                aux_list_actions = aux_possible_actions(extra_earth_components, combination, available_launches, last_date)

                if aux_list_actions:

                    [list_possible_actions.append(comb) for comb in aux_list_actions]

    return list_possible_actions


def is_goal(state, goal_state):
    """ Returns true if the goal state is achieved """

    assert isinstance(state, list), "state variable should be of type list"
    assert isinstance(goal_state, set), "goal_satate variable should be of type set"

    space_components = set()

    for action in state:
        already_sent_space_components = action[1]
        space_components = space_components | already_sent_space_components

    if space_components == goal_state:
        return True
    
    return False


def update_state(action, previous_state):
    """ Returns a new state from a previous one, based on a given action """

    assert isinstance(action, tuple)
    assert isinstance(previous_state, list)

    aux_list = previous_state[:]

    aux_list.append((action[0], set(action[1:-1]), action[-1]))

    return aux_list


def state_in_list(state, list_to_test):
    """ Returns true if a state is in a list, false otherwise """

    assert isinstance(state, list)
    assert isinstance(list_to_test, list)

    return state in list_to_test


def print_solution(solution):
    """ Prints the solution in the pretended format """
    
    assert isinstance(solution, tuple)
    
    for action in solution[0]:
        print(action[0], end='  ')
        for component in action[1]:
            print(component, end=' ')
        print(' ', action[-1])
    print(solution[-1])
    

def path_cost_function(state):
    """ Returns the total cost of a given path (state) """ 

    new_cost = 0

    for action_ in state:
        new_cost += action_[-1]

    return new_cost


def branching_factor(nodes_expanded, goal_depth, tol):
    """ Function that prints the branching factor """

    def aux_branching_factor(N, b, d, tolerance):
        """ Auxiliary function to calculate the branching factor """

        aux_value = 0
        for i in range(1, d+1):
            aux_value += b**i

        if N < aux_value + tolerance and N > aux_value-tolerance:
            return True
        else:
            return False

    def frange(init, maximum, step):
        """ Range that works with floats """
        while init < maximum:
            yield init
            init += step

    tol = tol

    for b in frange(0, 150.0, 0.0001):

        result = aux_branching_factor(nodes_expanded, b, goal_depth, tol)

        if result:
            return b


def decoy_main():
    """ Defining the main just to avoid running anything when importing this """
    pass


if __name__ == '__decoy_main__':

    decoy_main()
