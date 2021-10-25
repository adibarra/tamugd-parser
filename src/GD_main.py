# TAMU-GradeDistribution-ParserV2: GD_main.py
# @authors: github/adibarra


# imports
import sys
import bs4
import requests
from typing import List, Tuple
from alive_progress import alive_bar
from concurrent.futures import ThreadPoolExecutor

from GD_utils import *
from GD_logger import *
from GD_database import *
from GD_pdfparser import *


OVERWRITE_ALL_PDF = False
LEGACY_YEAR_DATA = ['2015','2014']
PDF_ROOT_LINK = 'https://web-as.tamu.edu/gradereport/'
PDF_BASE_LINK = 'https://web-as.tamu.edu/gradereport/PDFReports/{0}/grd{0}{1}.pdf'
PDF_SAVE_DIR  = 'pdfs/'


# scrape years and colleges from grade reports site using bs4
def scrapeReportMetadata() -> Tuple[List[str],List[str]]:
    response = requests.get(PDF_ROOT_LINK)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    years, colleges = [], []
    for option in soup.select("#ctl00_plcMain_lstGradYear > option"):
        years.append(option['value'])
    for option in soup.select("#ctl00_plcMain_lstGradCollege > option"):
        colleges.append(option['value'])
    return years, colleges


# load pdf or download from given url if not present
def loadPDF(downloadURL:str, noDL=False) -> str:
    fileName = downloadURL.split('/')[-1]
    filePath = PDF_SAVE_DIR+fileName
    def downloadPDF():
        Logger.log('Downloading PDF('+fileName+').', Importance.INFO)
        response = requests.get(downloadURL)
        with open(filePath, 'wb+') as f:
            f.write(response.content)
        Logger.log('Finished downloading and saving PDF('+fileName+').', Importance.INFO)
    
    if (noDL):
        Logger.log('[NO DOWNLOAD] PDF('+fileName+') download forcibly skipped.', Importance.INFO)
        return filePath
    
    if (os.path.exists(filePath)):
        if OVERWRITE_ALL_PDF:
            Logger.log('PDF('+fileName+') already exists. Overwriting.', Importance.INFO)
            downloadPDF()
        else:
            Logger.log('PDF('+fileName+') already exists. Skipping download.', Importance.INFO)
    else:
        os.makedirs(''.join(filePath.split('/')[:-1]), exist_ok=True)
        Logger.log('PDF('+fileName+') does not exist. Downloading.', Importance.INFO)
        downloadPDF()
    return filePath


# process given PDFdata
def processPDF(PDFdata) -> None:
    try:
        year, semester, college, bar = PDFdata
        pdflink = PDF_BASE_LINK.format(year+semester, college)
        pdfFilePath = loadPDF(pdflink, noDL=(year in LEGACY_YEAR_DATA))
        grades_list = parseGradesPDF(pdfFilePath)
        DatabaseHandler.addGradeEntries('tamugrades', grades_list)
    except:
        Logger.log('Unable to parse PDF('+pdfFilePath.split('/')[-1]+')', Importance.WARN)
    finally:
        bar(1)


# main
def main() -> None:
    # complete startup tasks
    Utils.startup(PreferenceLoader)
    print('Check the latest log file to see database build progress')

    with alive_bar(title='Scraping metadata'):
        semesters = ['1','2','3']
        years, colleges = scrapeReportMetadata()
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
        PDFdata = []
        for year in years[::-1]:
            for semester in semesters:
                for college in colleges:
                    PDFdata.append([year,semester,college,bar])

        # automatically load pdfs from pdfs list
        try:
            with ThreadPoolExecutor() as executor:
                executor.map(processPDF, PDFdata)
        except KeyboardInterrupt:
            Logger.log('KeyboardInterrupt recieved: Exiting', importance=None)
            Utils.shutdown()
            sys.exit(1)
        else:
            Utils.shutdown()


if __name__ == "__main__":
    main()