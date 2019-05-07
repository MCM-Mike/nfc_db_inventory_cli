#!/usr/bin/python2.7

""" CLI module to display menus

Menu's texts are set in the given configuration file.
"""

import sys
import math
import textwrap

import queries as queries

# need to add the path of config
MENU_KEYWORD = "menu"
MENU_NO_NAME = "no_name"
MENU_DESC_KEYWORD = "->"
MENU_ITEM_KEYWORD = ">"


def menus_get(cli_config_file):
    """ Retreive all menus in the cli_config_file.

    @return: dictionary with all menus
    """
    with open(cli_config_file, 'r') as f:
        lines = f.readlines();
        in_menu = False
        menus = {}
        menu_name = MENU_NO_NAME

        for i, l in enumerate(lines):
            if l.startswith(MENU_KEYWORD):
                try:
                    menu_name = l.split(":")[1].strip()
                except IndexError as e:
                    print("error retreiving menu line {}: '{}'".format(
                        str(i), l.strip()))
                    sys.exit(1)

                menus[menu_name] = {
                    "name": menu_name,
                    "desc": "",
                    "choices": [],
                }
                in_menu = True
            elif l.startswith(MENU_DESC_KEYWORD):
                menus[menu_name]["desc"] += l[2:].strip() + " "
            elif l.startswith(MENU_ITEM_KEYWORD):
                menus[menu_name]["choices"].append(l[2:].strip())
            else:
                # not a menu line
                menu_name = MENU_NO_NAME
        f.close()

    return menus

def menu_display(menu):
    """ Display the selected given menu

    @menu_name: menu dictionary with `desc` and `choices` keys.
    """
    print("\033[2;37m\n<MENU: {title}>\n{desc}\033[0m".format(
        title = menu["name"],
        desc = menu["desc"]));

    for i, c in enumerate(menu["choices"]):
        # +1 to avoid choice 0
        print("\033[2;37m\t{itemno}) {text}\033[0m".format(
            itemno = i + 1,
            text = menu["choices"][i]))

def print_list(tname,
               columns,
               data,
               print_total=False):
    """
    """
    count = 0

    for i, d in enumerate(data):
        count += 1
        for j, x in enumerate(d):
            col = columns[j]

            if (col != "nfcid"):
                print("{0: <20}: {1}".format(
                    col,
                    x))
            else:
                print("{0: <20}: \033[1;35m{1}\033[0m".format(
                    col,
                    x))
        print "--"

    if print_total:
        print "\n# of registered NFCID ({0}): \033[1;34m{1}\033[0m\n".format(tname,
                                                                           count)

def print_tables(db,
                 *tables):
    """
    """
    for tname in tables:
        res = db.execute(queries.table_list(db.dbname,
                                            tname),
                         True)
        cols = db.execute(queries.table_columns_name(db.dbname,
                                                     tname),
                          True)

        print_list(tname,
                   [c[0] for c in cols],
                   res,
                   print_total=True)
