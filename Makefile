.PHONY: install test build clean run

# Установка зависимостей
install:
	poetry install

# Сборка exe
build:
	python build_exe.py

# Очистка
clean:
	rm -rf build dist __pycache__ *.spec

# Запуск GUI
run:
	python -m xml_join.scripts.start_join

# Полная сборка (установка + тест + сборка)
all: install build

# Помощь
help:
	@echo "Доступные команды:"
	@echo "  install  - Установка зависимостей"
	@echo "  build    - Сборка exe файла"
	@echo "  clean    - Очистка временных файлов"
	@echo "  run      - Запуск GUI приложения"
	@echo "  all      - Полная сборка (install + build)"
	@echo "  help     - Показать эту справку"