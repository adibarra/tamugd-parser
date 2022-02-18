# TAMU-GradeDistribution-ParserV2: gd_database.py
# @authors: github/adibarra


# imports
import math
import pymysql
from gd_logger import Logger, Importance
from gd_prefsloader import PreferenceLoader


class DatabaseHandler:
    """ This is a class to handle database queries """

    @staticmethod
    def check_db_connection():
        """Checks connection to database.
        Returns:
            bool: True if connection successful, else False
        """

        return DatabaseHandler.check_db_connection_error() == 'No Error'

    @staticmethod
    def check_db_connection_error():
        """Checks database connection error.
        Returns:
            str: String representing error, None otherwise
        """

        try:
            database = pymysql.connect(host=PreferenceLoader.db_address, user=PreferenceLoader.db_user,
                                       password=PreferenceLoader.db_pass, database=PreferenceLoader.db_name, autocommit=True)
            cursor = database.cursor()
            cursor.execute('show tables;')
            cursor.fetchall()
            database.close()
        except Exception as ex:
            return str(ex.args[0])+': '+str(ex.args[1])
        return 'No Error'

    @staticmethod
    def send_query(message: str):
        """Send a querty to the database server.
        Parameters:
            message (str): The command to send to the MySQL database
        Returns:
            tuple: Will return tuple of tuples containing the result if no error was encountered
            str: Will return a string if an error was encountered
        """

        try:
            database = pymysql.connect(host=PreferenceLoader.db_address, user=PreferenceLoader.db_user,
                                       password=PreferenceLoader.db_pass, database=PreferenceLoader.db_name, autocommit=True)
            cursor = database.cursor()
            # Logger.log('>>> Executing DB Query: '+message, Importance.DBUG)
            cursor.execute(message)
            results = cursor.fetchall()
            database.close()
        except Exception as ex:
            Logger.log('>>> Error Executing DB Query: ERROR '+str(ex), Importance.CRIT)
            return 'ERROR '+str(ex)
        return results


    @staticmethod
    def add_grade_entries(table_name: str, entry_list: list):
        """Adds a list or single grade report entery to the database
        Parameters:
            table_name (str): Name of the table to check for
            entry_list (list): List to add to DB as a record
        Returns:
            tuple: Will return tuple of tuples containing the result if no error was encountered
            str: Will return a string if an error was encountered
        """

        def split_to_string(entry: list):
            # [year,semester,college,departmentName,course,section,honors,avgGPA,professorName,A,B,C,D,F,I,S,U,Q,X]
            return ('('+str(entry[ 0])+',"'+str(entry[ 1])+'","'+str(entry[ 2])+'","'+str(entry[ 3])+'","'+str(entry[ 4])+'","'+str(entry[ 5])+'",'+str(entry[ 6])+','
                       +str(entry[ 7])+',"'+str(entry[ 8])+'",' +str(entry[ 9])+ ',' +str(entry[10])+ ',' +str(entry[11])+ ',' +str(entry[12])+ ','+str(entry[13])+','
                       +str(entry[14])+',' +str(entry[15])+ ',' +str(entry[16])+ ',' +str(entry[17])+ ',' +str(entry[18])+ ')')

        try:
            Logger.log('Started adding new records to database', Importance.INFO)
            if isinstance(entry_list,list) and len(entry_list) > 0 and not isinstance(entry_list[0],list):
                # Logger.log('Adding new entry to '+table_name, Importance.DBUG)
                results = DatabaseHandler.send_query('INSERT INTO '+table_name+' '
                    +'(year,semester,college,departmentName,course,section,honors,avgGPA,professorName,numA,numB,numC,numD,numF,numI,numS,numU,numQ,numX) VALUES '
                    +split_to_string(entry_list)+';')

            elif isinstance(entry_list,list) and len(entry_list) > 0 and isinstance(entry_list[0],list):
                to_add = ''
                results = []
                rows_added = 0
                batch_size = 50

                for entry in entry_list:
                    to_add += split_to_string(entry)+'@'

                to_add = to_add[:-1]
                # Logger.log('Adding new entries to '+tableName, Importance.DBUG)

                # add batchSize at a time until out of records then the remainder
                to_add_split = to_add.split('@')
                if len(to_add_split) > batch_size+1:
                    tmp_batch_size = batch_size
                else:
                    tmp_batch_size = len(to_add_split)

                savelen = math.ceil(len(to_add_split)/tmp_batch_size)
                for _ in range(0, savelen):
                    if len(to_add_split) > batch_size+1:
                        tmp_batch_size = batch_size
                    else:
                        tmp_batch_size = len(to_add_split)

                    combined = ''
                    rows_added += tmp_batch_size
                    for k in range(0, tmp_batch_size):
                        combined += to_add_split[k]+','

                    if combined[:-1] != '':
                        results += DatabaseHandler.send_query('INSERT INTO '+table_name+' '
                            +'(year,semester,college,departmentName,course,section,honors,avgGPA,professorName,numA,numB,numC,numD,numF,numI,numS,numU,numQ,numX) VALUES '+combined[:-1]+';')
                    else:
                        rows_added -= 1

                    to_add_split = to_add_split[tmp_batch_size:]

            elif len(entry_list) == 0:
                return ()
        except Exception as ex:
            print('>>> Error Executing DB Query: ERROR '+str(ex))
            Logger.log('>>> Error Executing DB Query: ERROR '+str(ex), Importance.WARN)
            return 'ERROR '+str(ex)
        Logger.log('Finished adding new records('+str(rows_added)+') to database', Importance.INFO)
        return results
