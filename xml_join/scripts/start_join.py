import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import os
import sys
from pathlib import Path

# Добавляем родительскую директорию в путь для импорта модулей
sys.path.append(str(Path(__file__).parent.parent.parent))
from xml_join.join import process_xml


class XMLJoinApp(toga.App):
    def __init__(self):
        super().__init__(
            formal_name="XML Join Tool",
            app_id="org.xmljoin.tool",
            app_name="xml_join_tool",
            version="1.0.0",
            description="Tool for joining XML files with user and department data"
        )
        self.xml1_path = None
        self.xml2_path = None
        self.output_path = None

    def startup(self):
        # Создаем главное окно
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=20))

        # Заголовок
        title = toga.Label(
            'XML Join Tool',
            style=Pack(font_size=24, font_weight='bold', padding_bottom=20)
        )
        main_box.add(title)

        # Выбор первого XML файла
        xml1_box = toga.Box(style=Pack(direction=ROW, padding=5))
        xml1_label = toga.Label('XML файл 1 (пользователи):', style=Pack(width=200))
        self.xml1_path_label = toga.Label('Не выбран', style=Pack(flex=1))
        xml1_button = toga.Button(
            'Выбрать файл',
            on_press=self.select_xml1,
            style=Pack(padding_left=10)
        )
        xml1_box.add(xml1_label)
        xml1_box.add(self.xml1_path_label)
        xml1_box.add(xml1_button)
        main_box.add(xml1_box)

        # Выбор второго XML файла
        xml2_box = toga.Box(style=Pack(direction=ROW, padding=5))
        xml2_label = toga.Label('XML файл 2 (департаменты):', style=Pack(width=200))
        self.xml2_path_label = toga.Label('Не выбран', style=Pack(flex=1))
        xml2_button = toga.Button(
            'Выбрать файл',
            on_press=self.select_xml2,
            style=Pack(padding_left=10)
        )
        xml2_box.add(xml2_label)
        xml2_box.add(self.xml2_path_label)
        xml2_box.add(xml2_button)
        main_box.add(xml2_box)

        # Выбор папки для сохранения
        output_box = toga.Box(style=Pack(direction=ROW, padding=5))
        output_label = toga.Label('Папка для сохранения:', style=Pack(width=200))
        self.output_path_label = toga.Label('Не выбрана', style=Pack(flex=1))
        output_button = toga.Button(
            'Выбрать папку',
            on_press=self.select_output_folder,
            style=Pack(padding_left=10)
        )
        output_box.add(output_label)
        output_box.add(self.output_path_label)
        output_box.add(output_button)
        main_box.add(output_box)

        # Кнопка обработки
        process_button = toga.Button(
            'Обработать файлы',
            on_press=self.process_files,
            style=Pack(padding_top=20)
        )
        main_box.add(process_button)

        # Статус
        self.status_label = toga.Label(
            'Готов к обработке',
            style=Pack(padding_top=20, font_size=12)
        )
        main_box.add(self.status_label)

        # Создаем главное окно
        self.main_window = toga.MainWindow(title='XML Join Tool')
        self.main_window.content = main_box
        self.main_window.show()

    async def select_xml1(self, widget):
        try:
            file_path = await self.main_window.open_file_dialog(
                title='Выберите первый XML файл',
                file_types=['xml']
            )
            if file_path:
                self.xml1_path = str(file_path)
                self.xml1_path_label.text = os.path.basename(self.xml1_path)
                self.update_status()
        except Exception as e:
            self.status_label.text = f'Ошибка при выборе файла: {str(e)}'

    async def select_xml2(self, widget):
        try:
            file_path = await self.main_window.open_file_dialog(
                title='Выберите второй XML файл',
                file_types=['xml']
            )
            if file_path:
                self.xml2_path = str(file_path)
                self.xml2_path_label.text = os.path.basename(self.xml2_path)
                self.update_status()
        except Exception as e:
            self.status_label.text = f'Ошибка при выборе файла: {str(e)}'

    async def select_output_folder(self, widget):
        try:
            folder_path = await self.main_window.open_folder_dialog(
                title='Выберите папку для сохранения'
            )
            if folder_path:
                self.output_path = str(folder_path)
                self.output_path_label.text = os.path.basename(self.output_path)
                self.update_status()
        except Exception as e:
            self.status_label.text = f'Ошибка при выборе папки: {str(e)}'

    def update_status(self):
        if self.xml1_path and self.xml2_path and self.output_path:
            self.status_label.text = 'Все файлы выбраны. Готов к обработке.'
        else:
            missing = []
            if not self.xml1_path:
                missing.append('XML файл 1')
            if not self.xml2_path:
                missing.append('XML файл 2')
            if not self.output_path:
                missing.append('папка для сохранения')
            self.status_label.text = f'Не выбрано: {", ".join(missing)}'

    async def process_files(self, widget):
        if not all([self.xml1_path, self.xml2_path, self.output_path]):
            self.status_label.text = 'Пожалуйста, выберите все необходимые файлы и папку.'
            return

        try:
            self.status_label.text = 'Обработка файлов...'
            
            # Вызываем функцию обработки из модуля join
            process_xml(self.xml1_path, self.xml2_path, self.output_path)
            
            self.status_label.text = 'Обработка завершена успешно!'
            
            # Показываем сообщение об успехе
            await self.main_window.dialog(toga.InfoDialog(
                'Успех',
                f'Файлы успешно обработаны!\n\n'
                f'XML 1: {os.path.basename(self.xml1_path)}\n'
                f'XML 2: {os.path.basename(self.xml2_path)}\n'
                f'Результат сохранен в: {self.output_path}/user_deps.xlsx'
            ))
            
        except Exception as e:
            error_msg = f'Ошибка при обработке файлов: {str(e)}'
            self.status_label.text = error_msg
            
            # Показываем сообщение об ошибке
            await self.main_window.dialog(toga.ErrorDialog(
                'Ошибка',
                error_msg
            ))


def main():
    return XMLJoinApp()


if __name__ == '__main__':
    app = main()
    app.main_loop()
