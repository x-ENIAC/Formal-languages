import sys  # pragma: no cover

from io_handler import enter_grammar  # pragma: no cover
from algorithm import CYK  # pragma: no cover


def main(argv):  # pragma: no cover
    input_filename = argv[1]
    if len(argv) == 2:
        word = ""
    else:
        word = argv[2]
    grammar = enter_grammar(input_filename)

    if not grammar.check_grammar_on_chomsky_normal_form():
        print("The grammar isn't in Chomsky normal form")
        sys.exit(-1)

    grammar.print()

    cyk = CYK(grammar)

    if cyk.check_is_grammar_contains_word(word):
        print("The word is contained in the grammar")
    else:
        print("The word isn't contained in the grammar")


if __name__ == "__main__":  # pragma: no cover
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        help_message = (
            "Bad params. "
            "Please set the filename with grammar description and word"
        )

        print(help_message)
        sys.exit(-1)

    main(sys.argv)
