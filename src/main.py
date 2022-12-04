# tamugd-parser: main.py
# @authors: github/adibarra


# imports
import os
import sys
import argparse
from typing import Optional, Tuple
import itertools
import requests

import bs4
from alive_progress import alive_bar
from gd_utils import Utils
from gd_logger import Logger, Importance
from gd_database import DatabaseHandler
from gd_pdfparser import PDFParser
from gd_prefsloader import PreferenceLoader


PDF_ROOT_LINK = 'https://web-as.tamu.edu/GradeReports/'
PDF_BASE_LINK = 'https://web-as.tamu.edu/GradeReports/PDFReports/{0}/grd{0}{1}.pdf'
PDF_SAVE_DIR  = 'pdfs/'


# scrape years and colleges from grade reports site using bs4
def scrape_report_metadata() -> Tuple[list[int],list[str]]:
    soup = bs4.BeautifulSoup(requests.get(PDF_ROOT_LINK,timeout=1000).text, 'html.parser')
    years, colleges = [], []
    for option in soup.select("#ctl00_plcMain_lstGradYear > option"):
        years.append(int(option['value']))
    for option in soup.select("#ctl00_plcMain_lstGradCollege > option"):
        colleges.append(option['value'])
    return years, colleges


# load pdf or attempt to download if not present
def load_pdf(year: str, semester: str, college: str) -> str:
    download_url = PDF_BASE_LINK.format(year+semester, college)
    file_name = download_url.split('/')[-1]
    file_path = PDF_SAVE_DIR+file_name

    if os.path.exists(file_path):
        Logger.log(f'PDF({file_name}) already exists. Skipping download.', Importance.INFO)
    else:
        os.makedirs(''.join(file_path.split('/')[:-1]), exist_ok=True)
        Logger.log(f'PDF({file_name}) does not exist. Downloading.', Importance.INFO)
        with open(file_path,'wb+') as file:
            file.write(requests.get(download_url,timeout=1000).content)
        Logger.log(f'Finished downloading and saving PDF({file_name}).', Importance.INFO)
    return file_path


# process given pdf data
def process_pdf(year: str, semester: str, college: str) -> None:
    try:
        pdf_file_path = load_pdf(year, semester, college)
        DatabaseHandler.add_grade_entries('grades', PDFParser.parse_grades_pdf(pdf_file_path))
    except Exception:
        pdf_name = pdf_file_path.split('/')[-1]
        Logger.log(f'Unable to parse PDF({pdf_name})', Importance.WARN)


# main
def main(start_year: Optional[str], end_year: Optional[str]) -> None:
    Utils.startup()
    # set up database
    DatabaseHandler.send_query(
        f'CREATE TABLE IF NOT EXISTS {PreferenceLoader.db_grades_table} ('
        +'year SMALLINT(4),'
        +'semester VARCHAR(6),'
        +'college VARCHAR(7),'
        +'departmentName VARCHAR(5),'
        +'course VARCHAR(4),'
        +'section VARCHAR(3),'
        +'honors TINYINT(1),'
        +'avgGPA FLOAT(4,3),'
        +'professorName VARCHAR(30),'
        +'numA SMALLINT(3),'
        +'numB SMALLINT(3),'
        +'numC SMALLINT(3),'
        +'numD SMALLINT(3),'
        +'numF SMALLINT(3),'
        +'numI SMALLINT(3),'
        +'numS SMALLINT(3),'
        +'numU SMALLINT(3),'
        +'numQ SMALLINT(3),'
        +'numX SMALLINT(3)'
        +');')
    DatabaseHandler.send_query(
        f'CREATE TABLE IF NOT EXISTS {PreferenceLoader.db_status_table} ('
        +'item VARCHAR(10),'
        +'value SMALLINT(3)'
        +');')
    DatabaseHandler.send_query(f'TRUNCATE TABLE {PreferenceLoader.db_grades_table};')
    DatabaseHandler.send_query(f'TRUNCATE TABLE {PreferenceLoader.db_status_table};')

    # prepare to process data
    with alive_bar(total=1,title='Scraping metadata') as progress_bar:
        semesters = ['3','2','1']
        years, colleges = scrape_report_metadata()

        # process cmd year args
        if start_year is not None:
            years += Utils.interpolate_num_list([int(start_year), int(years[-1]-1)], 1)
        years.sort()
        start_year = years[0] if start_year is None else int(start_year)
        end_year = years[-1] if end_year is None else int(end_year)
        years = years[years.index(start_year):years.index(end_year)+1]

        print('Processing data for: ', years)
        blacklist = ['AE','AP','GV','QT','UT','DN_PROF','SL_PROF','MD_PROF','CP_PROF','VM_PROF']
        colleges = list(set(colleges) - set(blacklist))
        # AE=Academic Success Center
        # AP=Association Provost For UG Studies
        # GV=TAMU-Galveston
        # QT=TAMU-Qatar
        # UT=University Totals
        # PROF=Professional, format not yet supported
        progress_bar(1.0) # pylint: disable=not-callable

    num_pdfs = len(years)*len(semesters)*len(colleges)
    with alive_bar(total=num_pdfs,dual_line=True,title='Building database') as progress_bar:
        # automatically load pdfs from pdfs list
        try:
            sem = ['SPRING','SUMMER','FALL']
            for year, semester, college in list(itertools.product(years,semesters,colleges)):
                progress_bar.text = f'  -> Processing: {year} {sem[int(semester)-1]} {college}'
                process_pdf(str(year), semester, college)
                progress_bar() # pylint: disable=not-callable
                DatabaseHandler.set_build_percentage(round(progress_bar.current()/num_pdfs*100))
        except KeyboardInterrupt:
            Logger.log('KeyboardInterrupt recieved: Exiting', importance=None)
            Utils.shutdown()
            sys.exit(1)
        else:
            Utils.shutdown()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape and parse TAMU Registrar\'s grade report PDFs and load them into a SQL database.')
    parser.add_argument('-s', '--start-year', type=int, default=None, dest='sy',
        help='the integer year of your first pdf. '
        +'The default value is the year of the oldest pdf from the registrar\'s website.')
    parser.add_argument('-e', '--end-year', type=int, default=None, dest='ey',
        help='the integer year of your last pdf. '
        +'The default value is the year of the latest pdf from the registrar\'s website.')
    args = parser.parse_args()

    main(args.sy, args.ey)
