# NFC DataBase Inventory (nfcdbi)

## Project design
This project aims at identifying objects through NFC tags, and organize
them in a database.
NFC tags already has universal unique id (uuid) garanteed by the constructor.
This uuid will be used to uniquely identify an object in the database.

The database abstraction layer will be first using relational MariaDB backend.

The program will interact with the user through CLI. The CLI will be contextual
(NFC tag, configuration etc...) allowing an easy access (read/write) to the database.


## Python working environment: virtualenv setup
To work on a dedicated python installation, virtualenv is
a good choice. This allows us to construct a custom
environment fitting the needs of the project (modules, packages...).

1. Install python 2.7 virtualenv with the command:
```bash
pip install virtualenv
```

2. Activate the virtual env:
```bash
source py2_nfcdbi/bin/activate
```
You now should see the prompt's line starting with (py2_nfcdbi).
The virtualenv is now active.

3. To exit, simply use:
```bash
deactivate
```

## Use of the CLI

When starting the program, you may type `sudo python main.py` because
of the rights on /dev/usb on your system.

Also, you may start with `sudo python main.py -h` see usage.

To use the `backpack` and `charge` menus, you have 3 seconds
to type "end" + press enter if you want to terminate the list.
I have to find something better. :) You can custom this time
in the `main.py`.

## MYSQL/MARIADB
For sure, a mysql server must be running in background, in the
conventional port 3306. The user, password, db host and db name
can be passed as argument.

The db_name (-n) argument is required to create the battery table
and initialize de db state using the db you created. If the db is
already present, it will only be selected.