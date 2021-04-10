from EntryCellCollection import EntryCellCollection
from EntryCellColumn import EntryCellColumn
from EntryCell import EntryCell
from OutputFiles import OutputFiles
from OutputJsonFile import OutputJsonFile
import GetAllCombinations
import FileNameGenerator

import json


cell11 = EntryCell(value="A")
cell12 = EntryCell(value="B")
cell13 = EntryCell(value="C")

cell21 = EntryCell(value=1)
cell22 = EntryCell(value=2)
cell23 = EntryCell(value=3)

cell31 = EntryCell(value="a")
cell32 = EntryCell(value="b")
cell33 = EntryCell(value="c")


entry_column1 = EntryCellColumn(variable_name="One")
entry_column1.add_cell(entry_cell=cell11)
entry_column1.add_cell(entry_cell=cell12)
entry_column1.add_cell(entry_cell=cell13)

entry_column2 = EntryCellColumn(variable_name="Two")
entry_column2.add_cell(entry_cell=cell21)
entry_column2.add_cell(entry_cell=cell22)
entry_column2.add_cell(entry_cell=cell23)

entry_column3 = EntryCellColumn(variable_name="Three")
entry_column3.add_cell(entry_cell=cell31)
entry_column3.add_cell(entry_cell=cell32)
entry_column3.add_cell(entry_cell=cell33)
entry_column3.add_cell(entry_cell=cell33)



entry_column4 = EntryCellColumn(variable_name="Four")
entry_column4.add_cell(entry_cell=cell21)
entry_column4.add_cell(entry_cell=cell22)
entry_column4.add_cell(entry_cell=cell23)

entry_collection = EntryCellCollection()
entry_collection.add_column(entry_column1)
entry_collection.add_column(entry_column2)
entry_collection.add_column(entry_column3)
entry_collection.add_column(entry_column4)





def to_dict(obj):
    return json.dumps(obj, default=lambda o: o.__dict__, indent=2)


if __name__ == '__main__':

    collections = GetAllCombinations.get_all_dictionaries(entry_collection)
    # print(to_dict(entry_collection))
    all_files = OutputFiles()

    [(
        all_files.add_output_json_file(OutputJsonFile(variable_dictionary=dictionary))
    ) for dictionary in collections]

    for fl in all_files.output_json_file_array:
        if fl.should_be_generated:
            print(fl.__dict__)

    ref_arr = [1, "-", 3, "_",-1, "AA",0, "_", 2, "", 4]
    variable_arr = ["One", "Two", "Three", "Four"]

    FileNameGenerator.generate_file_name(all_files, ref_arr, variable_arr)
    print("\n\nGenereated Names\n\n")
    
    for fl in all_files.output_json_file_array:
        if fl.should_be_generated:
            print(fl.__dict__)

