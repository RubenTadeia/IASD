#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import copy

def negation(x):
    """ Negation method used to negate an atom, used after to search the symmetric of alpha"""

    if isinstance(x, tuple):
        return x[1]

    elif isinstance(x, list):
        if isinstance(x[0], tuple):
            return x[0][1]

        return negation(x[0])

    else:
        return tuple(["not", x])

class Resolution(object):
    """ Executes the Resolution Inference System Algorithm.

        Inputs:
        kb -- Knowledge base, list with all the sentences
        kb_raw -- Knowledge base before changes. Used when our choices went wrong, and we want to reset kb
        alpha -- used to infer the knowledge base
        alpha_not -- negation of alpha, used to search the symetric
        possible_alpha -- possible values for alpha

        Methods:
        result -- gives the result for our theorem prover. That uses the resolution method"""

    kb = [] 
    kb_raw = None 
    alpha = None
    alpha_not = None 
    possible_alpha = []
    def __init__(self, problem=[]):

        self.kb_raw = copy.deepcopy(problem) #inicializes kb_raw with every value from the file

        if not(len(problem)):
            self.kb = None
            self.alpha = None

        else:
            self.kb = problem[:-1]
            self.alpha = problem[-1]

        if (len(self.alpha) > 1) and (self.kb is not None):

            temp = problem
            for atom in temp:
                if len(atom) == 1:
                    self.alpha = atom
                    problem.remove(atom)
                    self.kb = problem
                    break
        
        self.alpha_not = negation(self.alpha)

        for sentence in problem:
            if len(sentence) == 1:
                self.possible_alpha.append(sentence)

    def result(self, printing_variable=True):
        """ Gives the result for our theorem prover. That uses the resolution method"""

        for p_alpha in self.possible_alpha:
            self.alpha = p_alpha
            self.alpha_not = negation(p_alpha)
            self.kb = copy.deepcopy(self.kb_raw)
                        
            if self.kb_raw[-1][0][0] == 'not':
                print ("True")
                sys.exit()

            if self.kb.__contains__(p_alpha):
                self.kb.remove(p_alpha)
            else:
                print("False")
                sys.exit()

            depth = [] #number of possible combinations

            kb = self.kb
            for sentence in kb:

                for atom in sentence:

                    if atom == self.alpha_not:
                        depth.append(sentence)
                        break


            if (not(len(depth))) or (len(kb) == 0) or (kb is None):
                if printing_variable:
                    print("False")
                return False

            if self.kb.__contains__(list(self.alpha)):
                if printing_variable:
                    print("True")
                return True

            for sentence in depth:

                kb = self.kb
                alpha = self.alpha
                alpha_not = self.alpha_not

                kb.remove(sentence)
                alpha = sentence

                if not(alpha.__contains__(alpha_not)):
                    if printing_variable:
                        print("False")

                    return False

                if alpha == alpha_not:
                    if printing_variable:
                        print("True")
                    return True

                alpha.remove(alpha_not)
                alpha_not = negation(alpha)

                if not(len(alpha)):
                    if printing_variable:
                        print("True")
                    return True

                resolution = Resolution(kb+[[alpha]])

                if resolution.result(False):
                    if printing_variable:
                        print("True")
                    return True

        if printing_variable:
            print("False")
        return False
