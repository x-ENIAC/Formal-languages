# Построение ДКА и МПДКА по НКА

## Запуск

Запуск: `python3 main.py <doa-file>`.
Например, `python3 main.py ../examples/3/example.doa`. Примеры можно увидеть в папке examples.

## Покрытие тестами

Покрытие тестами можно увидеть, введя в терминал команду `py.test test.py --cov=.`, находясь в папке `src`. Результат:

```
============================================================================ test session starts ============================================================================
platform linux -- Python 3.8.10, pytest-7.1.3, pluggy-1.0.0
rootdir: /home/xenia/Documents/education/Formal_languages/my_repo/src
plugins: cov-4.0.0
collected 9 items                                                                                                                                                           

test.py .........                                                                                                                                                     [100%]

---------- coverage: platform linux, python 3.8.10-final-0 -----------
Name                     Stmts   Miss  Cover
--------------------------------------------
determinize_automat.py     228      2    99%
io_handler.py              168     12    93%
main.py                      7      7     0%
minimize_automat.py         88      3    97%
test.py                    105      0   100%
--------------------------------------------
TOTAL                      596     24    96%


============================================================================= 9 passed in 1.22s =============================================================================
```

