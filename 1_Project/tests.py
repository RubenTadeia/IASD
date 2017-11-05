from os import listdir
import time

from functions import get_possible_actions
from functions import is_goal

from uninformed import uniform_cost_search
from informed import a_star

def test_functions():
    """ Test Functions """
    for file_ in listdir("tests"):
        if file_.split('.')[1] == "txt" and file_.split('.')[0]!="mir":
            
            print("Solving " + file_)
            
            initial_state = []
            problem = "tests/" + file_
            
            initial_time = time.time()

            uniform_cost_search(problem, initial_state, get_possible_actions, is_goal)    
            #a_star(problem, initial_state, get_possible_actions, is_goal)

            final_time = time.time()

            print("Solving " + file_ + " took {} seconds \n".format(final_time-initial_time))

if __name__ == '__main__':

    test_functions()