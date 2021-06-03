from helperobjects.EntryCellCollection import EntryCellCollection
from helperobjects.OutputFiles import OutputFiles
from helperobjects.OutputJsonFile import OutputJsonFile
from tkinter import StringVar, Entry
import re
import helpermodules.PreferencesJsonHandler as PreferencesJsonHandler



def autocorrect_filename(name:str)-> str:
    name = re.sub(r"[\\/\^\?\<\>:|\*]", "_",name)
    return name


def get_name(output_json_file:OutputJsonFile, ref_arr, GENERATE_NAMES):
    name = ""
    counter_present = False
    counter_position = 0
    for ref in ref_arr:
        if isinstance(ref, Entry): # Entry cell
            
            name += autocorrect_filename(ref.get())

        elif isinstance(ref, StringVar):# Dropdown
            
            if ref.get() == None or ref.get() == "None":
                pass
            elif ref.get() == "Counter":# Counter
                counter_present = True
                counter_position = len(name)
            elif ref.get() == "AdditionalComment":# Comment
                name += autocorrect_filename(output_json_file.comment)
            else:
                name += autocorrect_filename(str(output_json_file.variable_dictionary[ref.get()]))
                # name += str(output_json_file.variable_dictionary[variable_arr[ref-1]])
    if counter_present:
        counter_start = int(PreferencesJsonHandler.get_data_from_settings("fileNameCounterStart"))
        counter = counter_start
        name = name[:counter_position] + str(counter) + name[counter_position:]
        
        while True:
            
            if name in GENERATE_NAMES:
                counter += 1
                name = name[:counter_position] + str(counter) + name[(counter_position+len(str(counter))):]
            else:
                break
    
    autoAddCounterForGeneratedFiles = PreferencesJsonHandler.get_data_from_settings("autoAddCounterForGeneratedFiles")

    if autoAddCounterForGeneratedFiles == "True":

        if name in GENERATE_NAMES:
            counter_position = len(name)
            counter = int(PreferencesJsonHandler.get_data_from_settings("fileNameCounterStart"))
            name = name[:counter_position] + str(counter) + name[counter_position:]
            
            while True:
                
                if name in GENERATE_NAMES:
                    counter += 1
                    name = name[:counter_position] + str(counter) + name[(counter_position+len(str(counter))):]
                else:
                    break

    return name
    

    
def generate_file_name(output_files:OutputFiles, ref_arr):
    GENERATE_NAMES = []
    for each_json_file in output_files.get_output_json_file_array():
        name = get_name(each_json_file, ref_arr, GENERATE_NAMES)
        name = autocorrect_filename(name)
        GENERATE_NAMES.append(name)
        each_json_file.file_name = name
        each_json_file.temp_file_name = name
