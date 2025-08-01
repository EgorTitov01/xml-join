#!/usr/bin/env python3
"""
Скрипт для сборки exe файла с помощью PyInstaller
"""

import subprocess
import sys
import os
from pathlib import Path

def build_exe():
    """Собирает exe файл с помощью PyInstaller"""
    
    print("Начинаем сборку exe файла...")
    
    # Проверяем, что мы в правильной директории
    if not Path("xml_join.spec").exists():
        print("Ошибка: файл xml_join.spec не найден!")
        return False
    
    # Команда для сборки
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",  # Очищаем предыдущие сборки
        "xml_join.spec"
    ]
    
    try:
        print("Выполняем команду:", " ".join(cmd))
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("Сборка завершена успешно!")
        print("Exe файл находится в папке dist/")
        
        # Проверяем, что файл создался
        exe_path = Path("dist/xml_join_tool.exe")
        if exe_path.exists():
            print(f"Файл создан: {exe_path.absolute()}")
            return True
        else:
            print("Ошибка: exe файл не был создан!")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при сборке: {e}")
        print(f"Вывод команды: {e.stdout}")
        print(f"Ошибки: {e.stderr}")
        return False
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return False

if __name__ == "__main__":
    success = build_exe()
    sys.exit(0 if success else 1) 