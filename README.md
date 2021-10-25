# TAMU-GradeDistribution-ParserV2

This project is dedicated to helping analyze the massive amounts of data released every semester by Texas A&M University's Registrar's office regarding the courses they offer.

---

## Features:
- Parse grade report PDFs published by Texas A&M University's Registrar:
    - Automatically adds parsed course data to a mySQL database.


## Version 1.0 Roadmap:
- [x] Grade report parsing
- [x] Automatically add data to a mySQL database backend
- [ ] Automated grade report updates


## How to use:
1. Set up mySQL table:
    ```
    # create mySQL database table
    $ sudo mysql
    mysql> use database_name_here;
    mysql> CREATE TABLE tamugrades (
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
    ```
2. Install dependencies:
    ```
    # automatically install python dependencies
    $ python3 -m pip install -r requirements.txt
    ```
3. Generate prefs.json and update file:
    ```
    # run in TAMU-GradeDistribution-ParserV2
    $ python3 src/gd_main.py
    $ nano prefs.json
    ```
4. Run main python script:
    ```
    # NOTE: building the database will take a while
    $ python3 src/gd_main.py
    ```
5. Monitor created logfile (optional):
    ```
    # automatically get and display newest logfile
    $ cd logs
    $ tail -f $(ls -t | head -1)
    ```
