import json
import os

from OutputFiles import OutputFiles
from OutputJsonFile import OutputJsonFile


def generate_all_files(output_files:OutputFiles, template:dict, output_location:str):
    for json_file_obj in output_files.get_output_json_file_array():
        json_str_template = json.dumps(template)
        this_obj_var_dict = json_file_obj.variable_dictionary
        for var in this_obj_var_dict.keys():
            json_str_template = json_str_template.replace(var, this_obj_var_dict[var])
        this_file_name = os.path.join(output_location, f"{json_file_obj.file_name}.json")
        with open (this_file_name, mode="w") as json_file:
            json.dump(json.loads(json_str_template), json_file, indent=2)


def generate_one_file(output_json_file:OutputJsonFile, template, output_location:str):
    json_str_template = json.dumps(template)
    this_obj_var_dict = output_json_file.variable_dictionary

    for var in this_obj_var_dict.keys():
        json_str_template = json_str_template.replace(var, this_obj_var_dict[var])
        
    this_file_name = os.path.join(output_location, f"{output_json_file.file_name}.json")
    with open (this_file_name, mode="w") as json_file:
        json.dump(json.loads(json_str_template), json_file, indent=2)
