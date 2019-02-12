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
