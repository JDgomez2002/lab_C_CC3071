from syntax_tree import SyntaxTree
from directConstruction import DirectDFA
from yalexReader import *
from regex import shunting_yard

myFile = "slr-4.yal"

definitions, rules, translatedRules, expression = yalexReader(myFile)

print('\n##### Definitions #####')
for definition in definitions:
  print(f"{definition} = {definitions[definition]}")
  print()

print('##### Rules #####')
for rule in rules:
  print(f"{rule} = {rules[rule]}")
  print()

print('##### Translated Rules #####')
for rule in translatedRules:
  print(f"{rule} = {translatedRules[rule]}")
  print()

print('##### Expression #####')
print(expression)

postfix = shunting_yard(expression)
print('\n##### Postfix #####')
print(postfix)
print()

# Tree
tree = SyntaxTree(postfix)
tree.render()

# Direct DFA
dfa = DirectDFA(tree)
dfa.render()
