#!/usr/bin/python2.7

""" Databases mysql embedded in a db object
"""

# mysql.connector dependency
import mysql.connector

# constants
DB_STATUS_CONNECTED = "connected"
DB_STATUS_DISCONNECTED = "disconnected"

class MysqlDb:
    """ Wrapper for mysql queries
    """

    def __init__(self, host, username):
        """ Constructor
        """
        self.host = host
        self.username = username
        self.status = DB_STATUS_DISCONNECTED

        self.db = None
        self.cursor = None

    def __str__(self):
        """ String representation
        """
        return "<MysqlDb {0} {1} {2}>".format(
            self.host,
            self.username,
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

