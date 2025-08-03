# XML Join Tool

Инструмент для объединения XML файлов с данными о пользователях и департаментах в Excel файл.

## Возможности

- Консольное приложение для обработки XML файлов
- Объединение данных о пользователях и департаментах
- Экспорт результата в Excel файл (XLSX)
- Упаковка в исполняемый exe файл для Windows

## Установка зависимостей

```bash
poetry install
```

## Запуск приложения

### Как Python модуль
```bash
poetry run python xml_join/join.py --users users.xml --deps departments.xml --output output_folder
```

### Как exe файл
```bash
xml_join.exe --users users.xml --deps departments.xml --output output_folder
```

## Сборка exe файла

### Автоматическая сборка

```bash
poetry run python build_exe.py
```

### Ручная сборка

```bash
poetry run pyinstaller xml_join.spec
```

После сборки exe файл будет находиться в папке `dist/xml_join.exe`.

## Использование

### Синтаксис
```bash
xml_join.exe --users <users_file> --deps <departments_file> --output <output_folder>
```

### Параметры
- `--users` - XML файл с данными о пользователях
- `--deps` - XML файл с данными о департаментах  
- `--output` - Папка для сохранения результата

### Примеры
```bash
# Использование Python модуля
python -m xml_join.join --users users.xml --deps departments.xml --output output_folder

# Использование exe файла
xml_join.exe --users users.xml --deps departments.xml --output output_folder
```

### Результат
Результат будет сохранен как `user_deps_DD_MM_YYYY.xlsx` в указанной папке.

## Структура проекта

```
xml-join1/
├── xml_join/
│   ├── __init__.py
│   └── join.py              # Основная логика обработки XML
├── xml_join.spec            # Конфигурация PyInstaller
├── build_exe.py             # Скрипт сборки exe
├── pyproject.toml           # Зависимости проекта
└── README.md
```

## Зависимости

- `lxml` - обработка XML файлов
- `pyexcelerate` - создание Excel файлов
- `pyinstaller` - упаковка в exe

## Требования

- Python 3.10-3.13
- Poetry для управления зависимостями
