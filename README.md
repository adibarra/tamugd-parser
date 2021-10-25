# TAMU-GradeDistribution-Parser

This project is dedicated to helping analyze the massive amounts of data released yearly by the TAMU registrar's office regarding the courses they offer.

---

## Dependencies:
```
$ python3 -m pip install PyPDF2
$ python3 -m pip install pymysql
$ python3 -m pip install beautifulsoup4
```


## Features:
- Parse grade report PDFs published by Texas A&M University's Registrar:
    - Automatically adds parsed course data to SQL database.


## Version 1.0 Roadmap:
- [x] Grade report parsing
- [x] Automatically add data to a SQL backend
- [ ] Automated grade report updates


## How to use:
1. Install dependencies:
    ```
    # automatically install python dependencies
    $ python3 -m pip install -r requirements.txt
    ```
2. Generate prefs.json file:
    ```
    $ cd TAMU-GradeDistribution-Parser
    $ python3 src/GD_main.py
    ```
3. Update contents of prefs.json file:
    ```
    $ nano prefs.json
    ```
4. Run main python script:
    ```
    # NOTE: building the database will take a while
    $ cd TAMU-GradeDistribution-Parser
    $ python3 src/GD_main.py
    ```
5. Monitor created logfile (optional):
    ```
    # automatically get and display newest logfile
    $ tail -f $(ls -t | head -1)
    ```