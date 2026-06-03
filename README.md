# Log Analyzer

Анализатор nginx-логов для домашнего задания OTUS. Скрипт ищет последний лог `nginx-access-ui.log-YYYYMMDD[.gz]`, считает статистику по URL и генерирует HTML-отчёт.

## Что умеет

- ищет последний лог по дате в имени файла
- читает plain и gzip-логи
- считает статистику:
  - `count`
  - `count_perc`
  - `time_sum`
  - `time_perc`
  - `time_avg`
  - `time_max`
  - `time_med`
- пишет структурированные JSON-логи через `structlog`
- генерирует HTML-отчёт и копирует рядом `jquery.tablesorter.min.js`

## Структура конфигурации

Дефолтный конфиг находится в [src/app/config.py](/Users/andrey/Documents/self/otus_python_professional/hw_01/src/app/config.py):

```python
config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log",
}
```

Можно передать внешний конфиг через `--config`. Значения из файла переопределяют дефолты из `config.py`.

Пример внешнего конфига:

```text
REPORT_SIZE = 100
LOG_DIR = ./log
REPORT_DIR = ./reports
LOG_FILE = ./reports/app.log
```

`LOG_FILE` опционален. Если он не задан, лог пишется в `stdout`.

## Запуск локально

Установка зависимостей:

```bash
poetry install
```

Запуск с дефолтным конфигом:

```bash
poetry run log-analyzer
```

Запуск с внешним конфигом:

```bash
poetry run log-analyzer --config ./config.txt
```

## Запуск тестов и проверок

Тесты:

```bash
poetry run pytest
```

Линтер:

```bash
poetry run flake8 .
```

Сортировка импортов:

```bash
poetry run isort . --check-only
```

Pre-commit:

```bash
poetry run pre-commit run --all-files
```

## Docker

Сборка образа:

```bash
docker build -t log-analyzer .
```

Запуск с дефолтным конфигом из `config.py`:

```bash
docker run --rm \
  -v "$(pwd)/log:/app/log:ro" \
  -v "$(pwd)/reports:/app/reports" \
  log-analyzer
```

Запуск с внешним конфигом:

```bash
docker run --rm \
  -v "$(pwd)/config.txt:/app/config.txt:ro" \
  -v "$(pwd)/log:/data/log:ro" \
  -v "$(pwd)/reports:/data/reports" \
  log-analyzer \
  --config /app/config.txt
```

Пример Docker-конфига:

```text
REPORT_SIZE = 100
LOG_DIR = /data/log
REPORT_DIR = /data/reports
LOG_FILE = /data/reports/app.log
```

## Выходные артефакты

После успешного запуска в `REPORT_DIR` появляются:

- `report-YYYY.MM.DD.html`
- `jquery.tablesorter.min.js`
- `app.log`, если задан `LOG_FILE`

## Пример входного лога

Для локальной проверки можно использовать sample log из курса:

`/Users/andrey/Documents/self/otus_python_professional/01_new_project/homework/nginx-access-ui.log-20170630.gz`
