"""
XML → XLSX Joiner (Toga + WinForms backend)

Требует:  pythonnet  +toga-core +toga-winforms
          (под Windows 10/11 .NET Framework 4.8 уже установлен)

Сборка EXE (из той же папки):
    pyinstaller --noconsole --onefile ^
        --hidden-import=clr ^
        --hidden-import=pythonnet ^
        --collect-submodules=toga_winforms ^
        --copy-metadata=toga-core --copy-metadata=toga-winforms ^
        xml_join_toga.py
"""
from __future__ import annotations
from xml_join.join import process_xml
import os
import sys
from pathlib import Path

# ──────────────────── pythonnet: до импорта Toga ────────────────────
if sys.platform.startswith("win"):
    try:
        import pythonnet  # noqa: WPS433
        pythonnet.set_runtime("msnet48")  # .NET Framework 4.8
    except Exception:                      # fallback — задать через env
        os.environ.setdefault("PYTHONNET_RUNTIME", "msnet")

# ──────────────────────────── GUI ────────────────────────────
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, LEFT


class XMLJoinerApp(toga.App):
    def startup(self) -> None:            # создаём интерфейс
        self.xml1_path = None
        self.xml2_path = None
        self.xlsx_path = None

        main = toga.Box(style=Pack(direction=COLUMN, padding=16))

        # ─── XML #1 ───
        main.add(toga.Button("Выбрать XML #1…", on_press=self.pick_xml1,
                             style=Pack(padding=(0, 8))))
        self.lbl1 = toga.Label("XML #1: (не выбрано)",
                               style=Pack(padding=(0, 8), alignment=LEFT))
        main.add(self.lbl1)

        # ─── XML #2 ───
        main.add(toga.Button("Выбрать XML #2…", on_press=self.pick_xml2,
                             style=Pack(padding=(0, 8))))
        self.lbl2 = toga.Label("XML #2: (не выбрано)",
                               style=Pack(padding=(0, 8), alignment=LEFT))
        main.add(self.lbl2)

        # ─── XLSX ───
        main.add(toga.Button("Сохранить как XLSX…", on_press=self.pick_xlsx,
                             style=Pack(padding=(0, 8))))
        self.lbl3 = toga.Label("XLSX: (не выбрано)",
                               style=Pack(padding=(0, 8), alignment=LEFT))
        main.add(self.lbl3)

        # ─── Merge ───
        main.add(toga.Button("Объединить", on_press=self.merge_files,
                             style=Pack(padding=(12, 16))))

        self.main_window = toga.MainWindow(self.formal_name)
        self.main_window.content = main
        self.main_window.show()

    # ────────── Callbacks ──────────
    def pick_xml1(self, _: toga.Widget) -> None:
        path = self.main_window.open_file_dialog("Выберите первый XML",
                                                 initial_directory=str(Path.home()))
        if path:
            self.xml1_path, self.lbl1.text = path, f"XML #1: {path}"

    def pick_xml2(self, _: toga.Widget) -> None:
        start = str(Path(self.xml1_path).parent) if self.xml1_path else str(Path.home())
        path = self.main_window.open_file_dialog("Выберите второй XML",
                                                 initial_directory=start)
        if path:
            self.xml2_path, self.lbl2.text = path, f"XML #2: {path}"

    def pick_xlsx(self, _: toga.Widget) -> None:
        start = str(Path(self.xml1_path).parent) if self.xml1_path else str(Path.home())
        path = self.main_window.save_file_dialog("Сохранить как XLSX",
                                                 suggested_filename="merged.xlsx",
                                                 initial_directory=start)
        if path:
            if not path.lower().endswith(".xlsx"):
                path += ".xlsx"
            self.xlsx_path, self.lbl3.text = path, f"XLSX: {path}"

    def merge_files(self, _: toga.Widget) -> None:
        if not all((self.xml1_path, self.xml2_path, self.xlsx_path)):
            self.main_window.error_dialog("Ошибка", "Не выбраны все файлы!")
            return
        try:
            process_xml(self.xml1_path, self.xml2_path, self.xlsx_path)
            self.main_window.info_dialog("Готово",
                                         f"Файл сохранён:\n{self.xlsx_path}")
        except Exception as exc:          # pragma: no cover
            self.main_window.error_dialog("Ошибка обработки", str(exc))


def main() -> XMLJoinerApp:              # требуется Briefcase’ом
    return XMLJoinerApp("XML → XLSX Joiner", "org.example.xmljoiner")


if __name__ == "__main__":
    main().main_loop()

