from syntax_tree import SyntaxTree
from directConstruction import DirectDFA
from render import render_nfa, render_dfa
from regex_nfa import regex_to_nfa
from nfa_dfa import nfa_to_dfa
from utils import isValidExpression

def main(regex, string):
    print(f"--- Regex: {regex} ---")
    if not isValidExpression(regex):
        return
    print(f"--- Input: {string} ---")
    if not isValidExpression(string):
        return
    directDFA = DirectDFA(regex)
    directDFA.render()
    directDFA.run(string)

    # directDFA.render(True)
    # directDFA.minimize()
    # directDFA.run(string, True)

    # tree = SyntaxTree(regex)
    # tree.render()

    # nfa = regex_to_nfa(regex)
    # render_nfa(nfa)
    # dfa = nfa_to_dfa(nfa)
    # render_dfa(dfa)

    # nfa.run(string)
    # dfa.run(string)

    # dfa.minimize()
    # render_dfa(dfa, "min_dfa")
    # dfa.run(string, True)

if __name__ == "__main__":
    main(
        "(a|b)|(c|d)",
        "b",
    )
