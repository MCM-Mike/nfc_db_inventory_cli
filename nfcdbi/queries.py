#!/usr/bin/python2.7

""" Mysql queries relative to the project
"""

import datetime

BATTERY_TNAME = "battery"
DRONE_TNAME = "drone"

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
    CREATE TABLE IF NOT EXISTS `{0}`.`{1}` (
    battery_id INT AUTO_INCREMENT,
    nfcid VARCHAR(255) NOT NULL,
    comment VARCHAR(255) DEFAULT NULL,
    n_charge_cycles INT NOT NULL DEFAULT 0,
    last_charge DATETIME DEFAULT NULL,
    last_use DATETIME DEFAULT NULL,
    inserted_date DATE NOT NULL,
    PRIMARY KEY (battery_id)
)  ENGINE=INNODB COMMENT="Table to monitor batteries";
    """.format(dbname, BATTERY_TNAME)

# Create table drone
def create_drone_table(dbname):
    return """
    CREATE TABLE IF NOT EXISTS `{0}`.`{1}` (
    drone_id INT AUTO_INCREMENT,
    nfcid VARCHAR(255) NOT NULL,
    comment VARCHAR(255) DEFAULT NULL,
    n_use INT NOT NULL DEFAULT 0,
    last_use DATETIME DEFAULT NULL,
    inserted_date DATE NOT NULL,
    PRIMARY KEY (drone_id)
)  ENGINE=INNODB COMMENT="Table to monitor drones use";
    """.format(dbname, DRONE_TNAME)

# Get table info
def table_columns_name(dbname, tname):
    return "DESC `{0}`.`{1}`;".format(dbname, tname)

# Insert an object
def table_insert(dbname, tname, nfcid, comment):
    return """
    INSERT INTO `{0}`.`{1}`
    (`nfcid`, `comment`, `inserted_date`)
    VALUES
    ('{2}', '{3}', '{4}');
    """.format(dbname,
               tname,
               nfcid,
               comment,
               datetime.datetime.now())

# List batteries or drones
def table_list(dbname, tname):
    return "SELECT * FROM `{0}`.`{1}`;".format(dbname, tname)

# Select object on given nfcid
def get_by_nfcid(dbname, tname, nfcid):
    return """
    SELECT * FROM `{0}`.`{1}` WHERE (`nfcid` = '{2}');
    """.format(dbname, tname, nfcid)

# Remove object on given nfcid
def rm_by_nfcid(dbname, tname, nfcid):
    return """
    DELETE FROM `{0}`.`{1}` WHERE (`nfcid` = '{2}');
    """.format(dbname, tname, nfcid)

# edit comment
def comment_edit(dbname, tname, nfcid, comment):
    return """
    UPDATE `{0}`.`{1}`
    SET `comment` = '{3}'
    WHERE (`nfcid` = '{2}');
    """.format(dbname, tname, nfcid, comment)

# add battery to charging
def battery_charge(dbname, nfcid):
    return """
    UPDATE `{0}`.`battery`
    SET `n_charge_cycles` = `n_charge_cycles` + 1,
        `last_charge` = '{2}'
    WHERE (`nfcid` = '{1}');
    """.format(dbname, nfcid, datetime.datetime.now())

# when a battery is used (backpack)
def battery_use(dbname, nfcid):
    return """
    UPDATE `{0}`.`battery`
    SET `last_use` = '{2}'
    WHERE (`nfcid` = '{1}');
    """.format(dbname, nfcid, datetime.datetime.now())

# when a drone is used (backpack)
def drone_use(dbname, nfcid):
    return """
    UPDATE `{0}`.`drone`
    SET `last_use` = '{2}',
        `n_use` = `n_use` + 1
    WHERE (`nfcid` = '{1}');
    """.format(dbname, nfcid, datetime.datetime.now())
