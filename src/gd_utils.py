# tamugd-parser: gd_utils.py
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


    @staticmethod
    def startup() -> None:
        """ Startup tasks for the program. """

        Logger.log('-----------------------', importance=None)
        if PreferenceLoader.load_prefs():
            Logger.log('Loaded Preferences file.', importance=None)
            Logger.log(f'Starting up at {time.strftime("%Y-%m-%d %H:%M:%S")}', importance=None)
            if DatabaseHandler.check_db_connection():
                Logger.log('Database connection established!', importance=None)
                Logger.log('-----------------------\n', importance=None)
                print('Check the latest log file to see database build progress')
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


    @staticmethod
    def shutdown() -> None:
        """ Shutdown tasks for the program. """

        DatabaseHandler.set_build_percentage(100)
        Logger.log('\n-----------------------\nGoodbye...\n-----------------------\n\n\n', importance=None)


    @staticmethod
    def convert_to_entries(to_convert: list, year: int, semester: str) -> list:
        """Convert the parsed list into a list of entries for the database.
        Parameters:
            to_convert (list): The list to convert
            year (int): The year of the semester
            semester (str): The semester
        Returns:
            list: The converted list
        """

        converted_list = []
        try:
            for entry in to_convert:
                if len(entry) == 20 and 'TOTAL'.upper() not in str(entry[0]).upper():
                    converted_list += [[year, semester, entry[0].split('-')[0], entry[0].split('-')[1], entry[0].split('-')[2],
                                    int(entry[1]), int(entry[3]), int(entry[5]), int(entry[7]), int(entry[9]), float(entry[12]), int(entry[13]),
                                    int(entry[14]), int(entry[15]), int(entry[16]), int(entry[17]), int(entry[18]), entry[19]]]
        except Exception:
            tmp = [year, semester, entry[0].split("-")[0], entry[0].split("-")[1], entry[0].split("-")[2],
                    entry[1], entry[3], entry[5], entry[7], entry[9], float(entry[12]),
                    entry[13], entry[14], entry[15], entry[16], entry[17], entry[18], entry[19]
                ]
            print(f'BAD ENTRY DURING CONVERSION:\n{entry}\n{tmp}\n')
        return converted_list


    @staticmethod
    def is_honors(section: str) -> bool:
        """Check if the section number is an honors section
        Parameters:
            section (str): The section number to check
        Returns:
            bool: True if the section is an honors section, False otherwise
        """

        reg1 = re.compile('2[0-9]{2,}')
        reg2 = re.compile('58[0-9]{1,}')
        return (len(reg1.findall(section)) > 0 or
                len(reg2.findall(section)) > 0)


    @staticmethod
    def interpolate_num_list(num_list: list[int], step_size: int) -> list[int]:
        """Expands a range of numbers into a list of numbers using a step size.
        Example: [2017,2021] with a step size of 1 would become [2017,2018,2019,2020,2021]
        Parameters:
            num_list (list[int]): The list to expand
            step_size (int): The step size to use
        Returns:
            list[int]: The expanded list
        """

        new_list = [int(num_list[0])]
        while (new_list[len(new_list)-1] < int(num_list[len(num_list)-1])):
            new_list.append(new_list[len(new_list)-1] + step_size)
        return new_list
