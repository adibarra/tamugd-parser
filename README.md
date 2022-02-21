# TAMU-GradeDistribution-ParserV2

This project is dedicated to helping analyze the massive amounts of data released every semester by Texas A&M University's Registrar's office.

---

## Features:
- Parse grade report PDFs published by Texas A&M University's Registrar:
    - Automatically adds parsed course data to a mySQL database.


## Version 2.0 Roadmap:
- [x] Grade report parsing
- [x] Automatically add data to a mySQL database backend
- [x] Full rewrite with multithreading
- [ ] Fully automated grade report updates (auto add new reports)


## How to use:
1. Set up mySQL database and table:
    ```
    $ sudo mysql
    mysql> CREATE DATABASE database_name_here;
    mysql> USE database_name_here;
    mysql> CREATE TABLE database_table_name_here (
               year SMALLINT(4),
               semester VARCHAR(6),
               college VARCHAR(7),
               departmentName VARCHAR(5),
               course VARCHAR(4),
               section VARCHAR(3),
               honors TINYINT(1),
               avgGPA FLOAT(4,3),
               professorName VARCHAR(30),
               numA SMALLINT(3),
               numB SMALLINT(3),
               numC SMALLINT(3),
               numD SMALLINT(3),
               numF SMALLINT(3),
               numI SMALLINT(3),
               numS SMALLINT(3),
               numU SMALLINT(3),
               numQ SMALLINT(3),
               numX SMALLINT(3)
           );
    mysql> exit;
    ```
2. Create database user and grant permissions:
    ```
    $ sudo mysql
    mysql> CREATE USER 'database_user_name_here'@'localhost' IDENTIFIED BY 'database_user_password_here';
    mysql> GRANT ALL PRIVILEGES ON database_name_here.* TO 'database_user_name_here'@'localhost';
    mysql> FLUSH PRIVILEGES;
    mysql> exit;
    ```
3. Create virtual environment and install python dependencies:
    ```
    $ screen -SRD tamugd-parser
    $ python3 -m venv tamugd-parser-venv
    $ source tamugd-parser-venv/bin/activate
    $ pip install -r requirements.txt
    ```
4. Generate prefs.json and update file contents:
    ```
    $ python3 src/gd_main.py
    $ nano prefs.json
    ```
5. Run main python script:
    ```
    # NOTE: building the database will take a while (detatch screen with CTRL+A,D after running main script to run in background)
    $ python3 src/gd_main.py
    ```
6. Monitor created logfile (optional):
    ```
    # automatically find and display newest logfile
    $ cd logs
    $ tail -f $(ls -t | head -1)
    ```
