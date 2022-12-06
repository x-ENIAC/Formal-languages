from text_constants import *


class Grammar:
    def __init__(self,
                 grammar_rules: dict(),
                 terminals: list,
                 non_terminals: list,
                 start: str):
        self.grammar_rules = grammar_rules
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.start = start

    def check_grammar_on_chomsky_normal_form(self) -> bool:
        keys = self.grammar_rules.keys()

        for key in keys:
            rules = self.grammar_rules[key]
            for rule in rules:
                # A -> b | A -> BC | S -> EPS
                if not (len(rule) == 1 and rule.islower() and
                        len(rule) == 2 and rule[0].isupper() and
                        rule[1].isupper() and key == self.start and
                        rule == EPSILON):
                    return False
        return True

    def get_rules_without_terminals(self) -> dict():
        rules_without_terminals = dict()

        for non_terminal in self.non_terminals:
            rules = self.grammar_rules[non_terminal]

            for rule in rules:
                if rule in self.terminals:
                    continue

                if non_terminal not in rules_without_terminals:
                    rules_without_terminals[non_terminal] = [rule]
                else:
                    rules_without_terminals[non_terminal] += [rule]
        return rules_without_terminals

    def print(self) -> None:
        grammar = {"rules": self.grammar_rules, "terminals": self.terminals,
                   "non_terminals": self.non_terminals, "start": self.start}
        print(grammar)

    def is_equal(self, another_grammar: dict()) -> bool:
        if (sorted(self.terminals) != sorted(another_grammar.terminals) or
            sorted(self.non_terminals) !=
            sorted(another_grammar.non_terminals) or
                self.start != another_grammar.start):
            return False

        this_rules_keys = self.grammar_rules.keys()
        another_rules_keys = another_grammar.grammar_rules.keys()

        if sorted(this_rules_keys) != sorted(another_rules_keys):
            return False

        for key in this_rules_keys:
            this_value = self.grammar_rules[key]
            another_value = another_grammar.grammar_rules[key]

            if sorted(this_value) != sorted(another_value):
                return False

        return True
