#!/usr/bin/env python
# -*- coding: utf-8 -*-


def negation(x):

    if isinstance(x, tuple):
        return x[1]

    elif isinstance(x, list):
        if isinstance(x[0], tuple):
            return x[0][1]

        return negation(x[0])

    else:
        return tuple(["not", x])


class Search(object):

    kb = []
    kb_raw = None
    alpha = None
    alpha_not = None
    possible_alpha = []

    def __init__(self, problem=[]):

        self.kb_raw = problem

        # print ("And the problem is: ", problem)

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
        
        # print("alpha zero", self.alpha)
        self.alpha_not = negation(self.alpha)

        for sentence in problem:
            if len(sentence) == 0:
                self.possible_alpha.append()

    def result(self, loc=True):

        for p_alpha in self.possible_alpha:
            self.alpha = p_alpha
            self.alpha_not = negation(p_alpha)
            self.kb = self.kb_raw
            self.kb.remove(p_alpha)

            profundidade = []

            kb = self.kb
            # print("\n"+"################"+"\n")
            for sentence in kb:

                # print ("\n\nLast debug here: Sentence is: ", sentence)

                for atom in sentence:

                    # print("Testes, o elemento é :", atom, "resultado é", atom is self.alpha_not)

                    if atom is self.alpha_not:
                        profundidade.append(sentence)
                        # print("new possible sentence is :", sentence)
                        break

                        ################################################
                # print("Testes")

            # print("\n"+"##### deepth ", len(profundidade), " #####")
            # print("depth is ", profundidade)
            # print("################"+"\n")

            if (not(len(profundidade))) or (len(kb) == 0) or (kb is None):
                if loc:
                    print("False")
                    # print("alpha_not is ", self.alpha_not)
                return False

            if self.kb.__contains__(list(self.alpha)):
                if loc:
                    print(True)
                return True

            for sentence in profundidade:

                kb = self.kb
                alpha = self.alpha
                alpha_not = self.alpha_not

                kb.remove(sentence)
                # print ("sentence is ", sentence)
                # print ("alpha_not is ", alpha_not)
                alpha = sentence

                if not(alpha.__contains__(alpha_not)):
                    if loc:
                        print("False")

                    return False

                if alpha == alpha_not:
                    if loc:
                        print(True)
                    return True

                # print ("is alpha a list : ", alpha, "\n")
                alpha.remove(alpha_not)
                # print ("alpha is by ruben ", alpha)
                alpha_not = negation(alpha)
                # print ("not_alpha is by ruben ", alpha_not)

                if not(len(alpha)):
                    if loc:
                        print("True")
                    return True

                search = Search(kb+[[alpha]])

                if search.result(False):
                    if loc:
                        print("True")
                    return True

        if loc:
            print("False")
        return False
