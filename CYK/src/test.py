import unittest


from grammar import Grammar
from algorithm import CYK
from io_handler import enter_grammar


def generate_standart_grammar(grammar_type="without_EPS") -> Grammar:
    grammar_rules = dict()
    terminals = []
    non_terminals = []
    start = 'S'

    if grammar_type == "without_EPS":
        grammar_rules['S'] = ['AB']
        grammar_rules['A'] = ['BB', 'b']
        grammar_rules['B'] = ['CA', 'c']
        grammar_rules['C'] = ['AC', 'a']
        terminals = ['b', 'c', 'a']
        non_terminals = ['S', 'A', 'B', 'C']
    elif grammar_type == "not_chomsky_form":
        grammar_rules['S'] = ['AB']
        grammar_rules['A'] = ['BBW', 'bW']
        grammar_rules['B'] = ['CA', 'EPS']
        terminals = ['b']
        non_terminals = ['S', 'A', 'B', 'C', 'W']

    grammar = Grammar(grammar_rules, terminals,
                      non_terminals, start)
    return grammar


class TestCYK(unittest.TestCase):
    def test_initialize_dp(self):
        grammar = generate_standart_grammar()
        cyk = CYK(grammar)

        word = "abc"
        real_array = [[[] for i in range(len(word))] for i in range(len(word))]

        cyk.word = word
        cyk.initialize_dp()
        array = cyk.dp

        for i in range(len(real_array)):
            for j in range(len(real_array[i])):
                if real_array[i][j] != array[i][j]:
                    assert False
        assert True

    def test_handle_word(self):
        word = "ababc"
        grammar = generate_standart_grammar()
        real_answer = [[['C'], ['A'], ['C'], ['A'], ['B']],
                       [[], [], [], [], []],
                       [[], [], [], [], []],
                       [[], [], [], [], []],
                       [[], [], [], [], []]]

        cyk = CYK(grammar)
        cyk.word = word
        cyk.initialize_dp()
        cyk.handle_one_letter()
        answer = cyk.dp.copy()

        if len(answer) != len(real_answer):
            assert False
        if len(answer[0]) != len(real_answer[0]):
            assert False

        for i in range(len(answer)):
            for j in range(len(answer[i])):
                if answer[i][j] != real_answer[i][j]:
                    assert False
        assert True

    def test_check_is_grammar_contains_word_not_empty_word(self):
        grammar = generate_standart_grammar("without_EPS")
        word = "ababc"
        answer = True
        print(word)

        cyk = CYK(grammar)

        assert answer == cyk.check_is_grammar_contains_word(word)

    def test_check_is_grammar_contains_word_empty_word(self):
        grammar = generate_standart_grammar("without_EPS")
        word = ""
        answer = False
        print(word)

        cyk = CYK(grammar)

        assert answer == cyk.check_is_grammar_contains_word(word)


class TestGrammar(unittest.TestCase):
    def test_get_rules_without_terminals(self):
        grammar = generate_standart_grammar()
        real_answer = {'S': ['AB'], 'A': ['BB'], 'B': ['CA'], 'C': ['AC']}
        answer = grammar.get_rules_without_terminals()

        keys = list(answer.keys())
        for key in keys:
            if key not in real_answer:
                assert False
            del answer[key]
            del real_answer[key]

        if len(real_answer) > 0:
            assert False
        assert True

    def test_check_grammar_on_chomsky_normal_form_not_chomsky_form(self):
        grammar = generate_standart_grammar("not_chomsky_form")

        assert not grammar.check_grammar_on_chomsky_normal_form()

    def test_check_grammar_on_chomsky_normal_form_is_chomsky_form(self):
        grammar = generate_standart_grammar("without_EPS")

        assert not grammar.check_grammar_on_chomsky_normal_form()

    def test_enter_grammar_1(self):
        input_filename = "../examples/grammar.txt"
        answer = enter_grammar(input_filename)

        real_grammar_rules = {
                                'S': ['AB'],
                                'A': ['BB', 'b'],
                                'B': ['CA', 'c'],
                                'C': ['AC', 'a']
                            }
        real_non_terminals = ['S', 'A', 'B', 'C']
        real_terminals = ['b', 'c', 'a']
        real_start = 'S'
        real_grammar = Grammar(real_grammar_rules,
                               real_terminals,
                               real_non_terminals,
                               real_start)

        assert answer.is_equal(real_grammar)

    def test_enter_grammar_2(self):
        input_filename = "../examples/grammar2.txt"
        answer = enter_grammar(input_filename)

        real_grammar_rules = {
                                'S': ['AB', "EPS"],
                                'A': ['a'],
                                'B': ['b']
                            }
        real_non_terminals = ['S', 'A', 'B']
        real_terminals = ['b', 'a']
        real_start = 'S'
        real_grammar = Grammar(real_grammar_rules,
                               real_terminals,
                               real_non_terminals,
                               real_start)

        assert answer.is_equal(real_grammar)

    def test_is_equal_not_equal_terminals(self):
        grammar = generate_standart_grammar()

        real_grammar_rules = {'S': ["EPS"]}
        real_non_terminals = ['S']
        real_terminals = []
        real_start = 'S'
        real_grammar = Grammar(real_grammar_rules,
                               real_terminals,
                               real_non_terminals,
                               real_start)

        assert not grammar.is_equal(real_grammar)

    def test_is_equal_not_equal_rules(self):
        grammar = generate_standart_grammar()

        real_grammar_rules = {'S': ["AB", "EPS"], 'A': ["a"], 'B': []}
        real_non_terminals = ['S', 'A', 'B']
        real_terminals = ['b', 'a']
        real_start = 'S'
        real_grammar = Grammar(real_grammar_rules,
                               real_terminals,
                               real_non_terminals,
                               real_start)

        assert not grammar.is_equal(real_grammar)
