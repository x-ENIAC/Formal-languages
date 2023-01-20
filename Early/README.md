# Early algorithm

## Run

Required packages: pytest-cov

Run: `python3 main.py <file> <word>`. For example, `python3 main.py ../examples/grammar.txt abab`. Examples can be seen in `the examples/` folder.

In the input grammar, the starting nonterminal is automatically `S'`.

## Test coverage

Test coverage can be seen by typing `py.test test.py --cov=. --cov-report=html` while in the `src` folder. An html report will be generated (you need to open `src/htmlcov/index.html` in your browser to view it).

Current test coverage:

![test_coverage](https://github.com/x-ENIAC/Formal-languages/blob/master/Early/test_coverage.jpg)

