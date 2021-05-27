import json
import os
from helpermodules.constants import settings_dict

def overwrite_settings_json_file(json_obj:dict):
    settings_file_path = os.path.join(os.getenv('ProgramData'), 'JSON Test Case Generator')
    preferences_file_path = os.path.join(settings_file_path, "settings.json")
    
    try:
        with open(preferences_file_path, mode="w") as settings_json:
            json.dump(json_obj, settings_json, indent=2)
    except Exception:
        print("Error Occured")
    
def add_settings_json_file():
    settings_file_path = os.path.join(os.getenv('ProgramData'), 'JSON Test Case Generator')
    preferences_file_path = os.path.join(settings_file_path, "settings.json")
    
    if os.path.exists(preferences_file_path):
        return
    try:
        with open(preferences_file_path, mode="w") as settings_json:
            json.dump(settings_dict, settings_json, indent=2)
    except Exception:
        print("Error Occured")


def get_data_from_settings(path:str):
    keys = path.split("/")
    keys_history = []
    add_settings_json_file()
    settings_data_obj_from_file = {}
    settings_data_obj_from_file_parts = {}
    settings_data_obj_from_constants = settings_dict.copy()
    settings_file_path = os.path.join(os.getenv('ProgramData'), 'JSON Test Case Generator')
    preferences_file_path = os.path.join(settings_file_path, "settings.json")

    with open(preferences_file_path, mode="r") as settings_json_file:
        settings_data_obj_from_file = json.load(settings_json_file)
        settings_data_obj_from_file_parts = settings_data_obj_from_file.copy()

    while True:
        if not keys:
            return settings_data_obj_from_file_parts
        if keys[0] in settings_data_obj_from_file_parts.keys():
            settings_data_obj_from_file_parts = settings_data_obj_from_file_parts[keys[0]]
            settings_data_obj_from_constants = settings_data_obj_from_constants[keys[0]]
            keys_history.append(keys.pop(0))
        else:
            if keys[0] in settings_data_obj_from_constants.keys():
                settings_data_obj_from_file_parts = settings_data_obj_from_constants[keys[0]]
                settings_data_obj_from_constants = settings_data_obj_from_constants[keys[0]]
                with open(preferences_file_path, mode="w") as settings_json_file_new:
                    json.dump(settings_dict, settings_json_file_new, indent=2)
                keys_history.append(keys.pop(0))
            else:
                return None
