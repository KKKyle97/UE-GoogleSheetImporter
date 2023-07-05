# UE-GoogleSheetImporter



**Problem statement**: When using vcs in unreal engine, files are normally locked / checkout by the person that's editing it. This become a huge problem when multiple designer / programmer are tweaking values in certain datatable in unreal engine editor.

**Description**: This is an unreal engine editor tool that will import data from google spread sheet into unreal engine datatable. This tool aims to solve the problem mentioned above by having values that's constantly being tweaked save in google spreadsheet instead. All the designers should only amend the values in google spreadsheet and import it when needed. Before running a new build to package the game, the designer / programmer would use this editor tool to import the amended data.

## Important
* This tool is in POC **(Proof of Concept)** stage
    * Does not fully validate all the data from google spreadsheet api
* it showcase the flow of importing and filling datatable 
* It can convert whatever type that's supported by unreal "Fill datatable" node (mostly string and numbers)


## Importing Process
![Untitled Diagram drawio](https://github.com/KKKyle97/UE-GoogleSheetImporter/assets/68265288/df02be2c-3b84-48f4-bcdb-526d2ff69fd5)


## Running Environment
| Software      | Version |
| ------------- | ------- |
| Unreal Engine | 5.2.1   |
| Python        | 3.9.7   |

## .env Variables
| Title                   | Value                                                                                           |
| ----------------------- | ------------------------------------------------------------------------------------------------|
| MODULES_TO_INSTALL      | ['pandas', 'google-api-python-client', 'google-auth-httplib2', 'google-auth-oauthlib', 'httpx'] |
| TITLES_FOR_VALUES       | DATATABLE_ROW_TITLE                                                                             |
| SAMPLE_SPREADSHEET_ID   | YOUR_SPREADSHEET_ID                                                                             |
| SAMPLE_RANGE_NAME       | SPREADSHEET_TABLE_RANGE                                                                         |
| PATH_TO_PYTHON          | UNREAL_ENGINE_PATH_TO_PYTHON                                                                    |
| PATH_TO_CSV_OUTPUT_FILE | CSV_FOLDER_IN_YOUR_PROJECT                                                                      |
| CREDENTIAL_JSON         | CREDENTIAL_JSON_FILE_NAME                                                                       |
| TOKEN_JSON              | TOKEN_JSON_FILE_NAME                                                                            |

## Demo
![Animation](https://github.com/KKKyle97/UE-GoogleSheetImporter/assets/68265288/76c30e75-0c48-491d-b007-3488a5e190f2)

