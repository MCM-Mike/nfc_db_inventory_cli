#!/usr/bin/python2.7

""" Main of NFC DB inventory project
"""

# python core
import sys
import argparse

# project imports
import nfcdbi.acr122u as acr
import nfcdbi.db as db
import nfcdbi.queries as queries

def main(args):
    """
    """


    acr_dev = acr.AcrDev(args.usb_bus, args.usb_dev)
    acr_dev.acquire()

    if (acr_dev.is_connected()):
        acr_dev.wait_for_tag()
        print(acr_dev.last_nfcid)

    mydb = db.MysqlDb("localhost", "root")

    if not mydb.connect("PIEber.400"):
        return

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

    parser = argparse.ArgumentParser()

    parser.add_argument("-b", "--usb_bus", help="usb bus where NFC reader is available")
    parser.add_argument("-d", "--usb_dev", help="usb device identifier")
    parser.add_argument("-n", "--db_name", help="name of the database to be used")

    args = parser.parse_args()

    print(args)

    main(args)
