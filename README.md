# UE-GoogleSheetImporter



**Problem statement**: When using vcs in unreal engine, files are normally locked / checkout by the person that's editing it. This become a huge problem when multiple designer / programmer are tweaking values in certain datatable in unreal engine editor.

**Description**: This is a unreal engine editor tool that will import data from google spread sheet into unreal engine datatable. This tool aims to solve the problem mentioned above by having values that's constantly being tweaked save in google spreadsheet instead. All the designers should only amend the values in google spreadsheet and import it when needed. Before running a new build to package the game, the designer / programmer would use this editor tool to import the amended data.

## Important
* This tool is in POC **(Proof of Concept)** stage
    * Does not fully validate all the data from google spreadsheet api
* it showcase the flow of importing and filling datatable 
* It can convert whatever type that's supported by unreal "Fill datatable" node (mostly string and numbers)


## Importing Process
