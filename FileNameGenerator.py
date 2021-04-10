from EntryCellCollection import EntryCellCollection
from OutputFiles import OutputFiles
from OutputJsonFile import OutputJsonFile

GENERATE_NAMES = []

def generate_file_name(entry_cells_collection:OutputFiles, ref_arr, variable_arr):
    for each_json_file in entry_cells_collection.get_output_json_file_array():
        name = get_name(each_json_file, ref_arr, variable_arr)
        GENERATE_NAMES.append(name)
        each_json_file.file_name = name


def get_name(output_json_file:OutputJsonFile, ref_arr, variable_arr):
    name = ""
    counter_present = False
    counter_position = 0
    for ref in ref_arr:
        if isinstance(ref, str):
            name += ref

        elif isinstance(ref, int):
            if ref == -1:
                pass
            elif ref == 0:# Counter
                counter_present = True
                counter_position = len(name)
            elif ref > len(variable_arr):
                break
            else:
                name += str(output_json_file.variable_dictionary[variable_arr[ref-1]])
    if counter_present:
        counter = 1
        name = name[:counter_position] + str(counter) + name[counter_position:]
        
        while True:

            if name in GENERATE_NAMES:
                counter += 1
                name = name[:counter_position] + str(counter) + name[(counter_position+1):]
            else:
                break

    return name