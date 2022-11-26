# Алгоритм Кока-Янгера-Касами

## Запуск

Необходимые пакеты: pytest-cov

Запуск: `python3 main.py <file> <word>`. Например, `python3 main.py ../examples/grammar.txt ababc`. Пример грамматики можно увидеть в папке examples. Если хочется проверить пустое слово на принадлежность грамматике, то параметр `<word>` нужно оставить пустым.

Алгоритм принимает на вход КС-грамматику, находящуюся в НФ Хомского. Если слово принадлежит грамматике, то программа выведет `The word is contained in the grammar`, иначе - `The word isn't contained in the grammar`.

## Покрытие тестами

Покрытие тестами можно увидеть, если ввести в терминал команду `py.test test.py --cov=. --cov-report=html`, находясь в папке `src`. Будет сгенерирован отчет в html-формате (для просмотра нужно открыть `src/htmlcov/index.html` в браузере).

Текущее покрытие тестами:

![Покрытие тестами](https://sun9-51.userapi.com/impg/PYAB5rLB2KBP-1UuC5J1IMJ7ZPRSOL2kl3U7fA/FrZPKTEWpRQ.jpg?size=498x282&quality=96&sign=1eca688372b3bf4423d53e2e1ef8506b&type=album)

