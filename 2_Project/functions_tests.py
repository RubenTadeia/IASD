from convert import convert_equivalence
from convert import convert_implication
from convert import convert_negation
from convert import convert_disjunction

equi1 = ('<=>', 'A', 'B')
equi2 = ('<=>', ('or', 'A', 'B'), ('and', 'A', 'B'))

print(convert_equivalence(equi1))
print(convert_equivalence(equi2))

imp1 = ('=>', ('or', 'A', 'B'), ('and', 'A', 'B'))

print(convert_implication(imp1))

disj1 = ('or', 'A', ('and', ('neg', 'B'), ('neg', 'C')))

print(convert_disjunction(disj1))