
from helperobjects.EntryCell import EntryCell

def check_if_num(num:str) -> bool:
    try:
        float(num)
        return True
    except ValueError:
        return False

def get_bool(string:str) -> bool:
    string = string.lower()
    true_vals = ["true", "1", "t"]
    false_vals = ["false", "0", "f"]
    if string in true_vals:
        return True
    elif string in false_vals:
        return False
    else:
        return True

def get_null(string:str):
    return "null"

def add_to_var_dict(dictionary:dict, key:str, entry:EntryCell):

    data_type = entry.option_value.get()
    value = entry.entry.get()

    # str data types
    if data_type == "str":
        dictionary[key] = value

    # int Data Types
    elif data_type == "int":
        if check_if_num(value):
            key = "\"" + key + "\""
            dictionary[key] = str(int(float(value)))
        else:
            dictionary[key] = value

    # Float Data Types
    elif data_type == "float":
        if check_if_num(value):
            key = "\"" + key + "\""
            dictionary[key] = str(float(str(value)))
        else:
            dictionary[key] = value

    # bool Data types
    elif data_type == "bool":
        key = "\"" + key + "\""
        dictionary[key] = str(get_bool(value)).lower()


    # bool Data types
    elif data_type == "null":
        key = "\"" + key + "\""
        dictionary[key] = get_null(value)

    return dictionary

def genetrate_variable_dictionary(variables:list[str], entry_cells:list[EntryCell]):
    variable_dictionary = {}
    for var, entry_cell in zip(variables, entry_cells):
        variable_dictionary = add_to_var_dict(variable_dictionary, var, entry_cell)
    
    return variable_dictionary