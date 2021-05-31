import json
import os

from helperobjects.OutputFiles import OutputFiles
from helperobjects.OutputJsonFile import OutputJsonFile
import helpermodules.PreferencesJsonHandler as PreferencesJsonHandler


def generate_all_files(output_files:OutputFiles, template:dict, output_location:str):
    for json_file_obj in output_files.get_output_json_file_array():
        json_str_template = json.dumps(template)
        this_obj_var_dict = json_file_obj.variable_dictionary
        for var in this_obj_var_dict.keys():
            json_str_template = json_str_template.replace(var, this_obj_var_dict[var])
        this_file_name = os.path.join(output_location, f"{json_file_obj.file_name}.json")
        indent_from_settings = int(PreferencesJsonHandler.get_data_from_settings("spacesForTabs"))
        with open (this_file_name, mode="w") as json_file:
            json.dump(json.loads(json_str_template), json_file, indent=indent_from_settings)


def generate_one_file(output_json_file:OutputJsonFile, template, output_location:str):
    json_str_template = json.dumps(template)
    this_obj_var_dict = output_json_file.variable_dictionary

    for var in this_obj_var_dict.keys():
        json_str_template = json_str_template.replace(var, this_obj_var_dict[var])
        
    this_file_name = os.path.join(output_location, f"{output_json_file.file_name}.json")
    
    output_json_file.temp_file_name = output_json_file.file_name

    overwriteExistingJsonWithSameFileName = PreferencesJsonHandler.get_data_from_settings("overwriteExistingJsonWithSameFileName")
    
    if os.path.exists(this_file_name) and not overwriteExistingJsonWithSameFileName: # True is for a future feature
        new_file_name = auto_increment_file_name(output_location, output_json_file.temp_file_name, "json")
        output_json_file.temp_file_name = new_file_name
        this_file_name = os.path.join(output_location, f"{new_file_name}.json")
        
    indent_from_settings = int(PreferencesJsonHandler.get_data_from_settings("spacesForTabs"))
    with open (this_file_name, mode="w") as json_file:
        json.dump(json.loads(json_str_template), json_file, indent=indent_from_settings)


def auto_increment_file_name(folder_name:str, file_name:str, file_extension:str) -> str:
    file_name
    i = 1
    while True:
        this_file_name = os.path.join(folder_name, f"{file_name}-({i}).{file_extension}")
        if not os.path.exists(this_file_name):
            return f"{file_name}-({i})"
        i += 1
    