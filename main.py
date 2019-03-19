#!/usr/bin/python2.7

""" Main of NFC DB inventory project
"""

# python core
import sys

# project imports
import nfcdbi.acr122u as acr

def main(usb_bus, usb_dev):
    """
    """
    acr_dev = acr.AcrDev(usb_bus, usb_dev);
    print(acr_dev)
    print(acr_dev.acquire())
    acr_dev.wait_for_tag()
    print(acr_dev.last_nfcid)

if __name__ == "__main__":

    if (len(sys.argv) <= 1):
        print("\n\033[1;31mError: No USB information was provided.\033[0m");
        print("Usage: python main.py usb_bus usb_dev")
    else:
        main(sys.argv[1], sys.argv[2])
