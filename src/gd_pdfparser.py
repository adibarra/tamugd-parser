# TAMU-GradeDistribution-ParserV2: gd_pdfparser.py
# @authors: github/adibarra


# imports
from typing import List

import PyPDF2
from gd_utils import Utils
from gd_logger import Logger, Importance


class PDFParser:
    """ Class to parse PDF files """

    # parse grade report pdf
    @staticmethod
    def parse_grades_pdf(pdf_file_path:str) -> List:
        Logger.log('Started parsing full PDF('+pdf_file_path.split('/')[-1]+')', Importance.INFO)
        try:
            with open(pdf_file_path,'rb',encoding='utf8') as pdf_file:
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        except PyPDF2.utils.PdfReadError:
            print('Bad or missing PDF: '+pdf_file_path)
            return []

        tmp = pdf_file_path.split('.')[0].split('grd')[-1]
        year = tmp[:4]
        semester = tmp[4:-2]
        college = tmp[-2:]
        semester_names = ['SPRING','SUMMER','FALL']

        output_list = []
        for page_num in range(0,pdf_reader.numPages):
            page_obj = pdf_reader.getPage(page_num)
            page_str = page_obj.extractText().split('\n')
            if 'COLLEGE STATION' in page_str[36]:
                #print('(OLD 2012+) PDF FORMAT')
                page_str = [ps.strip() for ps in page_str[37:]]

                offset = 0
                for i in range(0,len(page_str)//20):
                    k = i*20+offset
                    if page_str[k+0].strip() in ['COURSE TOTAL:','DEPARTMENT TOTAL:','COLLEGE TOTAL:']:
                        offset -= 1
                        continue
                    # [year,semester,college,departmentName,course,section,honors,avgGPA,professorName,A,B,C,D,F,I,S,U,Q,X]
                    output_list.append([int(year), semester_names[int(semester)-1], college,
                                        page_str[k].split('-')[0], page_str[k].split('-')[1], page_str[k].split('-')[2], int(Utils.is_honors(page_str[k].split('-')[2])),
                                        float(page_str[k+ 1]),     page_str[k+ 2],  int(page_str[k+ 4]), int(page_str[k+ 5]), int(page_str[k+ 6]), int(page_str[k+ 7]),
                                            int(page_str[k+ 8]), int(page_str[k+10]), int(page_str[k+11]), int(page_str[k+12]), int(page_str[k+13]), int(page_str[k+14])])
            else:
                #print('(NEW 2017+) PDF FORMAT')
                page_str = [ps.strip() for ps in page_str[38:]]

                offset = 0
                for i in range(0,len(page_str)//20):
                    k = i*20+offset
                    if page_str[k+0].strip() in ['COURSE TOTAL:','DEPARTMENT TOTAL:','COLLEGE TOTAL:']:
                        offset -= 1
                        continue
                    # [year,semester,college,departmentName,course,section,honors,avgGPA,professorName,A,B,C,D,F,I,S,U,Q,X]
                    output_list.append([int(year), semester_names[int(semester)-1], college,
                                        page_str[k].split('-')[0], page_str[k].split('-')[1], page_str[k].split('-')[2], int(Utils.is_honors(page_str[k].split('-')[2])),
                                        float(page_str[k+12]),     page_str[k+19],  int(page_str[k+ 3]), int(page_str[k+ 5]), int(page_str[k+ 7]), int(page_str[k+ 9]),
                                            int(page_str[k+13]), int(page_str[k+14]), int(page_str[k+15]), int(page_str[k+16]), int(page_str[k+17]), int(page_str[k+18])])
        return output_list
