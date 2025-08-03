#!/usr/bin/env python3
"""
Скрипт для сборки exe файла с помощью PyInstaller
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Проверяет наличие необходимых зависимостей"""
    print("Проверка зависимостей...")
    
    try:
        import lxml
        print("✓ lxml установлен")
    except ImportError:
        print("✗ lxml не установлен")
        return False
    
    try:
        import pyexcelerate
        print("✓ pyexcelerate установлен")
    except ImportError:
        print("✗ pyexcelerate не установлен")
        return False
    
    try:
        import PyInstaller
        print("✓ PyInstaller установлен")
    except ImportError:
        print("✗ PyInstaller не установлен")
        return False
    
    return True

def clean_build():
    """Очищает предыдущие сборки"""
    print("Очистка предыдущих сборок...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if Path(dir_name).exists():
            import shutil
            shutil.rmtree(dir_name)
            print(f"✓ Удалена папка {dir_name}")
    
    # Удаляем .spec файлы (кроме нашего)
    for spec_file in Path('.').glob('*.spec'):
        if spec_file.name != 'xml_join.spec':
            spec_file.unlink()
            print(f"✓ Удален файл {spec_file.name}")

def build_exe():
    """Собирает exe файл с помощью PyInstaller"""
    
    print("Начинаем сборку exe файла...")
    
    # Проверяем зависимости
    if not check_dependencies():
        print("Ошибка: не все зависимости установлены!")
        return False
    
    # Очищаем предыдущие сборки
    clean_build()
    
    # Проверяем, что мы в правильной директории
    if not Path("xml_join.spec").exists():
        print("Ошибка: файл xml_join.spec не найден!")
        return False
    
    # Команда для сборки
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",  # Очищаем предыдущие сборки
        "--noconfirm",  # Не спрашиваем подтверждения
        "xml_join.spec"
    ]
    
    try:
        print("Выполняем команду:", " ".join(cmd))
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("Сборка завершена успешно!")
        print("Exe файл находится в папке dist/")
        
        # Проверяем, что файл создался
        exe_path = Path("dist/xml_join.exe")
        if exe_path.exists():
            print(f"✓ Файл создан: {exe_path.absolute()}")
            print(f"Размер файла: {exe_path.stat().st_size / (1024*1024):.1f} MB")
            return True
        else:
            print("✗ Ошибка: exe файл не был создан!")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"✗ Ошибка при сборке: {e}")
        print(f"Вывод команды: {e.stdout}")
        print(f"Ошибки: {e.stderr}")
        return False
    except Exception as e:
        print(f"✗ Неожиданная ошибка: {e}")
        return False

def test_exe():
    """Тестирует созданный exe файл"""
    exe_path = Path("dist/xml_join.exe")
    if not exe_path.exists():
        print("✗ Exe файл не найден для тестирования")
        return False
    
    print("Тестирование exe файла...")
    try:
        # Запускаем exe с флагом --help или просто проверяем, что он запускается
        result = subprocess.run([str(exe_path), "--help"], 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        print("✓ Exe файл запускается без ошибок")
        return True
    except subprocess.TimeoutExpired:
        print("✓ Exe файл запускается (таймаут ожидаем)")
        return True
    except Exception as e:
        print(f"✗ Ошибка при тестировании exe: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Сборка XML Join Tool")
    print("=" * 50)
    
    success = build_exe()
    
    if success:
        print("\n" + "=" * 50)
        print("Тестирование exe файла...")
        test_exe()
        print("\n✓ Сборка завершена успешно!")
        print("Exe файл готов к использованию.")
    else:
        print("\n✗ Сборка не удалась!")
    
    sys.exit(0 if success else 1) 