import pytest

from algorithm import initialize_dp
from algorithm import get_rules_without_terminals
from algorithm import handle_one_letter
from algorithm import check_is_grammar_contains_word
from algorithm import check_grammar_on_chomsky_normal_form
from io_handler import enter_grammar


def test_initialize_dp():
    word = "abc"
    real_array = [[[] for i in range(len(word))] for i in range(len(word))]

    array = initialize_dp(word)

    for i in range(len(real_array)):
        for j in range(len(real_array[i])):
            if real_array[i][j] != array[i][j]:
                assert False
    assert True


def generate_standart_grammar(grammar_type="without_EPS"):
    grammar = dict()
    terminals = []
    non_terminals = []
    start = 'S'

    if grammar_type == "without_EPS":
        grammar['S'] = ['AB']
        grammar['A'] = ['BB', 'b']
        grammar['B'] = ['CA', 'c']
        grammar['C'] = ['AC', 'a']
        terminals = ['b', 'c', 'a']
        non_terminals = ['S', 'A', 'B', 'C']
    elif grammar_type == "not_chomsky_form":
        grammar['S'] = ['AB']
        grammar['A'] = ['BBW', 'bW']
        grammar['B'] = ['CA', 'EPS']
        terminals = ['b']
        non_terminals = ['S', 'A', 'B', 'C', 'W']
    else:
        grammar['S'] = ['AB', 'EPS']
        grammar['A'] = ['a']
        grammar['B'] = ['b']
        terminals = ['a', 'b']
        non_terminals = ['S', 'A', 'B']
        start = 'S'

    grammar = {"grammar": grammar, "terminals": terminals,
               "non_terminals": non_terminals, "start": start}
    return grammar


def test_get_rules_without_terminals():
    grammar = generate_standart_grammar()
    real_answer = {'S': ['AB'], 'A': ['BB'], 'B': ['CA'], 'C': ['AC']}
    answer = get_rules_without_terminals(grammar)

    keys = list(answer.keys())
    for key in keys:
        if key not in real_answer:
            assert False
        del answer[key]
        del real_answer[key]

    if len(real_answer) > 0:
        assert False
    assert True


def test_handle_word():
    word = "ababc"
    grammar = generate_standart_grammar()
    real_answer = [[['C'], ['A'], ['C'], ['A'], ['B']],
                   [[], [], [], [], []],
                   [[], [], [], [], []],
                   [[], [], [], [], []],
                   [[], [], [], [], []]]

    dp = initialize_dp(word)
    answer = handle_one_letter(grammar, word, dp)

    if len(answer) != len(real_answer):
        assert False
    if len(answer[0]) != len(real_answer[0]):
        assert False

    for i in range(len(answer)):
        for j in range(len(answer[i])):
            if answer[i][j] != real_answer[i][j]:
                assert False
    assert True


@pytest.mark.parametrize('grammar_type,word,answer', (
                                         [["without_EPS", "ababc", True],
                                          ["without_EPS", "bab", True],
                                          ["without_EPS", "", False],
                                          ["with_EPS", "ab", True],
                                          ["with_EPS", "a", False],
                                          ["with_EPS", "", True]]
                                        ))
def test_check_is_grammar_contains_word(grammar_type, word, answer):
    grammar = generate_standart_grammar(grammar_type)
    print(word)

    assert answer == check_is_grammar_contains_word(grammar, word)


def test_enter_grammar():
    input_filename = "../examples/grammar.txt"
    answer = enter_grammar(input_filename)

    real_answer = {'grammar': {
                                'S': ['AB'],
                                'A': ['BB', 'b'],
                                'B': ['CA', 'c'],
                                'C': ['AC', 'a']
                            },
                   'terminals': ['b', 'c', 'a'],
                   'non_terminals': ['S', 'A', 'B', 'C'],
                   'start': 'S'
                   }

    assert answer == real_answer


@pytest.mark.parametrize('grammar_type,answer', (
                                         [["not_chomsky_form", False],
                                          ["without_EPS", True],
                                          ["with_EPS", True]]
                                        ))
def test_check_grammar_on_chomsky_normal_form(grammar_type, answer):
    grammar = generate_standart_grammar(grammar_type)

    assert answer == check_grammar_on_chomsky_normal_form(grammar)
