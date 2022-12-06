from grammar import Grammar
from text_constants import *


def scan_file(filename: str) -> str:
    text = ""
    with open(filename, 'r') as file:
        text = file.readlines()
    return text


def scan_left_rule_part(rule: str) -> str:
    parts = rule.split('->')
    left_part = parts[0].strip(' ')
    return left_part


def scan_right_rule_parts(rule: str) -> str:
    parts = rule.split(ARROW_CONSTANT)[1].strip(' ').strip('\n')
    parts = parts.split(RULES_DELIMETER)
    parts = [part.strip(' ') for part in parts]
    return parts


def convert_text_to_grammar(text: str) -> Grammar:
    non_terminals = []
    terminals = []
    grammar_rules = dict()

    start = "S'"

    for rule in text:
        left_rule_part = scan_left_rule_part(rule)
        right_rule_parts = scan_right_rule_parts(rule)
        for i in range(len(right_rule_parts)):
            if right_rule_parts[i] == EPSILON:
                right_rule_parts[i] = ""

        if left_rule_part not in non_terminals:
            non_terminals.append(left_rule_part)

        if left_rule_part not in grammar_rules.keys():
            grammar_rules[left_rule_part] = right_rule_parts
        else:
            grammar_rules[left_rule_part] += right_rule_parts

        for rule in right_rule_parts:
            if rule == EPSILON:
                continue
            for symbol in rule:
                if symbol.isupper() and symbol not in non_terminals:
                    non_terminals.append(symbol)
                if symbol.islower() and symbol not in terminals:
                    terminals.append(symbol)

    grammar = Grammar(grammar_rules, terminals, non_terminals, start)
    return grammar


def enter_grammar(input_filename: str) -> Grammar:
    return convert_text_to_grammar(scan_file(input_filename))
