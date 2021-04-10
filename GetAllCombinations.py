from EntryCellCollection import EntryCellCollection
from EntryCellColumn import EntryCellColumn
from EntryCell import EntryCell 

from typing import Dict, List
from copy import deepcopy




def get_all_dictionaries(entry_cell_collections: EntryCellCollection):
    combinations = []
    template = {}

    def combine(entry_collections, combined_dict):
        if len(entry_collections.entry_cells_collection) == 0:
            return
        column = entry_collections.entry_cells_collection[0]
        if len(entry_collections.entry_cells_collection) == 1:
            
            for cell in column.entry_cell_column:
                combined_dict_copy = deepcopy(combined_dict)
                combined_dict_copy[column.variable_name] = cell.value
                combinations.append(combined_dict_copy)

        for cell in column.entry_cell_column:
            combined_dict_copy = deepcopy(combined_dict)
            combined_dict_copy[column.variable_name] = cell.value
            entry_collections_copy = deepcopy(entry_collections)
            del entry_collections_copy.entry_cells_collection[0]
            combine(entry_collections_copy, combined_dict_copy)
            


    combine(entry_cell_collections, template)
    return combinations
    