from EntryCellColumn import EntryCellColumn

from typing import List

class EntryCellCollection:

    def __init__(self, entry_cell_column:EntryCellColumn = None):
        self.entry_cells_collection:List[EntryCellColumn] = []

        if entry_cell_column:
            self.entry_cells_collection.append(entry_cell_column)

    def add_column(self, entry_cell_column:EntryCellColumn = None):
        self.entry_cells_collection.append(entry_cell_column)

    def __hash__(self):
        return hash(self)