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
1. Install dependencies:
    ```
    # automatically install python dependencies
    $ python3 -m pip install -r requirements.txt
    ```
2. Generate prefs.json file:
    ```
    $ cd TAMU-GradeDistribution-ParserV2
    $ python3 src/GD_main.py
    ```
3. Update contents of prefs.json file:
    ```
    $ nano prefs.json
    ```
4. Run main python script:
    ```
    # NOTE: building the database will take a while
    $ cd TAMU-GradeDistribution-ParserV2
    $ python3 src/GD_main.py
    ```
5. Monitor created logfile (optional):
    ```
    # automatically get and display newest logfile
    $ tail -f $(ls -t | head -1)
    ```
