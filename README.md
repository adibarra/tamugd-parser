> [!CAUTION]
> **⚠️ This project is now deprecated and is no longer maintained. ⚠️**

# tamugd-parser

This project is dedicated to helping analyze the massive amounts of data released every semester by Texas A&M University's Registrar's office.

---

## Features:
- Parse grade report PDFs published by Texas A&M University's Registrar:
    - Automatically adds parsed course data to a mySQL database.


## Version 2.0 Roadmap:
- [x] <s>Grade report parsing</s>
- [x] <s>Automatically add data to a mySQL database backend</s>
- [x] <s>Full rewrite with multithreading</s>
- [x] <s>Fully automated grade report updates (auto add new reports)</s>


## How to set up:
1. Open MySQL:
    ```bash
    # open sql prompt
    $ sudo mysql
    ```
2. Create mySQL database and user:
    ```sql
    mysql> CREATE DATABASE database_name_here;
    mysql> CREATE USER 'database_user_name_here'@'localhost' IDENTIFIED BY 'database_user_password_here';
    mysql> GRANT ALL PRIVILEGES ON database_name_here.* TO 'database_user_name_here'@'localhost';
    mysql> FLUSH PRIVILEGES;
    mysql> exit;
    ```
3. Install dependencies:
    ```bash
    # automatically install python dependencies
    $ screen -SRD tamugd-parser
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    ```
4. Generate prefs.json and update file:
    ```bash
    # run in tamugd-parser/
    $ python3 src/main.py
    $ nano prefs.json
    ```


## Notes
By default, this tool only processes PDFs that are CURRENTLY available from the Registrar but it supports parsing PDFs from 2012 onwards (perhaps also older ones, but they have not been tested). It will automatically download PDFs as needed. If you have additional PDFs you can supply your own in the `pdfs/` folder however you must use the `-s or --start-year` flag.

Run `python3 src/main.py --help` for more detailed information.


## Examples
```bash
# Process all PDFs from the Registrar
$ python3 src/main.py

# Process PDFs from 2014 to present
$ python3 src/main.py --start-year 2014

# Process PDFs from 2014 to 2018
$ python3 src/main.py --start-year 2014 --end-year 2018
```

---

Once the script is running you can monitor its progress by using the following command:
```bash
# Building the database will take a while...
# Detach screen with CTRL+A then CTRL+D while running the main script
# Then run this to display a live feed from the newest logfile
$ cd logs && tail -f $(ls -t | head -1)
```
