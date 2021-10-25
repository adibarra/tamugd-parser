# TAMU-GradeDistribution-ParserV2: GD_pdfparser.py
# @authors: github/adibarra


# imports
import PyPDF2
from typing import List
from GD_utils import Utils
from GD_logger import Logger, Importance


# parse grade report pdf
def parseGradesPDF(pdfFilePath:str) -> List:
    Logger.log('Started parsing full PDF('+pdfFilePath.split('/')[-1]+')', Importance.INFO)
    try:
        pdfFile = open(pdfFilePath,'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFile)
    except PyPDF2.utils.PdfReadError:
        print('Bad or missing PDF: '+pdfFilePath)
        return []

    tmp = pdfFilePath.split('.')[0].split('grd')[-1]
    year = tmp[:4]
    semester = tmp[4:-2]
    college = tmp[-2:]
    semesterNames = ['SPRING','SUMMER','FALL']

    output_list = []
    for pageNum in range(0,pdfReader.numPages):
        pageObj = pdfReader.getPage(pageNum)
        pageStr = pageObj.extractText().split('\n')
        if 'COLLEGE STATION' in pageStr[36]:
            #print('(OLD 2012+) PDF FORMAT')
            pageStr = [ps.strip() for ps in pageStr[37:]]

            offset = 0
            for i in range(0,len(pageStr)//20):
                k = i*20+offset
                if pageStr[k+0].strip() in ['COURSE TOTAL:','DEPARTMENT TOTAL:','COLLEGE TOTAL:']:
                    offset -= 1
                    continue
                # [year,semester,college,departmentName,course,section,honors,avgGPA,professorName,A,B,C,D,F,I,S,U,Q,X]
                output_list.append([int(year), semesterNames[int(semester)-1], college,
                                    pageStr[k].split('-')[0], pageStr[k].split('-')[1], pageStr[k].split('-')[2], int(Utils.isSectionHonors(pageStr[k].split('-')[2])),
                                    float(pageStr[k+ 1]),     pageStr[k+ 2],  int(pageStr[k+ 4]), int(pageStr[k+ 5]), int(pageStr[k+ 6]), int(pageStr[k+ 7]),
                                        int(pageStr[k+ 8]), int(pageStr[k+10]), int(pageStr[k+11]), int(pageStr[k+12]), int(pageStr[k+13]), int(pageStr[k+14])])
        else:
            #print('(NEW 2017+) PDF FORMAT')
            pageStr = [ps.strip() for ps in pageStr[38:]]

            offset = 0
            for i in range(0,len(pageStr)//20):
                k = i*20+offset
                if pageStr[k+0].strip() in ['COURSE TOTAL:','DEPARTMENT TOTAL:','COLLEGE TOTAL:']:
                    offset -= 1
                    continue
                # [year,semester,college,departmentName,course,section,honors,avgGPA,professorName,A,B,C,D,F,I,S,U,Q,X]
                output_list.append([int(year), semesterNames[int(semester)-1], college,
                                    pageStr[k].split('-')[0], pageStr[k].split('-')[1], pageStr[k].split('-')[2], int(Utils.isSectionHonors(pageStr[k].split('-')[2])),
                                    float(pageStr[k+12]),     pageStr[k+19],  int(pageStr[k+ 3]), int(pageStr[k+ 5]), int(pageStr[k+ 7]), int(pageStr[k+ 9]),
                                        int(pageStr[k+13]), int(pageStr[k+14]), int(pageStr[k+15]), int(pageStr[k+16]), int(pageStr[k+17]), int(pageStr[k+18])])
    return output_list