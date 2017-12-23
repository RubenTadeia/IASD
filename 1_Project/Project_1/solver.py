import sys

from functions import get_possible_actions
from functions import is_goal

from informed import a_star
from uninformed import uniform_cost_search


def main():
    """ Main """

    if len(sys.argv) != 3:
    	print("Invalid number of arguments. Please run as Example: python3 solver.py -i example.txt")
    	exit()

    initial_state = []

    search_method = sys.argv[1]

    problem = sys.argv[2]

    #Uninformed search method
    if search_method == "-u": 
        
        uniform_cost_search(problem, initial_state, get_possible_actions, is_goal)

    #Informed search method
    elif search_method == "-i":

        a_star(problem, initial_state, get_possible_actions, is_goal)

    else:
        print("Not a valid search method. Example: python3 solver.py -i example.txt")

if __name__ == '__main__':

    main()
    
