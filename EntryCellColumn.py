
from EntryCell import EntryCell
from typing import List


class EntryCellColumn:

    def __init__(self):
        self.entry_cell_column:List[EntryCell] = []


        entry_cell = EntryCell(None)
        self.entry_cell_column.append(entry_cell)

