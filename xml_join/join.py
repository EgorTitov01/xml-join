from lxml import etree
from collections import defaultdict


def prettyprint(element, **kwargs):
    xml = etree.tostring(element, pretty_print=True, **kwargs)
    print(xml.decode(), end='')


with (open('../tests/fixtures/users.xml', 'rb') as f_users,
      open('../tests/fixtures/deps.xml', 'rb') as f_deps):
    users = etree.parse(f_users)
    users_root = users.getroot()
    deps = etree.parse(f_deps)
    deps_root = deps.getroot()
    deps_dict = {}
    # избавляемся от дублирования польз. с несколькими департаментами
    for dep in deps_root:
        deps_dict[dep[1].text] = dep[0].text      # dep_id: dep_name

    users_dict = {}
    user_deps = defaultdict(list)
    for user in users_root:
        user_txt = list(map(lambda u: u.text, user))
        dep_name = deps_dict.get(user_txt[11], '')
        if not users_dict.get(user_txt[0]):
            users_dict[user_txt[0]] = [user_txt[9], user_txt[2], user_txt[1],
                                   user_txt[3], user_txt[8], user_txt[10], dep_name, '']
        else:
            users_dict[user_txt[0]][6] += ('/ ' + dep_name)

    users_l = list(users_dict.values())




    print(users_l)





