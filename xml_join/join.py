from lxml import etree
from collections import defaultdict


def prettyprint(element, **kwargs):
    xml = etree.tostring(element, pretty_print=True, **kwargs)
    print(xml.decode(), end='')

def create_user(login, first_name, last_name, second_name, email, work_pos, dep_names, pers_phone=''):
    user = etree.Element("user")
    etree.SubElement(user, "LOGIN").text = login
    etree.SubElement(user, "FIRST_NAME").text = first_name
    etree.SubElement(user, "LAST_NAME").text = last_name
    etree.SubElement(user, "SECOND_NAME").text = second_name
    etree.SubElement(user, "EMAIL").text = email
    etree.SubElement(user, "WORK_POSITION").text = work_pos
    etree.SubElement(user, "DEP_NAMES").text = dep_names
    etree.SubElement(user, "PERS_PHONE").text = pers_phone





with (open('../tests/fixtures/users.xml', 'rb') as f_users,
      open('../tests/fixtures/deps.xml', 'rb') as f_deps):
    users = etree.parse(f_users)
    users_root = users.getroot()
    deps = etree.parse(f_deps)
    deps_root = deps.getroot()
    deps_dict = {}
    users_l = []

    for dep in deps_root:               # dep_id, dep_name
        deps_dict[dep[1]] = dep[0]
    for user in users_root:             # user_id, dep_id
        users_l.append((user[0], user[11]))

    user_deps_dict = defaultdict(list)
    for user in users:
        user_deps_dict[user[0]] = deps_dict.get(user[11])

    users_deps_root = etree.Element("users")

    for _ in range(len(users_root)):
        users_deps_root.append(create_user())

    print(users_root.tag)
    print(deps_root.tag)





