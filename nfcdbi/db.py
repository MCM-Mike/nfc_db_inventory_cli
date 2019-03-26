#!/usr/bin/python2.7

""" Databases mysql embedded in a db object
"""

# mysql.connector dependency
import mysql.connector

# local imports
import queries

# constants
DB_STATUS_CONNECTED = "connected"
DB_STATUS_DISCONNECTED = "disconnected"

class MysqlDb:
    """ Wrapper for mysql queries
    """

    def __init__(self,
                 host,
                 username,
                 password,
                 dbname):
        """ Constructor
        """
        self.host = host
        self.username = username
        self.dbname = dbname
        self.status = DB_STATUS_DISCONNECTED

        self.db = None
        self.cursor = None

        # try to connect
        if not self.connect(password):
            print "Error trying to connect database {0}".format(
                self.dbname)
            return None

        # create the db if not exist and select it
        res = self.execute(queries.create_db(self.dbname))

        if not res:
            print "Error trying to create the database {0}".format(
                self.dbname)
            return None

        # select the db to be used
        res = self.execute(queries.select_db(self.dbname))

        if not res:
            print "Error trying to select the database {0}".format(
                self.dbname)
            return None

        # try to create battery db if it doesnt exists
        res = self.execute(queries.create_battery_table(self.dbname))

        if not res:
            print "Error trying to create battery table for the database {0}".format(
                self.dbname)
            return None


    def __str__(self):
        """ String representation
        """
        return "<MysqlDb {0} {1} {2} {3}>".format(
            self.host,
            self.username,
            self.dbname,
            self.status)

    def close(self):
        """ Disconnect the driver
        """
        self.db.close()

    def connect(self, password):
        """ Connect to the database, return True on success,
        False otherwise.
        """
        try:
            self.db = mysql.connector.connect(
                host = self.host,
                user = self.username,
                passwd = password,
            )

            self.cursor = self.db.cursor(buffered=True)
            self.status = DB_STATUS_CONNECTED
            return True

        except mysql.connector.errors.InterfaceError as ie:
            print "MYSQL IE error: ", ie
            self.status = DB_STATUS_DISCONNECTED
            return False

        except mysql.connector.errors.ProgrammingError as p:
            print "MYSQL PGR error: ", p
            self.status = DB_STATUS_DISCONNECTED
            return False

        except Exception as e:
            print "General exception catch: ", e
            self.status = DB_STATUS_DISCONNECTED
            return False

    def execute(self, query, fetch=False):
        """ Execute the query on the db.cursor
        """
        try:
            # print "Executing: {0}".format(query)
            self.cursor.execute(query)

            if not fetch:
                self.db.commit()
                return True
            else:
                return self.cursor.fetchall()

        except mysql.connector.errors.ProgrammingError as p:
            print "MYSQL PGR error: ", p
            return False

        except Exception as e:
            print "General exception catch: ", e
            return False



# some prepares queries
def check_if_battery_exists(db, nfcid):
    """ Return True if the nfcid is associated to a battery
    in the databse. False otherwise.
    """
    res = db.execute(queries.get_battery_nfcid(db.dbname,
                                               nfcid), True)
    if not res:
        return False

    return True

def get_battery_info(db, nfcid):
    """ Return a tuple:
    (# cycles of charge, # of use, last use date)
    of a battery. Return empty False if nfcid is unkown to the db.
    """
    res = db.execute(queries.get_battery_nfcid(db.dbname,
                                               nfcid), True)
    if not res:
        return False

    return (res[0][3], res[0][4], res[0][5])

