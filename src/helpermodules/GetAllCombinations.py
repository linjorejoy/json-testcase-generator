from helperobjects.EntryCellCollection import EntryCellCollection
from helperobjects.EntryCellColumn import EntryCellColumn
from helperobjects.EntryCell import EntryCell 

from typing import Dict, List

def get_all_dictionaries(entry_cell_collections: EntryCellCollection):
    combinations = []
    template = {}
    variables = [column.variable_name for column in entry_cell_collections.get_all_columns()]

    def combine(entry_collections, combined_dict, index):
        
        if len(variables) == index:
            combinations.append(combined_dict)
            return
        
        
        for cell in entry_collections.get_all_columns()[index].get_all_cells():
            combined_dict_copy = combined_dict.copy()
            combined_dict_copy[variables[index]] = cell.value
            combine(entry_collections, combined_dict_copy, index + 1)
            
    combine(entry_cell_collections, template, 0)
    return combinations
    

def add_value_to_dict(dictionary:dict, key:str, cell:EntryCell):
    type_of_value = cell.option_value.get()

    if type_of_value == "str":
        dictionary[key] = cell.entry.get()
    elif type_of_value == "int":

        pass
    elif type_of_value == "float":
        pass
    elif type_of_value == "bool":
        pass
    elif type_of_value == "null":
        pass