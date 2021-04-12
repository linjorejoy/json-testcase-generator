
from helperobjects.EntryCell import EntryCell
from typing import List


class EntryCellColumn:

    def __init__(self, entry_cell:EntryCell = None, variable_name:str=None):
        self.variable_name = variable_name
        self.entry_cell_count = 0
        self.entry_cell_column:List[EntryCell] = []

        if entry_cell:
            self.entry_cell_column.append(entry_cell)

    def add_cell(self, entry_cell:EntryCell=None, value=None):
        if entry_cell:
            self.entry_cell_column.append(entry_cell)
            self.entry_cell_count += 1
            return self.entry_cell_count
        
        if value:
            self.entry_cell_column.append(EntryCell(value=value))
            self.entry_cell_count += 1
            return self.entry_cell_count
        else:
            raise KeyError

    def __hash__(self):
        return hash(self)