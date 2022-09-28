# TAMU-GradeDistribution-ParserV2: gd_utils.py
# @authors: github/adibarra


# imports
import re
import sys
import time
from gd_logger import Logger, Importance
from gd_database import DatabaseHandler
from gd_prefsloader import PreferenceLoader


class Utils:

    """ Class to hold misc. utility methods """

    # all startup tasks go here to declutter the main file
    @staticmethod
    def startup() -> None:
        Logger.log('-----------------------', importance=None)
        if PreferenceLoader.load_prefs():
            Logger.log('Loaded Preferences file.', importance=None)
            Logger.log(f'Starting up at {time.strftime("%Y-%m-%d %H:%M:%S")}', importance=None)
            if DatabaseHandler.check_db_connection():
                Logger.log('Database connection established!', importance=None)
                Logger.log('-----------------------\n', importance=None)
                DatabaseHandler.set_build_percentage(0)
            else:
                Logger.log('>>> Unable to establish database connection <<<', Importance.CRIT)
                Logger.log(' '*27+DatabaseHandler.check_db_connection_error(), importance=None)
                Logger.log('-----------------------\n', importance=None)
                sys.exit(0)
        else:
            Logger.log('Failed to load Preferences file. (See console for details).', importance=None)
            Logger.log('-----------------------\n', importance=None)
            sys.exit(0)

    # all shutdown tasks go here to declutter the main file
    @staticmethod
    def shutdown() -> None:
        DatabaseHandler.set_build_percentage(100)
        Logger.log('\n-----------------------\nGoodbye...\n-----------------------\n\n\n', importance=None)

    # convert parsed list into database format
    @staticmethod
    def convert_to_entries(to_convert: list, year: int, semster: str) -> list:
        converted_list = []
        try:
            for entry in to_convert:
                if len(entry) == 20 and 'TOTAL'.upper() not in str(entry[0]).upper():
                    converted_list += [[year, semster, entry[0].split('-')[0], entry[0].split('-')[1], entry[0].split('-')[2],
                                    int(entry[1]), int(entry[3]), int(entry[5]), int(entry[7]), int(entry[9]), float(entry[12]), int(entry[13]),
                                    int(entry[14]), int(entry[15]), int(entry[16]), int(entry[17]), int(entry[18]), entry[19]]]
        except Exception:
            tmp = [year, semster, entry[0].split("-")[0], entry[0].split("-")[1], entry[0].split("-")[2],
                    entry[1], entry[3], entry[5], entry[7], entry[9], float(entry[12]),
                    entry[13], entry[14], entry[15], entry[16], entry[17], entry[18], entry[19]
                ]
            print(f'BAD ENTRY DURING CONVERSION:\n{entry}\n{tmp}\n')
        return converted_list

    # check if the section number is a honors section
    @staticmethod
    def is_honors(section: str) -> bool:
        reg1 = re.compile('2[0-9]{2,}')
        reg2 = re.compile('58[0-9]{1,}')
        return (len(reg1.findall(section)) > 0 or
                len(reg2.findall(section)) > 0)

    # expands [2017,2021] into [2017,2018,2019,2020,2021]
    @staticmethod
    def interpolate_num_list(num_list: list[int], step_size: int) -> list[int]:
        new_list = [int(num_list[0])]
        while (new_list[len(new_list)-1] < int(num_list[len(num_list)-1])):
            new_list.append(new_list[len(new_list)-1] + step_size)
        return new_list
