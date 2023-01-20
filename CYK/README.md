# Cocke-Younger-Kasami algorithm

## Run

**Required packages:** pytest-cov

**Run:** `python3 main.py <file> <word>`. For example, `python3 main.py ../examples/grammar.txt ababc`. An example grammar can be seen in the `examples/` folder. If you want to check an empty word for belonging to a grammar, then the `<word>` parameter must be left empty.

The algorithm takes as input a CF-grammar located in Chomsky's NF. If the word belongs to the grammar, then the program will print `The word is contained in the grammar`, otherwise - `The word isn't contained in the grammar`.

The algorithm is a two-dimensional dynamics. A cell with the j-th column and the i-th row means that the first i characters in the word are currently being considered, starting from the j-th character. The cell contains non-terminals from which the word in question is derived. First, the first level is filled, and then the subsequent ones based on it. Grammar example:
```
s -> AB | BC
A -> BA | a
B -> CC | b
C -> AB | a
```

|        |     |  |     |     |  |
| ---|-----|----- |:--------|----------:| -----:|
| 5 letters  | ... | - | - | - | - |
| 4 letters   | ... | ... | - | - | - |
| 3 letters | ... | ... | ... | -| - |
| 2 letters | A,S | B | S,C | A,S | - |
| 1 letter | B | A,C | A,C | B | A,C |
|  | b | a | a | b | a |


If the cell that corresponds to the full word contains a starting non-terminal, then this means that the word is derivable in the grammar. Otherwise no.

## Test coverage

Test coverage can be seen by typing `py.test test.py --cov=. --cov-report=html` while in the `src` folder. An html report will be generated (you need to open `src/htmlcov/index.html` in your browser to view it).

Current test coverage:

![Test coverage](https://github.com/x-ENIAC/Formal-languages/blob/master/CYK/test_coverage.jpg)

