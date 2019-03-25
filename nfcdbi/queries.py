#!/usr/bin/python2.7

""" Mysql queries relative to the project
"""

import datetime


# Create db
def create_db(dbname):
    return """
    CREATE DATABASE IF NOT EXISTS {0};
    """.format(dbname)

def select_db(dbname):
    return "USE {0};".format(dbname)

# Create table item
def create_battery_table(dbname):
    return """
    CREATE TABLE IF NOT EXISTS battery (
    battery_id INT AUTO_INCREMENT,
    nfcid VARCHAR(255) NOT NULL,
    comment VARCHAR(255) DEFAULT NULL,
    n_charge_cycles INT NOT NULL DEFAULT 0,
    last_charge DATETIME DEFAULT NULL,
    last_use DATETIME DEFAULT NULL,
    inserted_date DATE NOT NULL,
    PRIMARY KEY (battery_id)
)  ENGINE=INNODB COMMENT="Table to monitor batteries";
    """.format(dbname)

# Insert a battery
def insert_battery(dbname, nfcid, comment):
    return """
    INSERT INTO `{0}`.`battery`
    (`nfcid`, `comment`, `inserted_date`)
    VALUES
    ("{1}", "{2}", "{3}");
    """.format(dbname,
               nfcid,
               comment,
               datetime.datetime.now())

# List batteries
def list_batteries(dbname):
    return "SELECT * FROM {0}.battery;".format(dbname)


# Select battery on given nfcid
def get_battery_nfcid(dbname, nfcid):
    return """
    SELECT * FROM {0}.battery WHERE (nfcid = "{1}");
    """.format(dbname, nfcid)

# Remove battery on given nfcid
def rm_battery_nfcid(dbname, nfcid):
    return """
    DELETE FROM {0}.battery WHERE (nfcid = "{1}");
    """.format(dbname, nfcid)

# add battery to charging
def battery_charge(dbname, nfcid):
    return """
    UPDATE `{0}`.`battery`
    SET `n_charge_cycles` = `n_charge_cycles` + 1,
        `last_charge` = '{2}'
    WHERE (`nfcid` = '{1}');
    """.format(dbname, nfcid, datetime.datetime.now())

# when a battery is used
def battery_use(dbname, nfcid):
    return """
    UPDATE `{0}`.`battery`
    SET `last_use` = '{2}'
    WHERE (`nfcid` = '{1}');
    """.format(dbname, nfcid, datetime.datetime.now())

# edit comment
def battery_edit_comment(dbname, nfcid, comment):
    return """
    UPDATE `{0}`.`battery`
    SET `comment` = '{2}'
    WHERE (`nfcid` = '{1}');
    """.format(dbname, nfcid, comment)
