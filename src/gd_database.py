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
            return f'{ex.args[0]}: {ex.args[1]}'
        return 'No Error'


    @staticmethod
    def send_query(message: str):
        """Send a query to the database server.
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
            # Logger.log(f'>>> Executing DB Query: {message}', Importance.DBUG)
            cursor.execute(message)
            results = cursor.fetchall()
            database.close()
        except Exception as ex:
            Logger.log(f'>>> Error Executing DB Query: ERROR {ex}', Importance.CRIT)
            return f'ERROR {ex}'
        return results


    @staticmethod
    def set_build_percentage(build_percentage: int):
        """Set the build percentage for the database.
        Parameters:
            build_percentage (int): Integer representing the build percentage
        Returns:
            tuple: Will return tuple of tuples containing the result if no error was encountered
            str: Will return a string if an error was encountered
        """

        try:
            database = pymysql.connect(host=PreferenceLoader.db_address, user=PreferenceLoader.db_user,
                                       password=PreferenceLoader.db_pass, database=PreferenceLoader.db_name, autocommit=True)
            cursor = database.cursor()
            # Logger.log(f'>>> Executing DB Query: {message}', Importance.DBUG)
            cursor.execute(f'TRUNCATE TABLE {PreferenceLoader.db_status_table};')
            cursor.execute(f'INSERT INTO {PreferenceLoader.db_status_table} (item,value) values ("BUILD_PERC",{build_percentage});')
            results = cursor.fetchall()
            database.close()
        except Exception as ex:
            Logger.log(f'>>> Error Executing DB Query: ERROR {ex}', Importance.CRIT)
            return f'ERROR {ex}'
        return results


    @staticmethod
    def add_grade_entries(table_name: str, entry_list: list):
        """Adds a list or single grade report entry to the database
        Parameters:
            table_name (str): Name of the table to check for
            entry_list (list): List to add to DB as a record
        Returns:
            tuple: Will return tuple of tuples containing the result if no error was encountered
            str: Will return a string if an error was encountered
        """

        def split_to_string(i: list):
            # [year,semester,college,departmentName,course,section,honors,avgGPA,professorName,A,B,C,D,F,I,S,U,Q,X]
            return (f'({i[0]},"{i[1]}","{i[2]}","{i[3]}","{i[4]}","{i[5]}",{i[6]},{i[7]},"{i[8]}",'+
                    f'{i[9]},{i[10]},{i[11]},{i[12]},{i[13]},{i[14]},{i[15]},{i[16]},{i[17]},{i[18]})')

        try:
            Logger.log('Started adding new records to database', Importance.INFO)
            if isinstance(entry_list,list) and len(entry_list) > 0 and not isinstance(entry_list[0],list):
                # Logger.log(f'Adding new entry to {table_name}', Importance.DBUG)
                results = DatabaseHandler.send_query(f'INSERT INTO {table_name} '+
                f'(year,semester,college,departmentName,course,section,honors,avgGPA,professorName,numA,numB,numC,numD,numF,numI,numS,numU,numQ,numX) VALUES {split_to_string(entry_list)};')

            elif isinstance(entry_list,list) and len(entry_list) > 0 and isinstance(entry_list[0],list):
                to_add = ''
                results = []
                rows_added = 0
                batch_size = 50

                for entry in entry_list:
                    to_add += split_to_string(entry)+'@'

                to_add = to_add[:-1]
                # Logger.log(f'Adding new entries to {table_name}', Importance.DBUG)

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
                        results += DatabaseHandler.send_query(f'INSERT INTO {table_name}'+
                        f'(year,semester,college,departmentName,course,section,honors,avgGPA,professorName,numA,numB,numC,numD,numF,numI,numS,numU,numQ,numX) VALUES {combined[:-1]};')
                    else:
                        rows_added -= 1

                    to_add_split = to_add_split[tmp_batch_size:]

            elif len(entry_list) == 0:
                return ()
        except Exception as ex:
            print(f'>>> Error Executing DB Query: ERROR {ex}')
            Logger.log(f'>>> Error Executing DB Query: ERROR {ex}', Importance.CRIT)
            return f'ERROR {ex}'
        Logger.log(f'Finished adding new records({rows_added}) to database', Importance.INFO)
        return results
