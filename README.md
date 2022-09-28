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


## How to set up:
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

## Legacy PDFs:
A legacy PDF is a PDF which you have already downloaded. This is useful if you want to add data from a PDF which is not currently available on the Registrar's website.

## How to run:
### If you DO NOT have legacy pdfs
1. Run main python script:
    ```bash
    # NOTE: Building the database will take a while...
    #       Detach screen with CTRL+A then CTRL+D after running main script.
    $ python3 src/gd_main.py
    ```

### If you DO have legacy pdfs
1. Run main python script:
    ```bash
    # NOTE: Building the database will take a while...
    #       Detach screen with CTRL+A then CTRL+D after running main script.

    # display help menu
    $ python3 src/gd_main.py --help
    # try adding legacy pdfs from 2014 to most recent downloadable pdf
    $ python3 src/gd_main.py --start-year-legacy 2014
    ```

---

Once the script is running you can monitor its progress by using the following command:
```bash
# automatically get and display a live feed from the newest logfile
$ cd logs && tail -f $(ls -t | head -1)
```
