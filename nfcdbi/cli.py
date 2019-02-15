#!/usr/bin/python2.7

""" CLI module to display menus

Menu's texts are set in the CLI_CONFIG_FILE.
"""

import sys

# need to add the path of config
CLI_CONFIG_FILE = "cli_config.txt"
MENU_KEYWORD = "menu"
MENU_NO_NAME = "no_name"
MENU_DESC_KEYWORD = "->"
MENU_ITEM_KEYWORD = ">"


def menus_get():
    """ Retreive all menus in the CLI_CONFIG_FILE.

    @return: dictionary with all menus
    """
    # try:
    with open(CLI_CONFIG_FILE, 'r') as f:
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
    # except:
    #     print("1.. error catched");
    return menus

def menu_display(menu):
    """ Display the selected given menu

    @menu_name: menu dictionary with `desc` and `choices` keys.
    """
    print("<MENU: {title}>\n{desc}".format(
        title = menu["name"],
        desc = menu["desc"]));

    for i, c in enumerate(menu["choices"]):
        # +1 to avoid choice 0
        print("\t{itemno}) {text}".format(
            itemno = i + 1,
            text = menu["choices"][i]))
