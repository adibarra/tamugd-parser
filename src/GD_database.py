# TAMU-GradeDistribution-ParserV2: GD_database.py
# @authors: github/adibarra


# imports
import math
import pymysql
from GD_logger import Logger, Importance
from GD_prefsloader import PreferenceLoader


class DatabaseHandler:
    """ This is a class to handle database queries """

    @staticmethod
    def checkDBConnection():
        """Checks connection to database.
        Returns:
            bool: True if connection successful, else False
        """

        return (DatabaseHandler.checkDBConnectionError() == 'No Error')


    @staticmethod
    def checkDBConnectionError():
        """Checks database connection error.
        Returns:
            str: String representing error, None otherwise
        """

        try:
            db = pymysql.connect(host=PreferenceLoader.db_address, user=PreferenceLoader.db_user,
                                 password=PreferenceLoader.db_pass, database=PreferenceLoader.db_name, autocommit=True)
            cursor = db.cursor()
            cursor.execute('show tables;')
            cursor.fetchall()
            db.close()
        except pymysql.Error as e:
            return str(e.args[0])+': '+str(e.args[1])
        return 'No Error'


    @staticmethod
    def sendQuery(message:str):
        """Send a querty to the database server.
        Parameters:
            message (str): The command to send to the MySQL database
        Returns:
            tuple: Will return tuple of tuples containing the result if no error was encountered
            str: Will return a string if an error was encountered
        """

        try:
            db = pymysql.connect(host=PreferenceLoader.db_address, user=PreferenceLoader.db_user,
                                 password=PreferenceLoader.db_pass, database=PreferenceLoader.db_name, autocommit=True)
            cursor = db.cursor()
            #Logger.log('>>> Executing DB Query: '+message, Importance.DBUG)
            cursor.execute(message)
            results = cursor.fetchall()
            db.close()
        except pymysql.Error as e:
            Logger.log('>>> Error Executing DB Query: ERROR '+str(e), Importance.CRIT)
            return 'ERROR '+str(e)
        return results


    @staticmethod
    def addGradeEntries(tableName:str, entrylist:list):
        """Adds a list or single grade report entery to the database
        Parameters:
            tableName (str): Name of the table to check for
            entry (list): List to add to DB as a record
        Returns:
            tuple: Will return tuple of tuples containing the result if no error was encountered
            str: Will return a string if an error was encountered
        """
        
        def splitToString(entry:list):
            # [year,semester,college,departmentName,course,section,honors,avgGPA,professorName,A,B,C,D,F,I,S,U,Q,X]
            return ('('+str(entry[ 0])+',"'+str(entry[ 1])+'","'+str(entry[ 2])+'","'+str(entry[ 3])+'","'+str(entry[ 4])+'","'+str(entry[ 5])+'",'+str(entry[ 6])+','
                       +str(entry[ 7])+',"'+str(entry[ 8])+'",' +str(entry[ 9])+ ',' +str(entry[10])+ ',' +str(entry[11])+ ',' +str(entry[12])+ ','+str(entry[13])+','
                       +str(entry[14])+',' +str(entry[15])+ ',' +str(entry[16])+ ',' +str(entry[17])+ ',' +str(entry[18])+ ')')
        
        try:
            Logger.log('Started adding new records to database', Importance.INFO)
            if type(entrylist) == type([]) and len(entrylist) > 0 and type(entrylist[0]) != type([]):
                #Logger.log('Adding new entry to '+tableName, Importance.DBUG)
                results = DatabaseHandler.sendQuery('INSERT INTO '+tableName+' '
                    +'(year,semester,college,departmentName,course,section,honors,avgGPA,professorName,numA,numB,numC,numD,numF,numI,numS,numU,numQ,numX) VALUES '
                    +splitToString(entrylist)+';')
            
            elif type(entrylist) == type([]) and len(entrylist) > 0 and type(entrylist[0]) == type([]):
                toAdd = ''
                results = []
                rowsAdded = 0
                batchSize = 50
                
                for entry in entrylist:
                    toAdd += splitToString(entry)+'@'
                
                toAdd = toAdd[:-1]
                #Logger.log('Adding new entries to '+tableName, Importance.DBUG)
                
                # add batchSize at a time until out of records then the remainder
                toAddSplit = toAdd.split('@')
                if len(toAddSplit) > batchSize+1:
                        tmpBatchSize = batchSize
                else:
                    tmpBatchSize = len(toAddSplit)
                
                savelen = math.ceil(len(toAddSplit)/tmpBatchSize)
                for i in range(0, savelen):
                    if len(toAddSplit) > batchSize+1:
                        tmpBatchSize = batchSize
                    else:
                        tmpBatchSize = len(toAddSplit)
                    
                    combined = ''
                    rowsAdded += tmpBatchSize
                    for k in range(0, tmpBatchSize):
                        combined += toAddSplit[k]+','
                    
                    if combined[:-1] != '':
                        results += DatabaseHandler.sendQuery('INSERT INTO '+tableName+' '
                            +'(year,semester,college,departmentName,course,section,honors,avgGPA,professorName,numA,numB,numC,numD,numF,numI,numS,numU,numQ,numX) VALUES '+combined[:-1]+';')
                    else:
                        rowsAdded -= 1
                    
                    toAddSplit = toAddSplit[tmpBatchSize:]
            
            elif len(entrylist) == 0:
                return ()            
                        
        except pymysql.Error as e:
            Logger.log('>>> Error Executing DB Query: ERROR '+str(e), Importance.WARN)
            return 'ERROR '+str(e)
        Logger.log('Finished adding new records('+str(rowsAdded)+') to database', Importance.INFO)
        return results