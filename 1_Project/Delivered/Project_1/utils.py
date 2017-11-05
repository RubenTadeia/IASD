import itertools
from collections import defaultdict

from classes import Launch
from classes import Graph

def txt_to_graph(txt):
    """ Creates a graph from a text file """

    def check_its_numeric(value):
        """ Asserts that a value is numeric """
        assert not value.islower() and not value.isupper(), "there are letters in the weight variable"
        assert float(value) >= 0,"Value has to be higher or equal to zero"
        return float(value)

    # Initialize the graph
    graph = Graph()

    try:

        # Parsing the file regarding vertices first - this way because they can appear in any order
        for line in open(txt):

            line_split = line.strip('\n').split()

            # To avoid parsing the empty lines
            if line_split:

                # Deal with the vertices
                if line_split[0][0] == 'V':

                    # Verify that we are only receiving two values on the vertices
                    assert len(line_split) == 2, "number of variables in the line should be 2"

                    # Read the name of the component
                    name = line_split[0][0:]
                    assert isinstance(name, str), "name should have the type string"
                
                    # Read the weight of the component
                    weight = line_split[1]
                    weight = check_its_numeric(weight)

                    # Add the component as vertice of the graph
                    graph.add_vertice(name, weight)

    except IOError:
        print ("File %s does not exist" % txt)
        exit()

    # Create a dictionary to hold the launch structures
    launches_dictionary = dict()

    # Parsing the file regarding edges and launches
    for line in open(txt):

        line_split = line.strip('\n').split()

        # To avoid parsing the empty lines
        if line_split:

            # Deal with the edges
            if line_split[0][0] == 'E':

                # Verifty that we have three elements on the line
                assert len(line_split) == 3, "number of variables in the line should be 3"

                # Read the name of the two components
                name1 = line_split[1][0:]
                name2 = line_split[2][0:]
                assert isinstance(name1, str), "name of the first"
                assert isinstance(name2, str)

                # Adding the edges to the graph
                graph.add_edge(name1, name2)
                graph.add_edge(name2, name1)

            # Deal with launches
            if line_split[0][0] == 'L':

                # Verify that we have five elements on the line
                assert len(line_split) == 5, "number of variables in the line should be 5"

                # Read the name of the variables
                date = line_split[1]
                assert isinstance(date, str), "date of the launch should be a string"

                max_payload = line_split[2]
                max_payload = check_its_numeric(max_payload)

                fixed_cost = line_split[3]
                fixed_cost = check_its_numeric(fixed_cost)

                var_cost = line_split[4]
                var_cost = check_its_numeric(var_cost)

                # Add structure to the dictionary of launches
                launches_dictionary[date] = Launch(max_payload, fixed_cost, var_cost)

    return graph, launches_dictionary 

def get_launches_lists(launches, launches_dict):
    """ Creates list with tuples with all the info for the components and the launches """

    # Verify that the variable types are correct
    assert isinstance(launches, list), "list variable has to be of type list"
    assert isinstance(launches_dict, dict), "launch variable has to be of type Dict"

    launches = [(date, launches_dict[date].max_payload, launches_dict[date].fixed_cost, \
                 launches_dict[date].var_cost) for date in launches]

    return sorted(launches, key=lambda x: x[1], reverse=True)

def total_weight(graph, combination):
    """ Returns the total weight of a tuple of components """

    assert isinstance(graph, Graph)
    assert isinstance(combination, tuple)

    tot_weight = 0

    for combination_component_name in combination:
        tot_weight += graph.structure[combination_component_name][0]

    return tot_weight

def all_subgraphs(graph):
    """ Returns a list with all the complete subgraphs of a graph """

    assert isinstance(graph, Graph)

    def algo(graph, start):
        """ Returns list with some subtrees of a tree starting in a certain node """

        # Create a dictionary with the parents
        explored = []
        stack = [ start ]
        parent_dict = defaultdict(lambda:0)

        while stack:

            parent = stack.pop(0)

            if parent in explored:
                continue
        
            explored.append(parent)

            children = graph.structure[parent][1:]

            for child in children:

                if child not in explored:
                    stack.insert(0, child)
                    parent_dict[child] = parent

        # Create intermediate dictionary
        combs_dict = dict()

        graph_structure = graph.structure

        for key in graph_structure:
            for i in range(1, len(graph_structure[key])+1):

                combs = itertools.combinations(graph_structure[key][1:], i)
                next_comb = next(combs, "END")

                if next_comb != "END":

                    next_comb += (key, )
                    next_comb = set(next_comb)

                    if key in combs_dict.keys():
                        combs_dict[key].append(next_comb)
                    else:
                        combs_dict[key] = [next_comb]

                while next_comb != "END":
                    
                    next_comb = next(combs, "END")

                    if next_comb != "END":

                        next_comb += (key, )
                        next_comb = set(next_comb)

                        if key in combs_dict.keys():
                            combs_dict[key].append(next_comb)
                        else:
                            combs_dict[key] = [next_comb]

        # Create final list
        possible_subgraphs = []

        graph_structure_ = dict()

        for key in graph_structure:
            graph_structure_[key] = graph_structure[key][1:]

        for vertix in graph.get_vertices():
            for child in combs_dict[vertix]:
                if child not in possible_subgraphs:
                    possible_subgraphs.append(child)
                for aux_vertix in graph_structure_[vertix]:
                    for aux_child in combs_dict[aux_vertix]:
                        new_comb = aux_child | child
                        if new_comb not in possible_subgraphs:
                            possible_subgraphs.append(new_comb)

        return possible_subgraphs

    # Main of this function
    subgraphs = []
    graph_structure = dict()
    
    for key in graph.structure:
        graph_structure[key] = graph.structure[key][1:]

    vertices = graph.get_vertices()

    for vertix in vertices:

        # Append the ones from the algorithm
        aux_subgraph = algo(graph, vertix)
        # Append the unique vertices
        aux_subgraph.append({vertix})
        # Append the whole graph
        aux_subgraph.append(set(vertices))

        for set_ in aux_subgraph:
            if set_ not in subgraphs:
                subgraphs.append(set_)

    subgraphs_ = list()
    
    # Union of subtrees with non-null intersections
    for subgraph in subgraphs:
        for aux_subgraph in subgraphs:
            if subgraph & aux_subgraph != set():
                new_thing = subgraph | aux_subgraph
                if new_thing not in subgraphs_:
                    subgraphs_.append(new_thing)

    for subgraph in subgraphs_:
        subgraphs.append(subgraph)

    return subgraphs    

def get_set_launches_components(state):
    """ Returns a set with the launches and components of a state """

    aux_set = set()

    for action in state:
        aux_set = aux_set | {action[0]} | action [1]

    return aux_set