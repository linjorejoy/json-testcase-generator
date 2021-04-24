from helperobjects.EntryCellColumn import EntryCellColumn
from helperobjects.EntryCellRow import EntryCellRow

from typing import List

class EntryCellCollection:

    def __init__(self, entry_cell_column:EntryCellColumn = None):
        self.entry_cells_collection:List[EntryCellColumn] = []
        self.entry_cell_rows:List[EntryCellRow] = []
        self.column_count = 0
        self.row_count = 0

        if entry_cell_column:
            self.column_count += 1
            self.entry_cells_collection.append(entry_cell_column)

    def add_column(self, entry_cell_column:EntryCellColumn = None):
        self.entry_cells_collection.append(entry_cell_column)
        self.column_count += 1
    
    def add_row(self, entry_cell_row:EntryCellRow=None):
        self.entry_cell_rows.append(entry_cell_row)
        self.row_count += 1

    def delete_row(self,entry_row:EntryCellRow):
        for index, row in enumerate(self.entry_cell_rows):
            if row == entry_row:
                del self.entry_cell_rows[index]
        

    def get_all_columns(self):
        return self.entry_cells_collection


    def get_all_rows(self):
        return self.entry_cell_rows

    def clear_all_columns(self):
        self.entry_cells_collection.clear()

    def clear_all_rows(self):
        self.entry_cell_rows.clear()

    def __hash__(self):
        return hash(self)