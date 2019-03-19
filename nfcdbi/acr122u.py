#!/usr/bin/python2.7

""" NFC related functions, through acr122u hardware.
"""

# pip install nfcpy
import nfc


def on_startup(targets):
    for target in targets:
        target.sensf_req = bytearray.fromhex("0012FC0000")
    return targets

def on_connect(tag):
    #print(tag)
    pass

class AcrDev:
    """ Class to abstract ACR122U device.
    """

    # class variables
    def __init__(self, usb_bus, usb_dev):
        """ Constructor of the class
        """
        self.usb_bus = usb_bus
        self.usb_dev = usb_dev
        self.usb_target = 'usb:{bus}:{dev}'.format(bus = self.usb_bus,
                                                   dev = self.usb_dev)

        self.rdwr_options = {
            'targets': ['106A'],        # type2tag, nfcA
            'on-startup': on_startup,
            'on-connect': on_connect,
        }

        self.last_nfcid = "";

    def __str__(self):
        """ String representation of the class
        """
        return '<AcrDev on {0}>'.format(self.usb_target);

    def acquire(self):
        """ Acquire the device from USB bus.
        To find the device, use the linux command: `lsusb`.

        @return: true if device was acquired, false otherwise.
        """
        clf = nfc.ContactlessFrontend()

        if clf.open('usb:{bus}:{dev}'.format(bus = self.usb_bus,
                                             dev = self.usb_dev)):
            print("dev {0} acquired successfully".format(self.usb_target))
            return True

        return False

    def wait_for_tag(self):
        """ Wait RF modulation from detected tag
        """
        try:

            with nfc.ContactlessFrontend(self.usb_target) as clf:
                tag = clf.connect(rdwr = self.rdwr_options)
                self.last_nfcid = ''.join('{:02x}'.format(x) for x in tag._nfcid)

        except IOError as ioe:
            print("Err: '" + self.usb_target + "' " + str(ioe))

