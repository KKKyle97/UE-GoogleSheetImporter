from __future__ import print_function
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv
import os
import sys
import subprocess
import pandas as pd
import asyncio
import httpx

# function built specially for unreal
# because the script will be run in unreal specific python env
# instead of the local pc env


def check_if_module_exists(module_name):
    try:
        __import__(module_name)
        print(f"The module '{module_name}' exists.")
        return True
    except ImportError:
        print(f"The module'{module_name}' does not exists.")
        return False


def try_install_module(module_name, python_executable_directory):
    try:
        subprocess.check_call(
            [python_executable_directory, "-m", "pip", "install", module_name], shell=False)
        print(f"Successfully installed {module_name}")
    except subprocess.CalledProcessError:
        print(f"Error installing {module_name}")
        sys.exit(f"unable to install {module_name}, ending script here...")


def get_unreal_python_executable_directory(path):
    unreal_engine_root_directory = os.path.dirname(os.path.abspath(path))
    return unreal_engine_root_directory + os.getenv('PATH_TO_PYTHON')


def get_project_excel_file_directory(path):
    unreal_project_root_directory = os.path.dirname(os.path.abspath(path))
    return unreal_project_root_directory + os.getenv('PATH_TO_CSV_OUTPUT_FILE')


def get_current_script_directory():
    return os.path.dirname(os.path.abspath(__file__))

# end of unreal specific function


def setup_google_api_creds():
    CREDENTIAL_JSON = os.getenv('CREDENTIAL_JSON')
    TOKEN_JSON = os.getenv('TOKEN_JSON')
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIAL_JSON, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_JSON, 'w') as token:
            token.write(creds.to_json())

    return creds


async def get_data_from_google_spreadsheet():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    SAMPLE_SPREADSHEET_ID = os.getenv('SAMPLE_SPREADSHEET_ID')
    SAMPLE_RANGE_NAME = os.getenv('SAMPLE_RANGE_NAME')
    TITLES_FOR_VALUE = os.getenv('TITLES_FOR_VALUE')
    creds = setup_google_api_creds()
    try:
        # traditional api calling way to support async await
        async with httpx.AsyncClient() as client:
            url = f'https://sheets.googleapis.com/v4/spreadsheets/{SAMPLE_SPREADSHEET_ID}/values/{SAMPLE_RANGE_NAME}'
            headers = {
                'Authorization': f'Bearer {creds.token}',
                'Content-Type': 'application/json'
            }

            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            values = data['values']
            for row in values:
                print(row)

        # # Call the Sheets API using google provided library
        # service = build('sheets', 'v4', credentials=creds)
        # sheet = service.spreadsheets()
        # request = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
        #                              range=SAMPLE_RANGE_NAME)
        # response = request.execute()
        # print(response)
        # values = result.get('values', [])

        df = pd.DataFrame(values, columns=TITLES_FOR_VALUE)
        print(df)
        df.to_csv('../ReferencedData/TestData.csv',
                  index=False, index_label=False)

    except HttpError as err:
        print(err)


def main():
    asyncio.run(get_data_from_google_spreadsheet())

# current unreal (5.2) only has python 3.9.7 install by default
# all unreal specific function will be commented until further updates
# check command line args
# args = sys.argv
# if (len(args) <= 2):
#     sys.exit(
#         "Not enough args. Please specify 'UNREAL_ENGINE_ROOT_PATH' and 'UNREAL_PROJECT_ROOT_PATH' as cmd args when executing script")

# install dotenv to get all the env var
# module_dotenv = 'dotenv'

# if (not (check_if_module_exists(module_dotenv))):
#     try_install_module(module_dotenv, get_unreal_python_executable_directory())

# for module in os.getenv('MODULES_TO_INSTALL'):
#     if (not (check_if_module_exists(module))):
#         try_install_module(module, get_unreal_python_executable_directory())


if __name__ == '__main__':
    load_dotenv()
    main()
