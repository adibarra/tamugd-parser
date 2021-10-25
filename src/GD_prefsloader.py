# TAMU-GradeDistribution-ParserV2: GD_prefsloader.py
# @authors: github/adibarra


# imports
import os
import json


class PreferenceLoader:
    """ Class to load preferences on startup """

    db_address = 'localhost'
    db_port = '3306'
    db_user = 'database_username_here'
    db_pass = 'database_password_here'
    db_name = 'database_name_here'

    logger_enabled = True
    preferences_location = '../'
    preference_file = 'prefs.json'

    @staticmethod
    def generatePrefsFile():
        generated = False
        filecontents = {
            'database_host': 'localhost',
            'database_port': 3306,
            'database_username': 'database_username_here',
            'database_password': 'database_password_here',
            'database_name': 'database_name_here',
            'logger_enabled': True
        }

        try:
            # check if path to preferences file exists else create
            if not os.path.exists(os.path.dirname(os.path.realpath(__file__))+'/'+PreferenceLoader.preferences_location):
                original_umask = os.umask(0)
                os.makedirs(os.path.dirname(os.path.realpath(__file__))+'/'+PreferenceLoader.preferences_location)
                os.umask(original_umask)
        except Exception as e:
            print('There was an error while trying to create the '+PreferenceLoader.preferences_location+' directory:')
            print(e)

        # check if preferences file exists else create
        fileName = os.path.dirname(os.path.realpath(__file__))+'/'+PreferenceLoader.preferences_location+PreferenceLoader.preference_file
        if not os.path.isfile(fileName):
            try:
                # create preferences file with default settings
                with open(fileName, 'w') as (json_file):
                    json.dump(filecontents, json_file, indent=4)
                    generated = True
            except Exception as e:
                print('There was an error while trying to create the '+PreferenceLoader.preference_file+' file:')
                print(e)

        return generated

    @staticmethod
    def loadPrefs():
        if PreferenceLoader.generatePrefsFile():
            print('Generated preferences file ('+PreferenceLoader.preferences_location+PreferenceLoader.preference_file+')')
            print('Fill it out then restart the script when you are ready.')
            return False

        try:
            filePath = os.path.dirname(os.path.realpath(__file__))+'/'+PreferenceLoader.preferences_location+PreferenceLoader.preference_file
            with open(filePath) as json_file:
                prefs = json.load(json_file)

                PreferenceLoader.db_address = prefs['database_host']
                PreferenceLoader.db_port = prefs['database_port']
                PreferenceLoader.db_user = prefs['database_username']
                PreferenceLoader.db_pass = prefs['database_password']
                PreferenceLoader.db_name = prefs['database_name']
                PreferenceLoader.logger_enabled = prefs['logger_enabled']
                return True

        except Exception as e:
            print('RUNTIME ERROR: Failed to open Prefs file.')
            print(e)
            return False
