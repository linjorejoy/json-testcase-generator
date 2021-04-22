
from helperobjects.EntryCell import EntryCell
from typing import List

class EntryCellRow:

    def __init__(self):
        self.file_name:str = None
        self.entry_cell_list:List[EntryCell] = []

    def add_cell(self, entry_cell:EntryCell):
        self.entry_cell_list.append(entry_cell)

    def get_all(self):
        return self.entry_cell_list

    def __hash__(self):
        return hash(self.__key)

    def __key(self):
        return (self.file_name.__hash__, self.entry_cell_list.__hash__)
        