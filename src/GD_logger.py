# TAMU-GradeDistribution-ParserV2: GD_logger.py
# @authors: github/adibarra


# imports
import os
import time
import glob
import enum
import zipfile
import traceback
from zipfile import ZipFile
from GD_prefsloader import PreferenceLoader


class Importance(enum.IntEnum):
    """ Enum to keep track of logger message importance """
    CRIT = 0
    WARN = 1
    INFO = 2
    DBUG = 3
    

class Logger:
    """ Class to handle logging """
    MAX_LOGFILE_SIZE = 1e+6 # 1 MB
    transaction_cache = []

    # log message to logfile
    def log(message: str, importance: Importance):
        if not PreferenceLoader.logger_enabled:
            return
        else:
            # if logs folder does not exist then create it
            try:
                if not os.path.exists(os.path.dirname(os.path.realpath(__file__))+'/../logs'):
                    original_umask = os.umask(0)
                    os.makedirs(os.path.dirname(os.path.realpath(__file__))+'/../logs')
                    os.umask(original_umask)
            except Exception as e:
                print('There was an error while trying to create the logs directory:')
                print(e)

            # if logfile for today does not exist then create it
            filePath = os.path.dirname(os.path.realpath(__file__))+'/../logs/'+time.strftime('log-%Y-%m-%d')+'.log'
            if not os.path.isfile(filePath):
                try:
                    open(filePath, 'a').close()
                except Exception as e:
                    print('There was an error while trying to create the logfile:')
                    print(e)

            # write message to the logfile
            try:
                with open(filePath, 'a') as (logFile):
                    if importance == None:
                        logFile.write(message+'\n')
                    else:
                        logFile.write(time.strftime('%Y-%m-%d %H:%M:%S')+' ['+importance.name+'] '+message+'\n')

                # if logfile goes over MAX_LOGFILE_SIZE, rename current logfile and later autocreate another
                if os.stat(filePath).st_size > Logger.MAX_LOGFILE_SIZE:
                    log_number = 0
                    # iterate through logs for the day and find largest logfile number
                    for name in glob.glob(filePath[:len(filePath)-4]+'*'):
                        if len(name.split('/')[-1].split('.')) > 2:
                            num = int(name.split('/')[-1].split('.')[1])
                            if num > log_number:
                                log_number = num

                    # rename current log to largest log number +1 then zip and delete original
                    fileName = (filePath[:len(filePath)-4]+'.'+str(log_number+1)+'.log').split('/')[-1]
                    os.rename(filePath, filePath[:len(filePath)-4]+'.'+str(log_number+1)+'.log')
                    with ZipFile(filePath[:len(filePath)-4]+'.'+str(log_number+1)+'.log.zip', 'w', zipfile.ZIP_BZIP2) as zip:
                        zip.write(filePath[:len(filePath)-4]+'.'+str(log_number+1)+'.log', fileName)
                    os.remove(filePath[:len(filePath)-4]+'.'+str(log_number+1)+'.log')

            except Exception as e:
                print('There was an error when reading or writing a file:')
                print(traceback.format_exc())
