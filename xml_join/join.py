from lxml import etree
from pyexcelerate import Workbook, Style, Font


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
                                       user_txt[3], user_txt[8], user_txt[10], dep_name, '']
            else:
                users_dict[user_txt[0]][6] += ('/ ' + dep_name)

        columns = ['Логин', 'Имя', 'Фамилия', 'Отчество', 'E-Mail', 'Должность', 'Подразделения', 'Личный мобильный' ]
        return [columns] + list(users_dict.values())


def to_xlsx(data):
    wb = Workbook()
    ws = wb.new_sheet("Sheet1", data=data)

    ws.get_row_style(1).font.bold = True
    for col in range(1,9):
        ws.get_col_style(col).size = 20

    wb.save("user_deps.xlsx")
    print("Файл создан.")





