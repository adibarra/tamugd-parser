# TAMU-GradeDistribution-ParserV2

This project is dedicated to helping analyze the massive amounts of data released every semester by Texas A&M University's Registrar's office.

---

## Features:
- Parse grade report PDFs published by Texas A&M University's Registrar:
    - Automatically adds parsed course data to a mySQL database.


## Version 2.0 Roadmap:
- [x] <s>Grade report parsing</s>
- [x] <s>Automatically add data to a mySQL database backend</s>
- [x] <s>Full rewrite with multithreading</s>
- [ ] Fully automated grade report updates (auto add new reports)


## How to use:
1. Open MySQL:
    ```bash
    # open sql prompt
    $ sudo mysql
    ```
2. Create mySQL database and user:
    ```sql
    mysql> CREATE DATABASE tamugradesDB;
    mysql> CREATE USER 'database_user_name_here'@'localhost' IDENTIFIED BY 'database_user_password_here';
    mysql> GRANT ALL PRIVILEGES ON tamugradesDB.* TO 'database_user_name_here'@'localhost';
    mysql> FLUSH PRIVILEGES;
    mysql> exit;
    ```
3. Install dependencies:
    ```bash
    # automatically install python dependencies
    $ screen -SRD tamugd-parser
    $ python3 -m venv tamugd-parser-venv
    $ source tamugd-parser-venv/bin/activate
    $ pip install -r requirements.txt
    ```
4. Generate prefs.json and update file:
    ```bash
    # run in TAMU-GradeDistribution-ParserV2
    $ python3 src/gd_main.py
    $ nano prefs.json
    ```
5. Run main python script:
    ```bash
    # NOTE: building the database will take a while (detatch screen with CTRL+A then CTRL+D after running main script)
    $ python3 src/gd_main.py
    ```
6. Monitor created logfile (optional):
    ```bash
    # automatically get and display newest logfile
    $ cd logs
    $ tail -f $(ls -t | head -1)
    ```
