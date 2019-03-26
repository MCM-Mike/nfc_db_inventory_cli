#!/usr/bin/python2.7

""" Main of NFC DB inventory project
"""

# python core
import sys
import argparse
import select

# project imports
import nfcdbi.acr122u as acr
import nfcdbi.db as db
import nfcdbi.queries as queries
import nfcdbi.cli as cli

CLI_CONFIG_FILE = "./cli_config.txt"
END_DELAY_SECOND = 3
END_INPUT = "end"

def main(args):
    """
    """

    # acquire hardware
    acr_dev = acr.AcrDev(args.usb_bus, args.usb_dev)
    acr_dev.acquire()

    # connect to mysql server
    # FIXME: from config file
    mydb = db.MysqlDb(args.db_host,
                      args.db_user,
                      args.db_passw,
                      args.db_name)

    if mydb.status == db.DB_STATUS_DISCONNECTED:
        sys.exit()

    # recover menus from config file
    cli_menus = cli.menus_get(CLI_CONFIG_FILE)

    while True:
        cli.menu_display(cli_menus["principal"])
        try:
            sys.stdout.write("> ")
            choice = input()
        except Exception as e:
            print "Invalid character"
            continue

        if (choice == 1):
            # db list battery of print no battery registered if empty.
            res = mydb.execute(queries.list_batteries(args.db_name), True)
            cols = mydb.execute(queries.get_columns_name(args.db_name), True)

            cli.print_battery_list([c[0] for c in cols],
                                   res,
                                   print_total=True)

        elif (choice == 2):
            # next tag get info in DB
            print "Wait for tag to get nfcid..."
            acr_dev.wait_for_tag();

            # check if exists
            res = mydb.execute(
                queries.get_battery_nfcid(mydb.dbname,
                                          acr_dev.last_nfcid),
                True)

            if res:
                print "\nNFCID: \033[1;32m{0}\033[0m\n".format(acr_dev.last_nfcid)
                cols = mydb.execute(
                    queries.get_columns_name(args.db_name),
                    True)

                cli.print_battery_list([c[0] for c in cols], res)
            else:
                print "\nNFCID: \033[1;31m{0}\033[0m\n".format(acr_dev.last_nfcid)
                print "Unkown tag"

        elif (choice == 3):
            # next tags are registered as used, and when user enters "end",
            # it prints a summary of used tag.
            insert = 0
            nfcids = set()

            print "Scan the battery to be used:"

            acr_dev.wait_for_tag();
            nfcids.add(acr_dev.last_nfcid)
            print "cantidate to backpack: " + acr_dev.last_nfcid

            while True:
                print "\n\033[2;37m(Type '{0}' then Enter to finish)\033[0m".format(END_INPUT)
                i, o, e = select.select([sys.stdin],
                                        [],
                                        [],
                                        END_DELAY_SECOND)

                if i:
                    if sys.stdin.readline().strip() == END_INPUT:
                        print nfcids
                        for nfcid in nfcids:
                            if not db.check_if_battery_exists(mydb,
                                                              nfcid):
                                print "\033[1;33m{0}\033[0m is not associated with a battery in the database. Skip.".format(
                                    nfcid)
                            else:
                                res = mydb.execute(
                                    queries.battery_use(mydb.dbname,
                                                        nfcid))
                                insert += 1
                                print "\033[1;32m{0}\033[0m update last_use date".format(nfcid)

                        print "# of batteries to be used: {0}".format(insert)
                        break
                else:
                    print "\033[2;32m(Ready to scan an other tag)\033[0m\n"
                    acr_dev.wait_for_tag();
                    nfcids.add(acr_dev.last_nfcid)
                    print "candidate to backpack: " + acr_dev.last_nfcid


        elif (choice == 4):
            # next tags are marked as in charge, until user enters "end".
            nfcids = set()

            print "Scan the battery to be charged:"
            acr_dev.wait_for_tag();
            print "candidate to charge: " + acr_dev.last_nfcid
            nfcids.add(acr_dev.last_nfcid)

            while True:
                print "\n\033[2;37m(Type '{0}' then Enter to finish)\033[0m".format(END_INPUT)
                i, o, e = select.select([sys.stdin],
                                        [],
                                        [],
                                        END_DELAY_SECOND)

                if i:
                    if sys.stdin.readline().strip() == END_INPUT:
                        # execute queries
                        for nfcid in nfcids:
                            if not db.check_if_battery_exists(mydb,
                                                              nfcid):
                                print "\033[1;33m{0}\033[0m is not associated with a battery in the database. Skip.".format(
                                    nfcid)
                            else:
                                res = mydb.execute(
                                    queries.battery_charge(mydb.dbname,
                                                           nfcid))
                                print "\033[1;32m{0}\033[0m charge cycle incremented by one.".format(nfcid)

                        print "# of batteries to be charged: {0}".format(len(nfcids))
                        break
                else:
                    print "\033[2;32m(Ready to scan an other tag)\033[0m\n"
                    acr_dev.wait_for_tag();
                    nfcids.add(acr_dev.last_nfcid)
                    print "candidate to charge: " + acr_dev.last_nfcid

        elif (choice == 5):
            # next tag is registers in the db, except if it is already known.
            print "Scan the battery to be inserted:"
            acr_dev.wait_for_tag();

            res = mydb.execute(
                queries.get_battery_nfcid(mydb.dbname,
                                          acr_dev.last_nfcid),
                True)

            if not res:
                print "\nNFCID: \033[1;32m{0}\033[0m\n".format(acr_dev.last_nfcid)
                print "\nEnter a comment for the current battery:"
                comment = raw_input()

                res = mydb.execute(
                    queries.insert_battery(mydb.dbname,
                                           acr_dev.last_nfcid,
                                           comment))
                print "\033[1;32mBattery inserted\033[0m"
            else:
                print "\nNFCID: \033[1;31m{0}\033[0m\n".format(acr_dev.last_nfcid)
                print "Battery already inserted:\n"
                cols = mydb.execute(
                    queries.get_columns_name(mydb.dbname), True)

                cli.print_battery_list([c[0] for c in cols], res)

        elif (choice == 6):
            mydb.close()
            print "bye"
            return

        else:
            print "\033[1;31mInvalid choice.\033[0m"


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
    parser.add_argument("--db_passw", default="",
                        help="password for the database (default: '')")

    args = parser.parse_args()

    main(args)

