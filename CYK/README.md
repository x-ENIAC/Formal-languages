# Алгоритм Кока-Янгера-Касами

## Запуск

Необходимые пакеты: pytest-cov

Запуск: `python3 main.py <file> <word>`. Например, `python3 main.py ../examples/grammar.txt ababc`. Пример грамматики можно увидеть в папке examples. Если хочется проверить пустое слово на принадлежность грамматике, то параметр `<word>` нужно оставить пустым.

Алгоритм принимает на вход КС-грамматику, находящуюся в НФ Хомского. Если слово принадлежит грамматике, то программа выведет `The word is contained in the grammar`, иначе - `The word isn't contained in the grammar`.

## Покрытие тестами

Покрытие тестами можно увидеть, если ввести в терминал команду `py.test test.py --cov=. --cov-report=html`, находясь в папке `src`. Будет сгенерирован отчет в html-формате (для просмотра нужно открыть `src/htmlcov/index.html` в браузере).

Текущее покрытие тестами:

![Покрытие тестами](https://sun9-35.userapi.com/impg/pDXzk9B8Fy65jOb5sZWfL0NrDi5WnpEo76Z5lQ/6IdJr0dFihA.jpg?size=561x277&quality=96&sign=507502b80bfce3c9380c5ffa56cb6a49&type=album)

