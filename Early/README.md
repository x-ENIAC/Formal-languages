# Early algorithm

## Run

Required packages: pytest-cov

Run: `python3 main.py <file> <word>`. For example, `python3 main.py ../examples/grammar.txt abab`. Examples can be seen in the examples folder.

In the input grammar, the starting nonterminal is automatically `S'`.

## Test coverage

Test coverage can be seen by typing `py.test test.py --cov=. --cov-report=html` while in the `src` folder. An html report will be generated (you need to open `src/htmlcov/index.html` in your browser to view it).

Current test coverage:

![test_coverage](https://sun9-55.userapi.com/impg/J9SWMLwl2eiB83H5lXo-FLo5msyA74dwvuWcoQ/nYgWrZmhxgM.jpg?size=527x315&quality=96&sign=53eb2979c5a87a6c5bf46889ffa89dd7&type=album)

