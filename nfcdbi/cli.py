#!/usr/bin/python2.7

""" CLI module to display menus

Menu's texts are set in the given configuration file.
"""

import sys
import math
import textwrap

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
    print("\n<MENU: {title}>\n{desc}".format(
        title = menu["name"],
        desc = menu["desc"]));

    for i, c in enumerate(menu["choices"]):
        # +1 to avoid choice 0
        print("\t{itemno}) {text}".format(
            itemno = i + 1,
            text = menu["choices"][i]))



def print_battery_list(columns, data):
    """
    """

    for d in data:
        for i,x in enumerate(d):
            col = columns[i]

            if (col != "nfcid"):
                print("{0: <20}: {1}".format(
                    col,
                    x))
            else:
                print("{0: <20}: \033[1;35m{1}\033[0m".format(
                    col,
                    x))
        print "--"


    # get longest wrap of 15 chars
    # print([textwrap.wrap(text=w, width=15) for r in data for w in r[1]])
    # longest_wrap = max(len())
    #                    for r in data
    #                    for w in r[1])

