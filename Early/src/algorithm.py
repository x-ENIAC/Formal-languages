from io_handler import EPSILON
from grammar import Grammar


class Situation:
    def __init__(self,
                 new_left_part: str,
                 new_right_part: str,
                 new_point_pos: int,
                 new_parent_index: int) -> None:
        self.left_part = new_left_part
        self.right_part = new_right_part
        self.point_pos = new_point_pos
        self.parent_index = new_parent_index

    def print(self, start_symbol="") -> None:
        print(start_symbol + self.get_format_string())

    def get_format_string(self) -> str:
        print_str = self.left_part + " -> "
        for i in range(len(self.right_part)):
            if i == self.point_pos:
                print_str += "."
            print_str += self.right_part[i]

        if self.point_pos == len(self.right_part):
            print_str += "."

        print_str += (", " + str(self.parent_index) +
                      " (" + str(self.point_pos) + ")")
        return print_str

    def __eq__(self, other):
        if isinstance(other, Situation):
            return (self.left_part == other.left_part and
                    self.right_part == other.right_part and
                    self.point_pos == other.point_pos and
                    self.parent_index == other.parent_index)
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(self.get_format_string())


class Early:
    def __init__(self, grammar: Grammar) -> None:
        self.situation_table = [[]]
        self.word = None
        self.grammar = grammar

    def initialize_situation_table(self) -> None:
        if self.word is None:
            word_len = 0
        else:
            word_len = len(self.word)
        self.situation_table = [set() for i in range(word_len + 1)]

    def is_terminal(self, symbol: str) -> bool:
        return symbol in self.grammar.terminals

    def is_non_terminal(self, symbol: str) -> bool:
        return symbol in self.grammar.non_terminals

    def scan(self, position: int) -> set:
        found_sutiations = set()
        if position == 0:
            return found_sutiations

        for situation in self.situation_table[position - 1]:
            if situation.point_pos < len(situation.right_part):
                symbol = situation.right_part[situation.point_pos]
                if self.is_terminal(symbol):
                    if symbol == self.word[position - 1]:
                        new_situation = Situation(
                                    situation.left_part,
                                    situation.right_part,
                                    situation.point_pos,
                                    situation.parent_index
                        )
                        new_situation.point_pos += 1
                        if new_situation not in found_sutiations:
                            found_sutiations.add(new_situation)

        return found_sutiations

    def complete(self, new_situations: set) -> set:
        founded_situations = set()

        for situation in new_situations:
            if (situation.point_pos == len(situation.right_part)):
                parent_index = situation.parent_index
                transition = situation.left_part

                for complete_situation in self.situation_table[parent_index]:
                    if (complete_situation.point_pos <
                        len(complete_situation.right_part) and
                        complete_situation.right_part[
                            complete_situation.point_pos
                            ] == transition):
                        new_situation = Situation(
                                    complete_situation.left_part,
                                    complete_situation.right_part,
                                    complete_situation.point_pos,
                                    complete_situation.parent_index
                        )

                        new_situation.point_pos += 1
                        if new_situation not in founded_situations:
                            founded_situations.add(new_situation)

        return founded_situations

    def predict(self, position: int) -> set:
        grammar_rules = self.grammar.grammar_rules
        founded_situations = set()
        for situation in self.situation_table[position]:
            if situation.point_pos < len(situation.right_part):
                symbol = situation.right_part[situation.point_pos]
                if self.is_non_terminal(symbol):
                    rule_right_parts = grammar_rules[symbol]
                    for rule_right_part in rule_right_parts:
                        new_situation = Situation(symbol,
                                                  rule_right_part,
                                                  0, position)
                        founded_situations.add(new_situation)

        return founded_situations

    def check_letters_in_word(self) -> bool:
        alphabet = self.grammar.terminals
        for letter in self.word:
            if letter not in alphabet:
                return False
        return True

    def situations_print(self, situations: set, start_message: str) -> None:
        print(start_message)
        for situation in situations:
            situation.print("\t")

    def check_is_grammar_contains_word(self, word: str) -> bool:
        '''
        Запускает алгоритм Эрли. Делает scan (чтение очередной буквы в слове),
        затем запускает все возможные predict (раскрытие нетерминала) и
        complete ("поднятие наверх"). Ситуации, обрабатываемые на i-ой итерации
        алгоритма, записываются в таблицу situation_table в i-ый столбец.

        Стартовая конфигурация: S' → .S, 0

        Алгоритм утверждает, что слово принадлежит языку, который порождён
        грамматикой, если в последнем столбце находится конфигурация
        S' → S., 0
        '''
        self.word = word

        if not self.check_letters_in_word():
            return False

        self.initialize_situation_table()
        word_len = len(self.word)

        start_situations = set()
        start_situations.add(Situation("S'", "S", 0, 0))
        self.situation_table[0] = start_situations

        for i in range(word_len + 1):
            situations_after_scan = self.scan(i)

            for situation in situations_after_scan:
                self.situation_table[i].add(situation)

            situations_after_complete = set()

            is_changed = True
            is_first_while_action = True
            while is_changed:
                is_changed = False

                if (is_first_while_action or
                   len(situations_after_complete) == 0):
                    situations_after_complete = self.complete(
                            self.situation_table[i])
                else:
                    situations_after_complete = self.complete(
                            situations_after_complete)

                for situation in situations_after_complete:
                    if situation not in self.situation_table[i]:
                        self.situation_table[i].add(situation)
                        is_changed = True

                situations_after_predict = self.predict(i)
                for situation in situations_after_predict:
                    if situation not in self.situation_table[i]:
                        self.situation_table[i].add(situation)
                        is_changed = True
                is_first_while_action = False

        finish_situation = Situation("S'", "S", 1, 0)
        if finish_situation in self.situation_table[word_len]:
            return True
        return False
