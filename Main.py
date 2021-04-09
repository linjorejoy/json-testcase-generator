from EntryCellCollection import EntryCellCollection
from EntryCellColumn import EntryCellColumn
from EntryCell import EntryCell
import GetAllCombinations

import json


cell11 = EntryCell("One", "A")
cell12 = EntryCell("One", "B")
cell13 = EntryCell("One", "C")

cell21 = EntryCell("Two", 1)
cell22 = EntryCell("Two", 2)
cell23 = EntryCell("Two", 3)

cell31 = EntryCell("Three", "a")
cell32 = EntryCell("Three", "b")
cell33 = EntryCell("Three", "c")


entry_column1 = EntryCellColumn()
entry_column1.add_cell(entry_cell=cell11)
entry_column1.add_cell(entry_cell=cell12)
entry_column1.add_cell(entry_cell=cell13)

entry_column2 = EntryCellColumn()
entry_column2.add_cell(entry_cell=cell21)
entry_column2.add_cell(entry_cell=cell22)
entry_column2.add_cell(entry_cell=cell23)

entry_column3 = EntryCellColumn()
entry_column3.add_cell(entry_cell=cell31)
entry_column3.add_cell(entry_cell=cell32)
entry_column3.add_cell(entry_cell=cell33)

entry_collection = EntryCellCollection()
entry_collection.add_column(entry_column1)
entry_collection.add_column(entry_column2)
entry_collection.add_column(entry_column3)



def to_dict(obj):
    return json.dumps(obj, default=lambda o: o.__dict__, indent=2)

d = {
    "One": "oneee",
    "Two": "Twooo",
    "Three": "Threeee"
}

if __name__ == '__main__':
    # print(to_dict(entry_collection))
    collections = GetAllCombinations.get_all_dictionaries2(d,entry_collection)
    [print(dictionary, type(dictionary)) for dictionary in collections]

