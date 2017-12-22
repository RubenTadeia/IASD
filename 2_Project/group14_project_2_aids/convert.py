import fileinput
import copy
import sys

from classes import Tree

def parse_file():
    """ Parses the directed file to the function """

    knowledge_base = list()

    # Add each line of the file to the knowledge base
    for line in fileinput.input():
        line_ = eval(line)
        knowledge_base.append(line_)

    # If the file was empty, warn the user and exit the program
    if knowledge_base:
        return knowledge_base
    else:
        print("Provided file is empty")
        exit()


def check_its_atom(tree):
    """ Check if the root of a tree is an atom """

    forbidden = ["<=>", "=>", "not", "or", "and"]

    # If the root of the tree is not of any of the other possible operators
    # and if it is correctly terminated with None childs, then it is an atom
    if tree.get_root_data() not in forbidden:
        if tree.left is None and tree.right is None:
            return True

    return False


def apply_recursion(tree, node_type):
    """ Applies recursion on the tree for nodes of a certain type """

    if tree.data == node_type:
        if node_type == "<=>":
            tree = convert_equivalence(tree)
        elif node_type == "=>":
            tree = convert_implication(tree)
        elif node_type == "not":
            tree = convert_negation(tree)
        elif node_type == "or":
            tree = convert_disjunction(tree)

    if tree.left is not None:
        if node_type == "<=>":
            tree.left = apply_recursion(tree.left, "<=>")
        elif node_type == "=>":
            tree.left = apply_recursion(tree.left, "=>")
        elif node_type == "not":
            tree.left = apply_recursion(tree.left, "not")
        elif node_type == "or":
            tree.left = apply_recursion(tree.left, "or")

    if tree.right is not None:
        if node_type == "<=>":
            tree.right = apply_recursion(tree.right, "<=>")
        elif node_type == "=>":
            tree.right = apply_recursion(tree.right, "=>")
        elif node_type == "not":
            tree.right = apply_recursion(tree.right, "not")
        elif node_type == "or":
            tree.right = apply_recursion(tree.right, "or")

    return tree


def convert_equivalence(tree):
    """ Returns a new tree with the all equivalences converted
        A <=> B is equivalent to (A => B) and (B => A) """

    aux_tree = copy.deepcopy(tree)
    tree.insert_left('=>')
    tree.left.right = aux_tree.right
    tree.insert_right('=>')
    tree.right.right = aux_tree.left
    tree.change_root_data('and')

    return tree


def convert_implication(tree):
    """ Convert implication to disjunction
        A => B is equivalent to (not A) or B """

    tree.insert_left('not')
    tree.change_root_data('or')

    return tree


def convert_negation(tree):
    """ Convert negations
        1. not(not A) is equivalent to A
        2. neg(A or B) is equivalent to (neg A and neg B)
        3. neg(A and B) is equivalent to (neg A or neg B)"""

    # Converting following nots
    if tree.left.data == 'not':
        aux_tree = copy.deepcopy(tree)
        tree.change_root_data(tree.left.left.data)

        if isinstance(aux_tree.left.left.left, Tree):
            tree.left = Tree(aux_tree.left.left.left)
        else:
            tree.left = None

        if isinstance(aux_tree.left.left.right, Tree):
            tree.right = Tree(aux_tree.left.left.right)
        else:
            tree.right = None

    # Converting ANDs and ORs
    elif tree.left.data == 'or':
        tree.change_root_data('and')
        tree.left.change_root_data('not')
        tree.right = Tree(('not', 'X'))
        tree.right.left = copy.deepcopy(tree.left.right)
        tree.left.right = None

    elif tree.left.data == 'and':
        tree.change_root_data('or')
        tree.left.change_root_data('not')
        tree.right = Tree(('not', 'X'))
        tree.right.left = copy.deepcopy(tree.left.right)
        tree.left.right = None

    return tree


def convert_disjunction(tree):
    """ Convert disjunctions (apply distributive law) to get conjunctions of disjunctions
        1. A or (B and C) is equivalent to (A or B) and (A or C)
        2. (A and B) or (C and D) is equivalent to (A or C) and (A or D) and (B or C) and (B or D)"""

    # Left and, right atom or negation
    if tree.left.data == 'and' and (check_its_atom(tree.right) or tree.right.data == 'not'):
        aux_tree = copy.deepcopy(tree)
        tree.change_root_data('and')
        tree.left.change_root_data('or')
        tree.right.change_root_data('or')
        tree.right.left = copy.deepcopy(tree.left.right)
        tree.left.right = Tree(aux_tree.right)
        tree.right.right = Tree(aux_tree.right)

    # Left atom or negation, right and
    elif (check_its_atom(tree.left) or tree.left.data == 'not') and tree.right.data == 'and':
        aux_tree = copy.deepcopy(tree)
        tree.change_root_data('and')
        tree.left.change_root_data('or')
        tree.right.change_root_data('or')
        tree.left.left = copy.deepcopy(tree.right.right)
        tree.left.right = Tree(aux_tree.left)
        tree.right.right = Tree(aux_tree.left)

    # Both ands
    elif tree.left.data == 'and' and tree.right.data == 'and':
        aux_tree = copy.deepcopy(tree)
        tree.change_root_data('and')
        # Define the following root nodes
        tree.left.left.change_root_data('or')
        tree.left.right.change_root_data('or')
        tree.right.left.change_root_data('or')
        tree.right.right.change_root_data('or')
        # Populate the ors
        tree.left.left.left = Tree(aux_tree.left.left)
        tree.left.right.left = Tree(aux_tree.left.left)
        tree.left.left.right = Tree(aux_tree.right.left)
        tree.right.left.right = Tree(aux_tree.right.left)
        tree.left.right.right = Tree(aux_tree.right.right)
        tree.right.right.right = Tree(aux_tree.right.right)
        tree.right.left.left = Tree(aux_tree.left.right)
        tree.right.right.left = Tree(aux_tree.left.right)

    # If there are ORs with nested ANDs
    elif tree.left.data == 'and' and tree.right.data == 'or' and check_its_atom(tree.right.left) and check_its_atom(tree.right.right):
        aux_tree = copy.deepcopy(tree)
        tree.change_root_data('and')
        # Define the following root nodes
        tree.left.change_root_data('or')
        tree.right.change_root_data('or')
        # Populate the ors
        tree.left.left = Tree(aux_tree.right.left)
        tree.left.right.change_root_data('or')
        tree.left.right.left = Tree(aux_tree.right.right)
        tree.left.right.right = Tree(aux_tree.left.left)
        tree.right.left = Tree(aux_tree.right.left)
        tree.right.right.change_root_data('or')
        tree.right.right.left = Tree(aux_tree.right.right)
        tree.right.right.right = Tree(aux_tree.left.right)

    elif tree.left.data == 'or' and tree.right.data == 'and' and check_its_atom(tree.left.left) and check_its_atom(tree.left.right):
        aux_tree = copy.deepcopy(tree)
        tree.change_root_data('and')
        # Define the following root nodes
        tree.left.change_root_data('or')
        tree.right.change_root_data('or')
        # Populate the ors
        tree.left.left = Tree(aux_tree.right.left)
        tree.left.right.change_root_data('or')
        tree.left.right.left = Tree(aux_tree.right.right)
        tree.left.right.right = Tree(aux_tree.left.left)
        tree.right.left = Tree(aux_tree.right.left)
        tree.right.right.change_root_data('or')
        tree.right.right.left = Tree(aux_tree.right.right)
        tree.right.right.right = Tree(aux_tree.left.right)

    return tree


def simplify(clauses):
    """ Applies simplifcations to a list """

    # Apply factoring -> removing literal that occur more than once in a clause
    clauses = list(set(clauses))

    # If a tautology is detected, return string saying it
    for ix1, element1 in enumerate(clauses):
        if isinstance(element1, tuple):
            for ix2, element2 in enumerate(clauses):
                if element1[1] == element2:
                    return "tautology"

    return clauses


def get_clauses(tree, flag):
    """ Returns the clauses of a tree """

    # Auxiliary function

    def flatten(tuple_):
        """ Returns flattened tuple """
        if tuple_ == tuple():
            return (tuple_)
        if isinstance(tuple_[0], tuple):
            return flatten(tuple_[0]) + flatten(tuple_[1:])
        return tuple_[:1] + flatten(tuple_[1:])

    # Main part - The main idea is that we can only get clauses from subtrees with root or, neg or if
    # they are atoms. Subtrees with root or might have several children. With this in mind, whenever
    # get clauses is called a flag is passed, corresponding to the root node of the caller. If the caller
    # is an and or it is the beginning of the process, then they should print the respective clause. If
    # the caller is an OR, then they should return a value. This is done until every clause has been printed
    # to the system output.

    # If the root node is an AND, we can check both sub trees independently, since
    # each of them will correspond to two distinct clauses
    if tree.data == "and":

        get_clauses(tree.left, "and")
        get_clauses(tree.right, "and")

        # If an OR calls an AND, than the three is built wrongly and the clause will be ignored - This happens
        # because the distributive law is not properly implemented
        if flag == "or":
            return "illegal_tree"

    # Case in which the root node is an OR
    elif tree.data == "or":

        if flag == "and" or flag == "begin":

            clause1 = get_clauses(tree.left, "or")
            clause2 = get_clauses(tree.right, "or")

            out_list = list()

            # Deal with clause1
            if isinstance(clause1, str):
                out_list.append(clause1)
            else:
                flattened_clause1 = flatten(clause1)

                for element in flattened_clause1:
                    out_list.append(element)

            # Deal with clause2
            if isinstance(clause2, str):
                out_list.append(clause2)
            else:
                flattened_clause2 = flatten(clause2)

                for element in flattened_clause2:
                    out_list.append(element)

            # Initiliaze the purged list. If the first element is not a not then it is manually added
            if out_list[0] != "not":
                purged_out_list = [out_list[0]]
            else:
                purged_out_list = list()

            # Put the nots back together
            for ix in range(1, len(out_list)):
                if out_list[ix-1] == "not":
                    purged_out_list.append(('not', out_list[ix]))
                elif out_list[ix] != "not":
                    purged_out_list.append(out_list[ix])

            # Apply the simplifcations to the list of obtained clauses
            purged_out_list = simplify(purged_out_list)

            # Print the respective clause
            if purged_out_list != "tautology" and "illegal_tree" not in purged_out_list:
                print(purged_out_list)

        # If the function was not called by an AND or it is the beginning of the process
        else:

            clause1 = get_clauses(tree.left, "or")
            clause2 = get_clauses(tree.right, "or")

            return (clause1, clause2)

    # Case in which the root node is a not
    elif tree.data == "not":

        if flag == "and" or flag == "begin":

            print("[({}, \'{}\')]".format("\'not\'", tree.left.data))

        else:

            return ('not', tree.left.data)

    # Case in which the root node is an atom
    elif check_its_atom(tree):

        if flag == "and" or flag == "begin":

            print("\'{}\'".format(tree.data))

        else:

            return (tree.data)


def main():
    """ Main Function. Calls every method needed to solve the problem """

    # Create the knowledge base
    knowledge_base = parse_file()

    # Go through every sentence in the knowledge base
    for sentence in knowledge_base:

        # Define the inital tree of the sentences
        tree = Tree(sentence)

        # Convert the equivalences
        tree = apply_recursion(tree, "<=>")
        tree = apply_recursion(tree, "=>")
        tree = apply_recursion(tree, "not")
        tree = apply_recursion(tree, "or")

        # Print solution
        get_clauses(tree, "begin")

if __name__ == '__main__':

    main()
    sys.stderr.close()
    