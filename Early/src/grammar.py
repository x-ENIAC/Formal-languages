from text_constants import *


class Grammar:
    def __init__(self,
                 grammar_rules: dict(),
                 terminals: list,
                 non_terminals: list,
                 start: str) -> None:
        self.grammar_rules = grammar_rules
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.start = start

    def print(self) -> None:
        grammar = {"rules": self.grammar_rules, "terminals": self.terminals,
                   "non_terminals": self.non_terminals, "start": self.start}
        print(grammar)

    def lists_are_equal(self, first: list, second: list) -> bool:
        first = sorted(first)
        second = sorted(second)

        if len(first) != len(second):
            return False

        for value in first:
            if value not in second:
                return False
        return True

    def is_equal(self, another_grammar: dict()) -> bool:
        if (sorted(self.terminals) != sorted(another_grammar.terminals) or
            sorted(self.non_terminals) !=
            sorted(another_grammar.non_terminals) or
                self.start != another_grammar.start):
            return False

        this_rules_keys = list(self.grammar_rules.keys())
        another_rules_keys = list(another_grammar.grammar_rules.keys())

        if not self.lists_are_equal(this_rules_keys, another_rules_keys):
            return False

        for key in this_rules_keys:
            this_value = self.grammar_rules[key]
            another_value = another_grammar.grammar_rules[key]

            if not self.lists_are_equal(this_value, another_value):
                return False

        return True
