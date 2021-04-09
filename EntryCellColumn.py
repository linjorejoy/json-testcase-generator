
from EntryCell import EntryCell
from typing import List


class EntryCellColumn:

    def __init__(self, entry_cell:EntryCell = None, variable_name:str=None):
        self.variable_name = variable_name
        self.entry_cell_column:List[EntryCell] = []

        if entry_cell:
            self.entry_cell_column.append(entry_cell)

    def add_cell(self, entry_cell:EntryCell=None, key:str=None, value=None):
        if entry_cell:
            self.entry_cell_column.append(entry_cell)
            return
        
        if key and value:
            self.entry_cell_column.append(EntryCell(key, value))
            return
        else:
            raise KeyError

    def __hash__(self):
        return hash(self)