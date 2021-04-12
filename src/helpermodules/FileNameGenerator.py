from helperobjects.EntryCellCollection import EntryCellCollection
from helperobjects.OutputFiles import OutputFiles
from helperobjects.OutputJsonFile import OutputJsonFile
from tkinter import StringVar, Entry

GENERATE_NAMES = []

# def generate_file_name(entry_cells_collection:OutputFiles, ref_arr, variable_arr):
#     for each_json_file in entry_cells_collection.get_output_json_file_array():
#         name = get_name(each_json_file, ref_arr, variable_arr)
#         GENERATE_NAMES.append(name)
#         each_json_file.file_name = name


# def get_name(output_json_file:OutputJsonFile, ref_arr, variable_arr):
#     name = ""
#     counter_present = False
#     counter_position = 0
#     for ref in ref_arr:
#         if isinstance(ref, str):
#             name += ref

#         elif isinstance(ref, int):
#             if ref == -1:
#                 pass
#             elif ref == 0:# Counter
#                 counter_present = True
#                 counter_position = len(name)
#             elif ref > len(variable_arr):
#                 break
#             else:
#                 name += str(output_json_file.variable_dictionary[variable_arr[ref-1]])
#     if counter_present:
#         counter = 1
#         name = name[:counter_position] + str(counter) + name[counter_position:]
        
#         while True:

#             if name in GENERATE_NAMES:
#                 counter += 1
#                 name = name[:counter_position] + str(counter) + name[(counter_position+1):]
#             else:
#                 break

#     return name


def generate_file_name(output_files:OutputFiles, ref_arr):
    for each_json_file in output_files.get_output_json_file_array():
        name = get_name(each_json_file, ref_arr)
        GENERATE_NAMES.append(name)
        each_json_file.file_name = name


def get_name(output_json_file:OutputJsonFile, ref_arr):
    name = ""
    counter_present = False
    counter_position = 0
    for ref in ref_arr:
        if isinstance(ref, Entry): # Entry cell
            
            name += ref.get()

        elif isinstance(ref, StringVar):# Dropdown
            
            if ref.get() == None or ref.get() == "None":
                pass
            elif ref.get() == "Counter":# Counter
                # print("Counter.....")
                counter_present = True
                counter_position = len(name)
            else:
                name += str(output_json_file.variable_dictionary[ref.get()])
                # name += str(output_json_file.variable_dictionary[variable_arr[ref-1]])
    if counter_present:
        counter = 1
        name = name[:counter_position] + str(counter) + name[counter_position:]
        
        while True:
            
            if name in GENERATE_NAMES:
                counter += 1
                name = name[:counter_position] + str(counter) + name[(counter_position+len(str(counter))):]
            else:
                break

    return name