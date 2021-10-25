# TAMU-GradeDistribution-ParserV2: GD_main.py
# @authors: github/adibarra


# imports
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple

import os
import sys
import bs4
import requests
from alive_progress import alive_bar
from gd_utils import Utils
from gd_logger import Logger, Importance
from gd_database import DatabaseHandler
from gd_pdfparser import PDFParser


OVERWRITE_ALL_PDF = False
LEGACY_YEAR_DATA = ['2015','2014']
PDF_ROOT_LINK = 'https://web-as.tamu.edu/gradereport/'
PDF_BASE_LINK = 'https://web-as.tamu.edu/gradereport/PDFReports/{0}/grd{0}{1}.pdf'
PDF_SAVE_DIR  = 'pdfs/'


# scrape years and colleges from grade reports site using bs4
def scrape_report_metadata() -> Tuple[List[str],List[str]]:
    response = requests.get(PDF_ROOT_LINK)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    years, colleges = [], []
    for option in soup.select("#ctl00_plcMain_lstGradYear > option"):
        years.append(option['value'])
    for option in soup.select("#ctl00_plcMain_lstGradCollege > option"):
        colleges.append(option['value'])
    return years, colleges


# load pdf or download from given url if not present
def load_pdf(download_url:str, no_dl=False) -> str:
    file_name = download_url.split('/')[-1]
    file_path = PDF_SAVE_DIR+file_name
    def download_pdf():
        Logger.log('Downloading PDF('+file_name+').', Importance.INFO)
        response = requests.get(download_url)
        with open(file_path, 'wb+') as file:
            file.write(response.content)
        Logger.log('Finished downloading and saving PDF('+file_name+').', Importance.INFO)

    if no_dl:
        Logger.log('[NO DOWNLOAD] PDF('+file_name+') download forcibly skipped.', Importance.INFO)
        return file_path

    if os.path.exists(file_path):
        if OVERWRITE_ALL_PDF:
            Logger.log('PDF('+file_name+') already exists. Overwriting.', Importance.INFO)
            download_pdf()
        else:
            Logger.log('PDF('+file_name+') already exists. Skipping download.', Importance.INFO)
    else:
        os.makedirs(''.join(file_path.split('/')[:-1]), exist_ok=True)
        Logger.log('PDF('+file_name+') does not exist. Downloading.', Importance.INFO)
        download_pdf()
    return file_path


# process given PDFdata
def process_pdf(pdf_data) -> None:
    try:
        year, semester, college, bar = pdf_data
        pdflink = PDF_BASE_LINK.format(year+semester, college)
        pdf_file_path = load_pdf(pdflink, no_dl=(year in LEGACY_YEAR_DATA))
        grades_list = PDFParser.parse_grades_pdf(pdf_file_path)
        DatabaseHandler.add_grade_entries('tamugrades', grades_list)
    except Exception:
        Logger.log('Unable to parse PDF('+pdf_file_path.split('/')[-1]+')', Importance.WARN)
    finally:
        bar(1)


# main
def main() -> None:
    # complete startup tasks
    Utils.startup()
    print('Check the latest log file to see database build progress')

    with alive_bar(title='Scraping metadata'):
        semesters = ['1','2','3']
        years, colleges = scrape_report_metadata()
        years = years+LEGACY_YEAR_DATA
        blacklist = ['AE','AP','GV','QT','UT','DN_PROF','SL_PROF','MD_PROF','CP_PROF','VM_PROF']
        colleges = list(set(colleges) - set(blacklist))
        # AE=Academic Success Center
        # AP=Association Provost For UG Studies
        # GV=TAMU-Galveston
        # QT=TAMU-Qatar
        # UT=University Totals
        # PROF=Professional, format not yet supported

    with alive_bar(total=len(years)*len(semesters)*len(colleges),title='Building database') as bar:
        # generate pdf urls
        pdf_data = []
        for year in years[::-1]:
            for semester in semesters:
                for college in colleges:
                    pdf_data.append([year,semester,college,bar])

        # automatically load pdfs from pdfs list
        try:
            with ThreadPoolExecutor() as executor:
                executor.map(process_pdf, pdf_data)
        except KeyboardInterrupt:
            Logger.log('KeyboardInterrupt recieved: Exiting', importance=None)
            Utils.shutdown()
            sys.exit(1)
        else:
            Utils.shutdown()


if __name__ == "__main__":
    main()
