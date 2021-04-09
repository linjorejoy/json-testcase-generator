from EntryCellColumn import EntryCellColumn

from typing import List

class EntryCellCollection:

    def __init__(self):
        self.entry_cells_collection:List[EntryCellColumn] = []

        entry_cell_column = EntryCellColumn()
        self.entry_cells_collection.append(entry_cell_column)