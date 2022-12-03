# Алгоритм Эрли

## Запуск

Необходимые пакеты: pytest-cov

Запуск: `python3 main.py <file> <word>`. Например, `python3 main.py ../examples/grammar.txt abab`. Примеры можно увидеть в папке examples.

В грамматике, подающейся на вход, стартовым нетерминалом автоматически считается `S'`.

## Покрытие тестами

Покрытие тестами можно увидеть, введя в терминал команду `py.test test.py --cov=. --cov-report=html`, находясь в папке `src`. Будет сгенерирован отчет в html-формате (для просмотра нужно открыть `src/htmlcov/index.html` в браузере).

Текущее покрытие тестами:

![Покрытие тестами](https://sun9-55.userapi.com/impg/J9SWMLwl2eiB83H5lXo-FLo5msyA74dwvuWcoQ/nYgWrZmhxgM.jpg?size=527x315&quality=96&sign=53eb2979c5a87a6c5bf46889ffa89dd7&type=album)

