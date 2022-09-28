# TAMU-GradeDistribution-ParserV2: gd_prefsloader.py
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
    db_grades_table = 'grades_table_name_here'
    db_status_table = 'status_table_name_here'

    logger_enabled = True
    preferences_location = '../'
    preference_file = 'prefs.json'

    @staticmethod
    def generate_prefs_file():
        generated = False
        filecontents = {
            'database_host': 'localhost',
            'database_port': 3306,
            'database_name': 'database_name_here',
            'database_username': 'database_username_here',
            'database_password': 'database_password_here',
            'db_grades_table': 'grades_table_name_here',
            'db_status_table': 'status_table_name_here',
            'logger_enabled': True
        }

        try:
            # check if path to preferences file exists else create
            if not os.path.exists(f'{os.path.dirname(os.path.realpath(__file__))}/{PreferenceLoader.preferences_location}'):
                original_umask = os.umask(0)
                os.makedirs(f'{os.path.dirname(os.path.realpath(__file__))}/{PreferenceLoader.preferences_location}')
                os.umask(original_umask)
        except Exception as ex:
            print(f'There was an error while trying to create the {PreferenceLoader.preferences_location} directory:')
            print(ex)

        # check if preferences file exists else create
        file_name = f'{os.path.dirname(os.path.realpath(__file__))}/{PreferenceLoader.preferences_location}{PreferenceLoader.preference_file}'
        if not os.path.isfile(file_name):
            try:
                # create preferences file with default settings
                with open(file_name,'w') as json_file:
                    json.dump(filecontents, json_file, indent=4)
                    generated = True
            except Exception as ex:
                print(f'There was an error while trying to create the {PreferenceLoader.preference_file} file:')
                print(ex)

        return generated

    @staticmethod
    def load_prefs():
        if PreferenceLoader.generate_prefs_file():
            print(f'Generated preferences file ({PreferenceLoader.preferences_location}{PreferenceLoader.preference_file})')
            print('Fill it out then restart the script when you are ready.')
            return False

        try:
            file_path = f'{os.path.dirname(os.path.realpath(__file__))}/{PreferenceLoader.preferences_location}{PreferenceLoader.preference_file}'
            with open(file_path,'r') as json_file:
                prefs = json.load(json_file)

                PreferenceLoader.db_address = prefs['database_host']
                PreferenceLoader.db_port = prefs['database_port']
                PreferenceLoader.db_name = prefs['database_name']
                PreferenceLoader.db_user = prefs['database_username']
                PreferenceLoader.db_pass = prefs['database_password']
                PreferenceLoader.db_grades_table = prefs['db_grades_table']
                PreferenceLoader.db_status_table = prefs['db_status_table']
                PreferenceLoader.logger_enabled = prefs['logger_enabled']
                return True

        except Exception as ex:
            print('RUNTIME ERROR: Failed to open Prefs file.')
            print(ex)
            return False
