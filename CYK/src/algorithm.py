from io_handler import EPSILON


def initialize_dp(word):
    '''
    Инициализирует пустой массив для динамики

    Parameters:
        word Слово, от длины которого зависит размер массива

    Returns:
        dp Массив для динамики
    '''

    word_len = len(word)
    dp = [[[] for i in range(word_len)] for i in range(word_len)]
    return dp


def handle_word(grammar, rules_without_terminals, word, current_word_len,
                dp):
    '''
    Инициализирует пустой массив для динамики

    Parameters:
        grammar Текущая грамматика
        rules_without_terminals Все правила, не содержащие терминалы
        word Слово, которое хотим проверить на принадлежность грамматике
        current_word_len Текущая длина слова в алгоритме
        dp Массив для динамики

    Returns:
        dp Обновленный массив для динамики с новой обработанной позицией в
           слове
    '''

    start = grammar["start"]

    keys_rules_without_terminals = rules_without_terminals.keys()

    wold_len = len(word)
    for start in range(wold_len):
        end = start + current_word_len
        if end >= wold_len:
            continue

        current_delimeter = 1
        current_start = start
        current_end = end

        '''
        bab:
            1 letter: (b), (a), (b)
            2 letter: (ba, b), (b, ab)
            3 letter: (bab)
        '''

        while current_start + current_delimeter - 1 < current_end:
            first_part, second_part = "", ""
            if current_delimeter == 1:
                first_part = word[current_start]
            else:
                left = current_start
                right = current_start + current_delimeter
                first_part = word[left:right]

            if current_delimeter == current_end:
                second_part = word[current_end]
            else:
                left = current_start + current_delimeter
                right = current_end + 1
                second_part = word[left:right]

            len_first_part = len(first_part) - 1
            len_second_part = len(second_part) - 1

            first_non_terminals = dp[len_first_part][current_start]
            second_non_terminals = dp[len_second_part][current_start +
                                                       current_delimeter]

            parent_non_terminals = []
            for i in first_non_terminals:
                for j in second_non_terminals:
                    if i + j not in parent_non_terminals:
                        parent_non_terminals.append(i + j)

            for i in parent_non_terminals:
                for non_terminal in keys_rules_without_terminals:
                    rules = rules_without_terminals[non_terminal]
                    for rule in rules:
                        if rule == i:
                            dp[current_word_len][start].append(non_terminal)

            current_delimeter += 1

    return dp


def get_rules_without_terminals(grammar):
    '''
    Достаёт из грамматики все правила, не содержащие терминалы
    (т.е. правила вида A -> BC)

    Parameters:
        grammar Текущая грамматика

    Returns:
        rules_without_terminals Все правила, не содержащие терминалы
    '''

    rules_without_terminals = dict()
    terminals = grammar["terminals"]
    non_terminals = grammar["non_terminals"]
    grammar_rules = grammar["grammar"]

    for non_terminal in non_terminals:
        rules = grammar_rules[non_terminal]

        for rule in rules:
            if rule in terminals:
                continue

            if non_terminal not in rules_without_terminals:
                rules_without_terminals[non_terminal] = [rule]
            else:
                rules_without_terminals[non_terminal] += [rule]
    return rules_without_terminals


def handle_one_letter(grammar, word, dp):
    '''
    Обработка одной буквы алгоритмом (это первый шаг алгоритма.
    Например, если на вход дано слово abc, сначала обработаются
    a, b, c (это и проиходит в данной функции), затем ab, bc, затем abc)

    Parameters:
        grammar Текущая грамматика
        word Слово, которое хотим проверить на принадлежность грамматике
        dp Массив для динамики

    Returns:
        dp Обновлённый массив для динамики
    '''

    word_len = len(word)

    non_terminals = grammar["non_terminals"]
    non_terminals_len = len(non_terminals)
    grammar = grammar["grammar"]

    for i in range(word_len):
        letter = word[i]

        for j in range(non_terminals_len):
            non_terminal = non_terminals[j]
            rules = grammar[non_terminal]

            for rule in rules:
                if len(rule) == 1 and letter == rule:
                    dp[0][i].append(non_terminal)
    return dp


def check_is_grammar_contains_word(grammar, word):
    '''
    Проверяет слово на принадлежность грамматике

    Parameters:
        grammar Текущая грамматика
        word Слово, которое хотим проверить на принадлежность грамматике

    Returns:
        True, если слово лежит в грамматике. Иначе False
    '''

    start = grammar["start"]
    word_len = len(word)

    if word_len == 0:
        if EPSILON in grammar["grammar"][start]:
            return True
        else:
            return False

    dp = initialize_dp(word)
    dp = handle_one_letter(grammar, word, dp)

    rules_without_terminals = get_rules_without_terminals(grammar)

    for current_word_len in range(1, word_len):
        dp = handle_word(grammar, rules_without_terminals, word,
                         current_word_len, dp)
    answer = dp[word_len - 1][0]

    if start in answer:
        return True
    return False


def check_grammar_on_chomsky_normal_form(grammar):
    grammar_rules = grammar["grammar"]
    start = grammar["start"]
    keys = grammar_rules.keys()

    for key in keys:
        rules = grammar_rules[key]
        for rule in rules:
            # A -> b
            if len(rule) == 1 and rule.islower():
                continue

            # A -> BC
            if len(rule) == 2 and rule[0].isupper() and rule[1].isupper():
                continue

            # S -> EPS
            if key == start and rule == EPSILON:
                continue
            return False
    return True
