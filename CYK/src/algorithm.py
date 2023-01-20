from io_handler import EPSILON
from grammar import Grammar


class CYK:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.word = None
        self.dp = None
        self.initialize_dp()

    def initialize_dp(self) -> None:
        if self.word is None:
            word_len = 0
        else:
            word_len = len(self.word)
        self.dp = [[[] for i in range(word_len)] for i in range(word_len)]

    def handle_one_letter(self) -> None:
        '''
        Processing one letter by the algorithm (this is the first step of the algorithm.
        For example, if the word abc is given as input, the a, b, c
        (this is what happens in this function), then ab, bc, then abc)
        '''

        word_len = len(self.word)

        non_terminals = self.grammar.non_terminals
        non_terminals_len = len(non_terminals)
        grammar_rules = self.grammar.grammar_rules

        for i in range(word_len):
            letter = self.word[i]

            for j in range(non_terminals_len):
                non_terminal = non_terminals[j]
                rules = grammar_rules[non_terminal]

                for rule in rules:
                    if len(rule) == 1 and letter == rule:
                        self.dp[0][i].append(non_terminal)

    def check_is_grammar_contains_word(self, word: str) -> bool:
        self.word = word
        self.initialize_dp()

        start = self.grammar.start
        word_len = len(self.word)

        if word_len == 0:
            if EPSILON in self.grammar.grammar_rules[start]:
                return True
            else:
                return False

        self.handle_one_letter()

        rules_without_terminals = self.grammar.get_rules_without_terminals()

        for current_word_len in range(1, word_len):
            self.handle_word(rules_without_terminals, current_word_len)
        answer = self.dp[word_len - 1][0]

        if start in answer:
            return True
        return False

    def handle_word(self, rules_without_terminals: list,
                    current_word_len: int) -> None:
        '''
        Processes the word w[1:current_word_len].
        Fills self.dp[current_word_len] with True/False values
        True - if the given word is displayed in the grammar
        False - if not displayed
        '''

        start = self.grammar.start

        keys_rules_without_terminals = rules_without_terminals.keys()

        wold_len = len(self.word)
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
                    first_part = self.word[current_start]
                else:
                    left = current_start
                    right = current_start + current_delimeter
                    first_part = self.word[left:right]

                if current_delimeter == current_end:
                    second_part = self.word[current_end]
                else:
                    left = current_start + current_delimeter
                    right = current_end + 1
                    second_part = self.word[left:right]

                len_first_part = len(first_part) - 1
                len_second_part = len(second_part) - 1

                current_start_after_delimeter = (current_start +
                                                 current_delimeter)
                first_non_terminals = self.dp[len_first_part][current_start]
                second_non_terminals = (self.dp[len_second_part]
                                        [current_start_after_delimeter])

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
                                self.dp[current_word_len][start].append(
                                    non_terminal
                                )

                current_delimeter += 1
