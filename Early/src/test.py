import unittest

from grammar import Grammar
from algorithm import Early
from io_handler import enter_grammar


def generate_standart_grammar(grammar_type="grammar1") -> Grammar:
    grammar_rules = dict()
    terminals = []
    non_terminals = []
    start = "S'"

    if grammar_type == "grammar1":
        grammar_rules["S'"] = ['S']
        grammar_rules['S'] = ['aFbF']
        grammar_rules['F'] = ['aFb', '']
        terminals = ['a', 'b']
        non_terminals = ["S'", 'S', 'F']
    else:  # grammar_type == "grammar2":
        grammar_rules["s'"] = ['S']
        grammar_rules['S'] = ['ASB', 'c']
        grammar_rules['A'] = ['a']
        grammar_rules['B'] = ['b']
        terminals = ['a', 'b', 'c']
        non_terminals = ["S'", 'S', 'A', 'B']

    grammar = Grammar(grammar_rules, terminals,
                      non_terminals, start)
    return grammar


class TestEarly(unittest.TestCase):
    def test_initialize_situation_table(self):
        grammar = generate_standart_grammar()
        early = Early(grammar)

        word = "abc"
        real_array = [set() for i in range(len(word) + 1)]

        early.word = word
        early.initialize_situation_table()
        array = early.situation_table

        if len(array) != len(real_array):
            assert False

        for i in range(len(array)):
            if array[i] != real_array[i]:
                assert False
        assert True

    def test_check_is_grammar_contains_word_grammar1_not_contain(self):
        grammar = generate_standart_grammar("grammar1")
        early = Early(grammar)
        word = "aba"

        assert not early.check_is_grammar_contains_word(word)

    def test_check_is_grammar_contains_word_grammar2_contain(self):
        grammar = generate_standart_grammar("grammar2")
        early = Early(grammar)
        word = "acb"

        assert early.check_is_grammar_contains_word(word)

    def test_check_is_grammar_contains_word_grammar2_not_contain(self):
        grammar = generate_standart_grammar("grammar2")
        early = Early(grammar)
        word = "aiashdih"

        assert not early.check_is_grammar_contains_word(word)


class TestGrammar(unittest.TestCase):
    def test_enter_grammar_1_is_equal(self):
        input_filename = "../examples/grammar.txt"
        grammar = enter_grammar(input_filename)
        real_grammar = generate_standart_grammar("grammar1")

        assert grammar.is_equal(real_grammar)

    def test_enter_grammar_1_not_equal(self):
        input_filename = "../examples/grammar.txt"
        grammar = enter_grammar(input_filename)

        real_grammar = generate_standart_grammar("grammar1")
        real_grammar.grammar_rules["D"] = ['c']

        assert not grammar.is_equal(real_grammar)

    def test_enter_grammar_2_not_equal(self):
        input_filename = "../examples/grammar.txt"
        grammar = enter_grammar(input_filename)

        real_grammar = generate_standart_grammar("grammar1")
        real_grammar.grammar_rules["F"] = ['c']

        assert not grammar.is_equal(real_grammar)
