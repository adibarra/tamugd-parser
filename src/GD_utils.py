# TAMU-GradeDistribution-ParserV2: GD_utils.py
# @authors: github/adibarra


# imports
import re
import sys
import time
from typing import List
from GD_logger import Logger, Importance
from GD_database import DatabaseHandler


class Utils:

    """ Class to hold misc. utility methods """

    # all startup tasks go here to declutter the main file
    @staticmethod
    def startup(PreferenceLoader) -> None:
        Logger.log('-----------------------', importance=None)
        if PreferenceLoader.loadPrefs():
            Logger.log('Loaded Preferences file.', importance=None)
            Logger.log('Starting up at '+time.strftime("%Y-%m-%d %H:%M:%S"), importance=None)
            if DatabaseHandler.checkDBConnection():
                Logger.log('Database connection established!', importance=None)
            else:
                Logger.log('>>> Unable to establish database connection <<<', Importance.CRIT)
                Logger.log('                           '+DatabaseHandler.checkDBConnectionError(), importance=None)
            Logger.log('-----------------------\n', importance=None)
        else:
            Logger.log('Failed to load Preferences file. (See console for details).', importance=None)
            Logger.log('-----------------------\n', importance=None)
            sys.exit(0)
    

    # all shutdown tasks go here to declutter the main file
    @staticmethod
    def shutdown() -> None:
        Logger.log('\n-----------------------\nGoodbye...\n-----------------------\n\n\n', importance=None)


    # convert parsed list into database format
    @staticmethod
    def convertToEntries(toConvert:list, year:int, semster:str) -> List:
        convertedList = []
        try:
            for entry in toConvert:
                if len(entry) == 20 and 'TOTAL'.upper() not in str(entry[0]).upper():
                    convertedList += [[year, semster, entry[0].split('-')[0], entry[0].split('-')[1], entry[0].split('-')[2], int(entry[1]), int(entry[3]), int(entry[5]), 
                                       int(entry[7]), int(entry[9]), float(entry[12]), int(entry[13]), int(entry[14]), int(entry[15]), int(entry[16]), int(entry[17]), int(entry[18]), entry[19]]]
        except:
            print('BAD ENTRY DURING CONVERSION:\n'+str(entry)+'\n'+str([year, semster, entry[0].split('-')[0], entry[0].split('-')[1], entry[0].split('-')[2], entry[1], entry[3], entry[5], 
                entry[7], entry[9], float(entry[12]), entry[13], entry[14], entry[15], entry[16], entry[17], entry[18], entry[19]])+'\n')
        return convertedList
    

    # convert parsed list into database format
    @staticmethod
    def isSectionHonors(section:str) -> bool:
        h1 = re.compile('2[0-9]{2,}')
        h2 = re.compile('58[0-9]{1,}')
        return len(h1.findall(section)) > 0 or len(h2.findall(section)) > 0