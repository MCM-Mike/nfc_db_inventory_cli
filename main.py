#!/usr/bin/python2.7

""" Main of NFC DB inventory project
"""

# python core
import sys
import argparse
import select
import time

# project imports
import nfcdbi.acr122u as acr
import nfcdbi.db as db
import nfcdbi.queries as queries
import nfcdbi.cli as cli

CLI_CONFIG_FILE = "./cli_config.txt"

def main(args):
    """
    """

    # acquire hardware
    acr_dev = acr.AcrDev(args.usb_bus, args.usb_dev)
    acr_dev.acquire()

    # connect to mysql server
    # FIXME: from config file
    mydb = db.MysqlDb(args.db_host, args.db_user)
    if not mydb.connect("PIEber.400"):
        return

    # recover menus from config file
    cli_menus = cli.menus_get(CLI_CONFIG_FILE)

    while True:
        cli.menu_display(cli_menus["principal"])
        try:
            sys.stdout.write("> ")
            choice = input()
        except Exception as e:
            print("Invalid character")
            continue

        if (choice == 1):
            # db list battery of print no battery registered if empty.
            res = mydb.execute(queries.list_batteries(args.db_name), True)
            cols = mydb.execute(queries.get_columns_name(args.db_name), True)

            cli.print_battery_list([c[0] for c in cols], res)

        elif (choice == 2):
            # next tag get info in DB, or register if not known.
            print("Wait for tag to get nfcid...");
            acr_dev.wait_for_tag();
            print("NFCID: \033[1;32m{0}\033[0m".format(acr_dev.last_nfcid))

            # check if exists
            res = mydb.execute(queries.get_battery_nfcid(args.db_name, acr_dev.last_nfcid),
                               True)

            if not res:
                print("Unkown tag")
            else:
                print(res)


        elif (choice == 3):
            # next tags are registered as used, and when user enters "end",
            # it prints a summary of used tag.
            print("Scan the battery to be used:")

            # list of battery + confirmation at the end?

            acr_dev.wait_for_tag();
            print "added to backpack: " + acr_dev.last_nfcid

            while True:
                i, o, e = select.select([sys.stdin], [], [], 5)

                if i:
                    if sys.stdin.readline().strip() == "end":
                        print "Summary: (+ confirmation)"
                else:
                    acr_dev.wait_for_tag();
                    print "added to backpack: " + acr_dev.last_nfcid



        elif (choice == 4):
            # next tags are marked as in charge, until user enters "end".
            print("4")

        elif (choice == 5):
            # next tag is registers in the db, except if it is already known.
            print("5")

        elif (choice == 6):
            print("bye")
            return

        else:
            print("Invalid choice.")

    print(mydb)

    print mydb.execute(queries.create_db(args.db_name))
    print mydb.execute(queries.select_db(args.db_name))
    print mydb.execute(queries.create_battery_table(args.db_name))
    print mydb.execute(queries.insert_battery(args.db_name, "AAAAC", "test"))
    print mydb.execute(queries.get_battery_nfcid(args.db_name, "AAAAD"), fetch=True)
    print mydb.execute(queries.rm_battery_nfcid(args.db_name, "AAAA"))
    print mydb.execute(queries.battery_charge(args.db_name, "AAAAD"))
    print mydb.execute(queries.battery_use(args.db_name, "AAAAD"))
    print mydb.execute(queries.battery_edit_comment(args.db_name, "AAAAD", "TTTTTT"))

    mydb.close()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="""
        Database manager related to NFC tags.
        Use lsusb to find the USB bus and device of your NFC reader/writer.
        """
    )

    parser.add_argument("-b", "--usb_bus", required=True,
                        help="usb bus where NFC reader is available")
    parser.add_argument("-d", "--usb_dev", required=True,
                        help="usb device identifier")
    parser.add_argument("-n", "--db_name", required=True,
                        help="name of the database to be used")
    parser.add_argument("--db_user", default="root",
                        help="name of the user for the database (default: root)")
    parser.add_argument("--db_host", default="localhost",
                        help="host for the database (default: localhost)")

    args = parser.parse_args()

    main(args)

