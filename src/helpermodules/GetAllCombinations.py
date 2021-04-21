from helperobjects.EntryCellCollection import EntryCellCollection
from helperobjects.EntryCellColumn import EntryCellColumn
from helperobjects.EntryCell import EntryCell 

from typing import Dict, List
from copy import deepcopy

def get_all_dictionaries(entry_cell_collections: EntryCellCollection):
    combinations = []
    template = {}
    variables = [column.variable_name for column in entry_cell_collections.get_all_columns()]

    def combine2(entry_collections, combined_dict, index):
        
        if len(variables) == index:
            combinations.append(combined_dict)
            return
        
        
        for cell in entry_collections.get_all_columns()[index].get_all_cells():
            combined_dict_copy = deepcopy(combined_dict)
            combined_dict_copy[variables[index]] = cell.value
            combine2(entry_collections, combined_dict_copy, index + 1)
            
    combine2(entry_cell_collections, template, 0)
    return combinations
    