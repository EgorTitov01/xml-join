# XML Join Tool

Инструмент для объединения XML файлов с данными о пользователях и департаментах в Excel файл.

## Возможности

- GUI интерфейс для выбора XML файлов и папки сохранения
- Объединение данных о пользователях и департаментах
- Экспорт результата в Excel файл (XLSX)
- Упаковка в исполняемый exe файл для Windows

## Установка зависимостей

```bash
poetry install
```

## Запуск GUI приложения

```bash
poetry run python xml_join/scripts/start_join.py
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

После сборки exe файл будет находиться в папке `dist/xml_join_tool.exe`.

## Использование

1. Запустите приложение (GUI или exe)
2. Выберите первый XML файл с данными о пользователях
3. Выберите второй XML файл с данными о департаментах
4. Выберите папку для сохранения результата
5. Нажмите "Обработать файлы"
6. Результат будет сохранен как `user_deps.xlsx` в выбранной папке

## Структура проекта

```
xml-join1/
├── xml_join/
│   ├── __init__.py
│   ├── join.py              # Основная логика обработки XML
│   └── scripts/
│       ├── __init__.py
│       └── start_join.py    # GUI приложение с Toga
├── xml_join.spec            # Конфигурация PyInstaller
├── build_exe.py             # Скрипт сборки exe
├── pyproject.toml           # Зависимости проекта
└── README.md
```

## Зависимости

- `toga-core` - GUI фреймворк
- `toga-winforms` - Windows backend для Toga
- `pythonnet` - .NET интеграция для Windows
- `lxml` - обработка XML файлов
- `pyexcelerate` - создание Excel файлов
- `pyinstaller` - упаковка в exe

## Требования

- Python 3.10-3.13
- Windows (для GUI и exe)
- Poetry для управления зависимостями
