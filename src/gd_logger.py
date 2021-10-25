# TAMU-GradeDistribution-ParserV2: gd_logger.py
# @authors: github/adibarra


# imports
import os
import time
import glob
import enum
import zipfile
import traceback
from zipfile import ZipFile
from gd_prefsloader import PreferenceLoader


class Importance(enum.IntEnum):
    """ Enum to keep track of logger message importance """
    CRIT = 0
    WARN = 1
    INFO = 2
    DBUG = 3


class Logger:
    """ Class to handle logging """
    MAX_LOGFILE_SIZE = 1e+6  # 1 MB

    # log message to logfile
    @staticmethod
    def log(message: str, importance: Importance):
        if not PreferenceLoader.logger_enabled:
            return
        # if logs folder does not exist then create it
        try:
            if not os.path.exists(os.path.dirname(os.path.realpath(__file__))+'/../logs'):
                original_umask = os.umask(0)
                os.makedirs(os.path.dirname(os.path.realpath(__file__))+'/../logs')
                os.umask(original_umask)
        except Exception as ex:
            print('There was an error while trying to create the logs directory:')
            print(ex)

        # if logfile for today does not exist then create it
        file_path = os.path.dirname(os.path.realpath(__file__))+'/../logs/'+time.strftime('log-%Y-%m-%d')+'.log'
        if not os.path.isfile(file_path):
            try:
                with open(file_path,'a') as log_file:
                    pass
            except Exception as ex:
                print('There was an error while trying to create the logfile:')
                print(ex)

        # write message to the logfile
        try:
            with open(file_path,'a') as log_file:
                if importance is None:
                    log_file.write(message+'\n')
                else:
                    log_file.write(time.strftime('%Y-%m-%d %H:%M:%S')+' ['+importance.name+'] '+message+'\n')

            # if logfile goes over MAX_LOGFILE_SIZE, rename current logfile and later autocreate another
            if os.stat(file_path).st_size > Logger.MAX_LOGFILE_SIZE:
                log_number = 0
                # iterate through logs for the day and find largest logfile number
                for name in glob.glob(file_path[:len(file_path)-4]+'*'):
                    if len(name.split('/')[-1].split('.')) > 2:
                        num = int(name.split('/')[-1].split('.')[1])
                        if num > log_number:
                            log_number = num

                # rename current log to largest log number +1 then zip and delete original
                file_name = (file_path[:len(file_path)-4]+'.'+str(log_number+1)+'.log').split('/')[-1]
                os.rename(file_path, file_path[:len(file_path)-4]+'.'+str(log_number+1)+'.log')
                with ZipFile(file_path[:len(file_path)-4]+'.'+str(log_number+1)+'.log.zip', 'w', zipfile.ZIP_BZIP2) as zip_file:
                    zip_file.write(file_path[:len(file_path)-4]+'.'+str(log_number+1)+'.log', file_name)
                os.remove(file_path[:len(file_path)-4]+'.'+str(log_number+1)+'.log')

        except Exception:
            print('There was an error when reading or writing a file:')
            print(traceback.format_exc())
