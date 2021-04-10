from tkinter import Tk, Frame, filedialog, LabelFrame, Scrollbar
from tkinter import Text, Button, Label, Entry
from tkinter import ttk
from tkinter import RIGHT, LEFT, END, TOP
from tkinter import X, Y, N, WORD
import json
from functools import partial

from EntryCellCollection import EntryCellCollection
from EntryCellColumn import EntryCellColumn
from EntryCell import EntryCell
from OutputFiles import OutputFiles
from OutputJsonFile import OutputJsonFile

import ProcessData

"""

my_notebook.select(get_data_frame)
"""

TEMPLATE_JSON_FILE = ""
JSON_STR = ""
JSON_STR_TO_PRINT = ""
VARIABLES_PRESENT = []


WINDOW_HEIGHT = 650
WINDOW_WIDTH = 800



    

def main():

    def add_cell(entry_col: EntryCellColumn, index:int):
        # print("Index : ",index)
        this_cell = EntryCell()
        yindex = entry_col.add_cell(this_cell)
        this_entry = Entry(processdata_wrapper_body, width=10)
        this_entry.grid(row=(yindex+2), column=(index + 1), pady=1, padx=8)
        this_cell.entry = this_entry
        

    def select_file():
        global TEMPLATE_JSON_FILE
        global JSON_STR
        global VARIABLES_PRESENT
        filename = filedialog.askopenfilename(initialdir = "E:/my_works/programming/python/JSON_Test_Case_Generator/For testing",
                                            title = "Select a File",
                                                filetypes = (
                                                    ("JSON files","*.json*"),    
                                                    ("all files","*.*")
                                                )
                                            )
        
        TEMPLATE_JSON_FILE = filename
        with open(TEMPLATE_JSON_FILE, mode="r") as json_file:
            json_data = json.load(json_file)
            JSON_STR_TO_PRINT = json.dumps(json_data, indent=2)
            JSON_STR = json.dumps(json_data)
            VARIABLES_PRESENT = ProcessData.get_all_variables(JSON_STR)
            



        json_string_label.delete("1.0",END)
        json_string_label.insert(END, JSON_STR_TO_PRINT)
        json_string_label.config(state="disabled")
        file_name_label.configure(text=TEMPLATE_JSON_FILE)
        entry_cell_collection = EntryCellCollection()

        table_start_row = 1

        for index, variable in enumerate(VARIABLES_PRESENT):
            this_var_entry_col = EntryCellColumn(variable_name=variable)
            this_var_entry_col_cell = EntryCell()
            this_var_entry_col.add_cell(entry_cell = this_var_entry_col_cell)
            this_var_entry_col.add_cell(entry_cell = this_var_entry_col_cell)
            entry_cell_collection.add_column(this_var_entry_col)

            processdata_wrapper_body.config(height=580)
            column_index = index
            # print("Column Index : ", column_index)
            this_processdata_variable_add_cell_button = Button(processdata_wrapper_body, text="Add cell", command=partial(add_cell, this_var_entry_col, column_index))
            this_processdata_variable_add_cell_button.grid(row=0, column=(index+1), pady=2, padx=8)

            this_processdata_variable_header = Label(processdata_wrapper_body, width="10", text=variable, font=("bold", 12))
            this_processdata_variable_header.grid(row=table_start_row, column=(index+1), pady=2, padx=8)

            for yindex, cell in enumerate(this_var_entry_col.entry_cell_column):
                this_entry = Entry(processdata_wrapper_body, width=10)
                this_entry.grid(row=(yindex+table_start_row+1), column=(index+1), pady=1, padx=8)
                cell.entry = this_entry

        processdata_wrapper_col1_label = Label(processdata_wrapper_body, text="Fill the variations here", font=("bold", 12))
        processdata_wrapper_col1_label.grid(row=1, column=0, pady=2, padx=8)


    root = Tk()
    root.title("JSON Testcase Creator v0.0.1")
    root.geometry("1000x650")

    # Notebook
    my_notebook = ttk.Notebook(master=root)
    my_notebook.pack(pady="6")







    # Get Data Frame
    get_data_frame = Frame(my_notebook, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)


    getdata_wrapper_top = LabelFrame(get_data_frame, text="Upload", height="50")

    upload_file_label = Label(getdata_wrapper_top, width=30, text="Please Upload the JSON Template File : ", font=("bold", 10))
    upload_file_label.place(x=250,y=0)

    # Upload File
    select_file_button = Button(getdata_wrapper_top, text="Select File", command=select_file, width=20)
    select_file_button.place(x=500,y=0)

    file_name_label = Label(getdata_wrapper_top, text=TEMPLATE_JSON_FILE, font=("bold", 6))
    file_name_label.place(x=700)
    getdata_wrapper_top.pack(fill="both", expand="yes")



    getdata_wrapper_body = LabelFrame(get_data_frame, text="File", height="580")

    getdata_vertical_scroll = Scrollbar(getdata_wrapper_body, orient="vertical")

    getdata_vertical_scroll.pack(side=RIGHT, fill=Y)

    json_str = "Please Select a JSON File"

    json_string_label = Text(getdata_wrapper_body, width=200, height=200, wrap=WORD, yscrollcommand=getdata_vertical_scroll.set)
    json_string_label.insert(END, json_str)
    json_string_label.pack(side=TOP, fill=X)
    
    getdata_vertical_scroll.config(command=json_string_label.yview)
    getdata_wrapper_body.pack(fill="both", expand="yes")






    # Process Data Frame

    process_data_frame = Frame(my_notebook, width=1000, height=650)

    VARIABLES_PRESENT = []

    processdata_wapper_top = LabelFrame(process_data_frame, text="Head", height="50")





    processdata_wapper_top.pack(fill="both", expand=N)

    processdata_wrapper_body = LabelFrame(process_data_frame, text="Body", height="500")



    processdata_wrapper_body.pack(fill="both", expand=Y)

    processdata_wrapper_footer = LabelFrame(process_data_frame, text="Options", height="50")


    processdata_wrapper_footer.pack(fill="both", expand=N)








    # Preview Outputs Frame


    preview_data_frame = Frame(my_notebook, width=1000, height=650)










    # Generate Status Frame

    generate_data_frame = Frame(my_notebook, width=1000, height=650)




    # Pack Frames
    get_data_frame.pack(fill="both", expand=1)
    process_data_frame.pack(fill="both", expand=1)
    preview_data_frame.pack(fill="both", expand=1)
    generate_data_frame.pack(fill="both", expand=1)

    # adding tabs

    my_notebook.add(get_data_frame, text="Get Data")
    my_notebook.add(process_data_frame, text="Process Data")
    my_notebook.add(preview_data_frame, text="Preview Data")
    my_notebook.add(generate_data_frame, text="Generate Data")

    root.mainloop()



if __name__ == '__main__':
    main()

