#!usr/bin/env python3

from xml_join.join import prepare_data, to_xlsx


def main():
    f_users = '../../tests/fixtures/users.xml'
    f_departments = '../../tests/fixtures/deps.xml'

    to_xlsx(prepare_data(f_users, f_departments))


if __name__ == '__main__':

    main()