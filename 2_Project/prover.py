import sys
import fileinput
import select

from resolution import Resolution

def parse_file():
    """ Parses the directed file to the function """

    knowledge_base = list()
    mode = 0;
    
    #Stdin has data
    #version to text the prover alone
    if select.select([sys.stdin,],[],[],0.0)[0]:
        mode = 1
        for line in fileinput.input():
            line_ = eval(line)
            knowledge_base.append(line_)

        if knowledge_base:
            return knowledge_base
        else:
            print("Provided file is empty")
            exit()
    
    #filters output use when we are considering the pipe
    #that uses converter.py and prover.py
    if mode == 0:
        for line in sys.stdin:
            line_ = eval(line)
            knowledge_base.append(line_)

        if knowledge_base:
            return knowledge_base
        else:
            print("Provided file is empty")
            exit()

    #Stdin has not input data
    #Exit softly
    else:
        print ("The CNF convertor should read from stdin sentences!")
        exit()

def main():
    """ Main Function. Calls every method needed to solve the problem"""

    file_content = parse_file()

    #applies resolution method using the Resolution class    
    resolution = Resolution(file_content);
    resolution.result();

if __name__ == '__main__':

    main()