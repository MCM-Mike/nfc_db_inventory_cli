#!/usr/bin/python2.7

""" Test cli interface
"""

import sys

sys.path.append("../")

import nfcdbi.cli as cli


def main():
    """
    """
    menus = cli.menus_get();

    assert len(menus) == 2
    assert len(menus["first"]["choices"]) == 3
    assert len(menus["second"]["choices"]) == 4
    assert menus["first"]["name"] == "first"
    assert menus["second"]["name"] == "second"
    assert menus["first"]["desc"] == "Welcome to nfcdbi, what to do, on multiple lines: "

    cli.menu_display(menus["first"])
    cli.menu_display(menus["second"])

    print("\n\ncli tests done")

if __name__ == "__main__":
    main()

