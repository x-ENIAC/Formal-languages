# Построение ДКА и МПДКА по НКА

## Запуск

Необходимые пакеты: pytest-cov

Запуск: `python3 main.py <file>`. Например, `python3 main.py ../examples/3/example.doa`. Примеры можно увидеть в папке examples.

## Покрытие тестами

Покрытие тестами можно увидеть, введя в терминал команду `py.test test.py --cov=. --cov-report=html`, находясь в папке `src`. Будет сгенерирован отчет в html-формате (для просмотра нужно открыть `src/htmlcov/index.html` в браузере).

Текущее покрытие тестами:

![Покрытие тестами](https://sun9-49.userapi.com/impg/GN4hJ3ami0Uj8nSesYuqmkAIXtc_spThNwy1tA/eHNMPTe8ruE.jpg?size=608x302&quality=96&sign=5f19f8b82f7e6b191b7c19abe1f0ac79&type=album)

