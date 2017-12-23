class Launch:
    """ Creates the Launch class.

        Inputs:
        launch_date -- string with the date in format DDMMYYYY of the launch
        max_payload -- float with the value of the maximum payload of the launch
        fixed_cost -- float with the value of the fixed cost of the launch
        var_cost -- float with the variable cost (per weight) of the launch

        Methods:
        print_information -- prints the data from a given launch """

    def __init__(self, max_payload, fixed_cost, var_cost):
        # Verify that all variables have the right type
        assert isinstance(max_payload, float), "maximum payload has to be initialized with a float"
        assert isinstance(fixed_cost, float), "fixed cost has to be initialized with a float"
        assert isinstance(var_cost, float), "variable cost has to be initialized with a float"

        self.max_payload = max_payload
        self.fixed_cost = fixed_cost
        self.var_cost = var_cost

    def print_information(self):
        """ Prints information of a given launch object """

        print("max_payload: ", self.max_payload)
        print("fixed_cost: ", self.fixed_cost)
        print("variable_cost: ", self.var_cost)


class Graph:
    """ Creates the class Graph. Vertices are Component objects. The added edges are names of components.

    Inputs:
    none

    Methods:
    add_vertice -- adds a vertice to the graph
    get_vertices -- return a list with the names of the vertices of the graph
    add_edge -- adds the name of a component to whom the vertice is connected to
    print_graph -- prints the graph
    print_vertices -- prints the names of the vertices on the graph
    print_edges -- print the names of the components connected to a given vertice"""

    def __init__(self):

        self.structure = dict()

    # Functions dealing with vertices
    def add_vertice(self, new_vertice, weight):
        """ Adds a new vertice to the graph """

        assert isinstance(new_vertice, str), "name of the vertice to add has to be a Component object"

        if new_vertice not in self.structure.keys():
            self.structure[new_vertice] = tuple()
            self.structure[new_vertice] += (weight,)
        else:
            print("The vertice is already in the graph")

    def get_vertices(self):
        """ Returns a list with all the vertices names """

        return [key for key in self.structure] 

    # Functions dealing with edges
    def add_edge(self, vertice, new_edge):
        """ Adds a new connection to the object Component """

        # Verify that variables have the right type
        assert isinstance(new_edge, str), "name of the edge to add has to be a string"
        
        self.structure[vertice] += (new_edge, )

    # Functions dealing with prints
    def print_graph(self):
        """ Print the whole dictionary """
        
        print("graph is:")

        for key in self.structure:

            print("{}: ".format(key), end="")
            print(self.structure[key])

    def print_vertices(self):
        """ Print all vertices """

        print("\nvertices of the graph are: ")
        
        for key in self.structure:
            print(key, end=', ')

        print("END_OF_VERTICES")

    def print_edges(self, vertice):
        """ Print self connections """

        print("\nvertices connected to {} are: ".format(vertice))

        for key in self.structure:
            if key == vertice:
                print(self.structure[key][1:])
                break
