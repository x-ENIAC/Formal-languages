ARROW_CONSTANT = "->"
RULES_DELIMETER = "|"
EPSILON = "EPS"


def scan_file(filename):
    '''
    Считывает текст из файла

    Parameters:
        filename Имя файла

    Returns:
        text Текст, считанный из указанного файла
    '''

    text = ""
    with open(filename, 'r') as file:
        text = file.readlines()
    return text


def scan_left_rule_part(rule):
    '''
    Считывает левую часть правила, т.е. нетерминал

    Parameters:
        rule Правило целиком

    Returns:
        left_part Нетерминал из левой части правила
    '''

    parts = rule.split('->')
    left_part = parts[0].strip(' ')
    return left_part


def scan_right_rule_parts(rule):
    '''
    Считывает правую часть правила

    Parameters:
        rule Правило целиком

    Returns:
        parts Правая часть правила
    '''

    parts = rule.split(ARROW_CONSTANT)[1].strip(' ').strip('\n')
    parts = parts.split(RULES_DELIMETER)
    parts = [part.strip(' ') for part in parts]
    return parts


def convert_text_to_grammar(text):
    '''
    Переводит текст в грамматику

    Parameters:
        text Текст

    Returns:
        grammar Итоговая грамматика
    '''

    non_terminals = []
    terminals = []
    grammar = dict()

    start = 'S'

    for rule in text:
        left_rule_part = scan_left_rule_part(rule)
        right_rule_parts = scan_right_rule_parts(rule)

        if EPSILON not in right_rule_parts:
            if left_rule_part not in non_terminals:
                non_terminals.append(left_rule_part)

            if left_rule_part not in grammar.keys():
                grammar[left_rule_part] = right_rule_parts
            else:
                grammar[left_rule_part] += right_rule_parts

        for rule in right_rule_parts:
            if rule == EPSILON:
                if start not in grammar and EPSILON not in grammar[start]:
                    grammar[start] = [EPSILON]
                else:
                    grammar[start].append(EPSILON)
                continue
            for symbol in rule:
                if symbol.isupper() and symbol not in non_terminals:
                    non_terminals.append(symbol)
                if symbol.islower() and symbol not in terminals:
                    terminals.append(symbol)

    grammar = ({"grammar": grammar, "terminals": terminals,
                "non_terminals": non_terminals,
                "start": start})
    return grammar


def enter_grammar(input_filename):
    '''
    Из указанного файла достаёт грамматику

    Parameters:
        input_filename Имя файла, в котором описана грамматика

    Returns:
        grammar Грамматика
    '''

    return convert_text_to_grammar(scan_file(input_filename))
