from lxml import etree
from pyexcelerate import Workbook, Style, Font
from datetime import datetime
import sys
import argparse

def process_xml(f_users, f_departments, output_path):
    try:
        to_xlsx(prepare_data(f_users, f_departments), output_path)
        print(f"Merging '{f_users}' and '{f_departments}' into '{output_path}'...")
    except Exception as e:
        print(f"Ошибка при обработке файлов. Проверьте правильность путей к файлам и наличие ошибок в файлах.")
        sys.exit(1)


def prepare_data(file_u,  file_deps):

    with (open(file_u, 'rb') as f_users,
          open(file_deps, 'rb') as f_deps):
        users = etree.parse(f_users)
        users_root = users.getroot()
        deps = etree.parse(f_deps)
        deps_root = deps.getroot()
        deps_dict = {}

        # избавляемся от дублирования польз. с несколькими департаментами
        for dep in deps_root:
            deps_dict[dep[1].text] = dep[0].text      # dep_id: dep_name

        users_dict = {}
        for user in users_root:
            user_txt = list(map(lambda u: u.text, user))
            dep_name = deps_dict.get(user_txt[11], '')
            if not users_dict.get(user_txt[0]):
                users_dict[user_txt[0]] = [user_txt[9], user_txt[2], user_txt[1],
                                       user_txt[3], user_txt[8], user_txt[10], dep_name, user_txt[6][:10], '']
            else:
                users_dict[user_txt[0]][6] += ('/ ' + dep_name)

        columns = ['Логин', 'Имя', 'Фамилия', 'Отчество', 'E-Mail', 'Должность', 'Подразделения', 'Дата приема', 'Личный мобильный' ]
        return [columns] + list(users_dict.values())


def to_xlsx(data, output_path):
    wb = Workbook()
    ws = wb.new_sheet("Sheet1", data=data)

    ws.get_row_style(1).font.bold = True
    for col in range(1,9):
        ws.get_col_style(col).size = 20

    # Получаем текущую дату в формате ДД_ММ_ГГГГ
    current_date = datetime.now().strftime("%d_%m_%Y")
    
    # Создаем имя файла с датой
    filename = f"user_deps_{current_date}.xlsx"
    
    wb.save(output_path + '/' + filename)
    print(f"Файл сохранен: {output_path}/{filename}")


def main():
    parser = argparse.ArgumentParser(
        description='Утилита для объединения XML файлов с данными о пользователях и департаментах',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python -m xml_join.join --users users.xml --deps departments.xml --output output_folder
  ./xml_join.exe --users users.xml --deps departments.xml --output output_folder
        """
    )
    
    parser.add_argument('--users', required=True, help='XML файл с данными о пользователях')
    parser.add_argument('--deps', required=True, help='XML файл с данными о департаментах')
    parser.add_argument('--output', required=True, help='Папка для сохранения результата')
    
    args = parser.parse_args()
    
    try:
        process_xml(args.users, args.deps, args.output)
        print("Обработка завершена успешно!")
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()





