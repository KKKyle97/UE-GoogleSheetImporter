from __future__ import print_function
import os
import sys
import subprocess
import asyncio
import time


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


def try_install_module(module_name, python_executable_directory, log_directory):
    try:
        with open(f'{log_directory}/error.log', 'w') as f:
            subprocess.check_call(
                [python_executable_directory, "-m", "pip", "install", module_name], shell=False, stderr=f)
        print(f"Successfully installed {module_name}")
    except subprocess.CalledProcessError:
        print(f"Error installing {module_name}")
        sys.exit(f"unable to install {module_name}, ending script here...")


def get_unreal_python_executable_directory(path):
    unreal_engine_root_directory = os.path.dirname(os.path.abspath(path))
    return (unreal_engine_root_directory + "/Binaries/ThirdParty/Python3/Win64/python.exe").replace('\\', '/')


def get_project_excel_file_directory(path):
    return (path + "ReferenceData").replace('\\', '/')


def get_current_script_directory():
    return os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')

# end of unreal specific function


def massage_array_like_string_from_env(string):
    string = string.replace("[", "")
    string = string.replace("]", "")
    string = string.replace("'", "")
    string = string.replace(" ", "")
    return string.split(",")


def setup_google_api_creds():
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.oauth2.credentials import Credentials
    CREDENTIAL_JSON = env_vars['CREDENTIAL_JSON']
    TOKEN_JSON = env_vars['TOKEN_JSON']
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    PATH_TO_TOKEN = f'{get_current_script_directory()}/{TOKEN_JSON}'
    PATH_TO_CREDENTIAL = f'{get_current_script_directory()}/{CREDENTIAL_JSON}'
    if os.path.exists(PATH_TO_TOKEN):
        creds = Credentials.from_authorized_user_file(PATH_TO_TOKEN, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                PATH_TO_CREDENTIAL, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(PATH_TO_TOKEN, 'w') as token:
            token.write(creds.to_json())

    return creds


async def get_data_from_google_spreadsheet():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    import pandas as pd
    import httpx
    from googleapiclient.errors import HttpError
    SAMPLE_SPREADSHEET_ID = env_vars['SAMPLE_SPREADSHEET_ID']
    SAMPLE_RANGE_NAME = env_vars['SAMPLE_RANGE_NAME']
    TITLES_FOR_VALUE = massage_array_like_string_from_env(
        env_vars['TITLES_FOR_VALUES'])
    creds = setup_google_api_creds()
    slow_task.enter_progress_frame(25)
    time.sleep(2)
    try:
        # traditional api calling way to support async await
        async with httpx.AsyncClient() as client:
            url = f'https://sheets.googleapis.com/v4/spreadsheets/{SAMPLE_SPREADSHEET_ID}/values/{SAMPLE_RANGE_NAME}'
            headers = {
                'Authorization': f'Bearer {creds.token}',
                'Content-Type': 'application/json'
            }

            response = await client.get(url, headers=headers)
            slow_task.enter_progress_frame(25)
            time.sleep(2)
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

        slow_task.enter_progress_frame(25)
        time.sleep(2)
        # create dataframe and write to csv
        df = pd.DataFrame(values, columns=TITLES_FOR_VALUE)
        df.to_csv(f'{get_project_excel_file_directory(unreal_engine_project_dir)}\TestData.csv',
                  index=False, index_label=False)

    except HttpError as err:
        print(err)


def main():
    asyncio.run(get_data_from_google_spreadsheet())


# check command line args
args = sys.argv
if (len(args) <= 2):
    sys.exit(
        "Not enough args. Please specify 'UNREAL_PROJECT_ROOT_PATH'and 'UNREAL_ENGINE_ROOT_PATH' as cmd args when executing script")

# save command-line args to variable
unreal_engine_project_dir = args[1]
unreal_engine_root_dir = args[2]

# install dotenv to get all the env var
module_dotenv = 'python-dotenv'

if (not (check_if_module_exists(module_dotenv))):
    try_install_module(
        module_dotenv, get_unreal_python_executable_directory(unreal_engine_root_dir), unreal_engine_project_dir)


if __name__ == '__main__':
    import unreal
    total_frames = 100
    text_label = "Importing data from google sheet..."

    with unreal.ScopedSlowTask(total_frames, text_label) as slow_task:
        slow_task.make_dialog(True)
        from dotenv import dotenv_values
        env_vars = dotenv_values(
            f'{get_current_script_directory()}/.env')

        module_to_install = massage_array_like_string_from_env(
            env_vars['MODULES_TO_INSTALL'])

        # install all the required modules
        for module in module_to_install:
            if (not (check_if_module_exists(module))):
                try_install_module(
                    module, get_unreal_python_executable_directory(unreal_engine_root_dir), get_current_script_directory())
        slow_task.enter_progress_frame(25)
        time.sleep(2)
        # run main
        main()
