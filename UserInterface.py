from tkinter import Tk, Frame, filedialog, LabelFrame, Scrollbar, OptionMenu, Checkbutton, Canvas
from tkinter import Text, Button, Label, Entry
from tkinter import IntVar, StringVar
from tkinter import ttk
from tkinter.ttk import Combobox, Treeview, Progressbar
from tkinter import RIGHT, LEFT, END, BOTH, TOP, SE, W, BOTTOM, HORIZONTAL, VERTICAL
from tkinter import X, Y, N, WORD
import json
import os
from functools import partial

from EntryCellCollection import EntryCellCollection
from EntryCellColumn import EntryCellColumn
from EntryCell import EntryCell
from OutputFiles import OutputFiles
from OutputJsonFile import OutputJsonFile

import ProcessData
import GetAllCombinations
import FileNameGenerator
import GenerateFile

"""

my_notebook.select(get_data_frame)
"""

TEMPLATE_JSON_FILE = ""
json_data = {}
JSON_STR = ""
JSON_STR_TO_PRINT = ""
VARIABLES_PRESENT = []
entry_cell_collection = None
output_files = OutputFiles()
reference_arr_for_name_gen = []

WINDOW_HEIGHT = 650
WINDOW_WIDTH = 800



    

def to_dict(obj):
    return json.dumps(obj, default=lambda o: o.__dict__, indent=2)

def main():
    global VARIABLES_PRESENT

    def generate_files():
        my_notebook.select(4)
        global json_data
        output_location = "E:/my_works/programming/python/JSON_Test_Case_Generator/For testing/Output"
        total_length = 300
        progress_bar = Progressbar(generate_file_wrapper_progress, orient="horizontal", length=total_length)
        progress_bar.pack(pady=10)

        num_files = output_files.count
        progress_jump = int(total_length // num_files)

        for json_file_obj in output_files.get_output_json_file_array():
            generated_files_text.config(state="normal")
            generated_files_text.insert(END, f"\n{json_file_obj.file_name:>50}............Creating")
            generated_files_text.config(state="disabled")
            GenerateFile.generate_one_file(json_file_obj, json_data, output_location)
            progress_bar['value'] += progress_jump
            generated_files_text.config(state="normal")
            generated_files_text.insert(END, f"\n{json_file_obj.file_name:>50}............Done")
            generated_files_text.config(state="disabled")

        
    def preview_all_files():
        global reference_arr_for_name_gen
        my_notebook.select(3)
        FileNameGenerator.generate_file_name(output_files, reference_arr_for_name_gen)
        for widget in preview_wrapper_body.winfo_children():
            widget.destroy()
        
        preview_tree_scroll_frame = Frame(preview_wrapper_body)
        preview_tree_scroll_frame.pack(pady=20)

        preview_tree_scrollbar_y = Scrollbar(preview_tree_scroll_frame, orient='vertical')
        preview_tree_scrollbar_y.pack(side=RIGHT, fill=Y)

        preview_tree_scrollbar_x = Scrollbar(preview_tree_scroll_frame, orient='horizontal')
        preview_tree_scrollbar_x.pack(side=BOTTOM, fill="x")

        preview_tree = Treeview(preview_tree_scroll_frame,yscrollcommand=preview_tree_scrollbar_y.set, xscrollcommand=preview_tree_scrollbar_x)

        preview_tree_scrollbar_y.config(command=preview_tree.yview)
        preview_tree_scrollbar_x.config(command=preview_tree.xview)

        preview_tree_variables = ["File Name", *VARIABLES_PRESENT]

        # Columns
        preview_tree['columns'] = tuple(preview_tree_variables)

        # Format Column

        preview_tree.column("#0", width=60, minwidth=45)
        for var in preview_tree_variables:
            preview_tree.column(var, width=200, anchor=W, minwidth=45)

        # Headings
        preview_tree.heading("#0", text="Count", anchor=W)
        for var in preview_tree_variables:
            preview_tree.heading(var, text=var.title(), anchor=W)

        for index, json_file_obj in enumerate(output_files.get_output_json_file_array()):
            vales_to_add_list = [json_file_obj.file_name, *json_file_obj.variable_dictionary.values()]
            vales_to_add_tuple = tuple(vales_to_add_list)
            preview_tree.insert(parent='', index="end", iid=index, text=(index+1), values=vales_to_add_tuple)
            
        preview_tree.pack()

        # preview_wrapper_footer
        generate_json_files_button = Button(preview_wrapper_footer, text="Generate All Files", command=generate_files)
        generate_json_files_button.place(rely=1.0, relx=1.0, x=-5, y=-5, anchor=SE)


    def set_name_page():
        global reference_arr_for_name_gen
        global VARIABLES_PRESENT
        veriables_for_dropdown = VARIABLES_PRESENT.copy()
        veriables_for_dropdown.append("Counter")
        # filename_generator_frame
        entry_0 = Entry(filename_generator_wrapper_body, width=10)
        entry_0.grid(row=0, column=0)
        reference_arr_for_name_gen.append(entry_0)

        for index in range(len(veriables_for_dropdown)):

            if not veriables_for_dropdown:
                veriables_for_dropdown = [""]

            this_dropdown_var = StringVar()
            this_dropdown_var.set(None)
            this_dropdown = OptionMenu(filename_generator_wrapper_body, this_dropdown_var, *veriables_for_dropdown)
            this_dropdown.grid(row=0, column=(2*index + 1))
            reference_arr_for_name_gen.append(this_dropdown_var)

            entry_n = Entry(filename_generator_wrapper_body, width=10)
            entry_n.grid(row=0, column=(2*index + 2))
            reference_arr_for_name_gen.append(entry_n)
            
        goto_preview_button = Button(filename_generator_wrapper_footer,text="Preview All Files", command=preview_all_files)
        goto_preview_button.place(rely=1.0, relx=1.0, x=-5, y=-5, anchor=SE)


    def generate_output_file_obj():
        global entry_cell_collection
        global output_files

        for column in entry_cell_collection.entry_cells_collection:
            # print("column : ", column.variable_name)
            for cell in column.entry_cell_column:
                cell.value = cell.entry.get()
                cell.entry = None

                # print(cell.value, type(cell.value))
        all_combinations = GetAllCombinations.get_all_dictionaries(entry_cell_collection)

        [(
            output_files.add_output_json_file(OutputJsonFile(variable_dictionary=combination))
        ) for combination in all_combinations]

        my_notebook.select(2)
        set_name_page()


    def add_cell(entry_col: EntryCellColumn, index:int):
        
        this_cell = EntryCell()
        yindex = entry_col.add_cell(this_cell)
        this_entry = Entry(processdata_subframe, width=10)
        this_entry.grid(row=(yindex+2), column=(index + 1), pady=1, padx=8)
        this_cell.entry = this_entry

        # processdata_wrapper_body_canvas.config(scrollregion=processdata_subframe.bbox())
        # processdata_wrapper_body_canvas.bind(
        #         '<Configure>',
        #         lambda e : processdata_wrapper_body_canvas.configure(
        #             scrollregion = processdata_wrapper_body_canvas.bbox("all")
        #         )
        #     )
        

        # processdata_wrapper_body_canvas.create_window(
        #     (0, 0),
        #     window = processdata_subframe,
        #     anchor = "nw"
        # )

    def select_file():
        global TEMPLATE_JSON_FILE
        global JSON_STR
        global VARIABLES_PRESENT
        global entry_cell_collection
        global json_data
        current_dir = os.curdir
        filename = filedialog.askopenfilename(initialdir = current_dir,
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
            entry_cell_collection.add_column(this_var_entry_col)

            # processdata_wrapper_body.config(height=580)
            column_index = index
            # print("Column Index : ", column_index)
            this_processdata_variable_add_cell_button = Button(processdata_subframe, text="Add cell", command=partial(add_cell, this_var_entry_col, column_index))
            this_processdata_variable_add_cell_button.grid(row=0, column=(index+1), pady=2, padx=3)

            this_processdata_variable_header = Label(processdata_subframe, width="10", text=variable, font=("bold", 12))
            this_processdata_variable_header.grid(row=table_start_row, column=(index+1), pady=2, padx=3)

            for yindex, cell in enumerate(this_var_entry_col.entry_cell_column):
                this_entry = Entry(processdata_subframe, width=10)
                this_entry.grid(row=(yindex+table_start_row+1), column=(index+1), pady=1, padx=3)
                cell.entry = this_entry
        # [(
        #     [print("\t",cell," : ", cell.value, " : ", cell.entry.get()) for cell in cell_column.entry_cell_column]
        # ) for cell_column in entry_cell_collection.entry_cells_collection]
        # print(to_dict(entry_cell_collection))

        processdata_wrapper_col1_label = Label(processdata_subframe, text="Fill the variations here", font=("bold", 12))
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

    # Frame
    processdata_wrapper_body = LabelFrame(process_data_frame, text="Body")
    processdata_wrapper_body.pack(fill="both", expand=1)

    # Canvas
    processdata_wrapper_body_canvas = Canvas(processdata_wrapper_body)
    processdata_wrapper_body_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    # Scrollbar

    processdata_wrapper_body_canvas_y = ttk.Scrollbar(
        processdata_wrapper_body,
        orient="vertical",
        command=processdata_wrapper_body_canvas.yview
    )
    processdata_wrapper_body_canvas_y.pack(side=RIGHT, fill=Y)


    processdata_wrapper_body_canvas_x = ttk.Scrollbar(
        processdata_wrapper_body,
        orient="horizontal",
        command=processdata_wrapper_body_canvas.xview
    )
    processdata_wrapper_body_canvas_x.pack(side=BOTTOM, fill='x')

    # Configure Scroll Bar
    processdata_wrapper_body_canvas.configure(
        yscrollcommand=processdata_wrapper_body_canvas_y.set,
        xscrollcommand=processdata_wrapper_body_canvas_x.set
    )


    processdata_wrapper_body_canvas.bind(
        '<Configure>',
        lambda e : processdata_wrapper_body_canvas.configure(
            scrollregion = processdata_wrapper_body_canvas.bbox("all")
        )
    )
    
    # New frame inside Canvas

    processdata_subframe = Frame(processdata_wrapper_body_canvas)


    # Add new frame to window of canvas

    processdata_wrapper_body_canvas.create_window(
        (0, 0),
        window = processdata_subframe,
        anchor = "nw"
    )
    # for j in range(20):
    #     for i in range(10):
    #         Button(processdata_subframe, text=f"Button {j}{i}").grid(row = i, column = j, pady=20, padx=15)


    processdata_wrapper_footer = LabelFrame(process_data_frame, text="Options", height="50")

    goto_filename_button = Button(processdata_wrapper_footer, text="Set Names", command=generate_output_file_obj)

    goto_filename_button.place(rely=1.0, relx=1.0, x=-5, y=-5, anchor=SE)

    processdata_wrapper_footer.pack(fill="both", expand=N)






    # File Name specifier Frame


    filename_generator_frame = Frame(my_notebook, width=1000, height=650)

    filename_generator_wrapper_body = LabelFrame(filename_generator_frame, text="Body", height="560")
    filename_generator_wrapper_body.pack(fill="both", expand=Y)

    filename_generator_wrapper_footer = LabelFrame(filename_generator_frame, text="Options", height="50")

    filename_generator_wrapper_footer.pack(fill="both", expand=N)

    

    # Preview Outputs Frame


    preview_data_frame = Frame(my_notebook, width=1000, height=650)


    preview_wrapper_head = LabelFrame(preview_data_frame, text="Head", height="50")

    preview_wrapper_head.pack(fill="both", expand=N)

    preview_wrapper_body = LabelFrame(preview_data_frame, text="Body", height="560")


    preview_wrapper_body.pack(fill="both", expand=Y)


    preview_wrapper_footer = LabelFrame(preview_data_frame, text="Options", height="50")

    preview_wrapper_footer.pack(fill="both", expand=N)





    # Generate Status Frame

    generate_file_frame = Frame(my_notebook, width=1000, height=650)

    generate_file_wrapper_progress = LabelFrame(generate_file_frame, text="Progree", height="75")

    generate_file_wrapper_progress.pack(fill="both", expand=N)

    
    
    generate_file_wrapper_status = LabelFrame(generate_file_frame, text="Status", height="500")

    generated_files_text_scroll_y = Scrollbar(generate_file_wrapper_status, orient="vertical")
    generated_files_text_scroll_y.pack(side=RIGHT, fill=Y)

    generated_files_text = Text(generate_file_wrapper_status, width=200, height=200, wrap=WORD, yscrollcommand=generated_files_text_scroll_y.set)

    generated_files_text.insert(END, "Generating JSON Files....")
    generated_files_text.pack(side=TOP, fill=X)
    

    generated_files_text_scroll_y.config(command=generated_files_text.yview)
    generate_file_wrapper_status.pack(fill="both", expand=Y)



    # Pack Frames
    get_data_frame.pack(fill="both", expand=1)
    process_data_frame.pack(fill="both", expand=1)
    filename_generator_frame.pack(fill="both", expand=1)
    preview_data_frame.pack(fill="both", expand=1)
    generate_file_frame.pack(fill="both", expand=1)

    # adding tabs

    my_notebook.add(get_data_frame, text="Get Data")
    my_notebook.add(process_data_frame, text="Process Data")
    my_notebook.add(filename_generator_frame, text="File Name")
    my_notebook.add(preview_data_frame, text="Preview Data")
    my_notebook.add(generate_file_frame, text="Generate Data")

    root.mainloop()



if __name__ == '__main__':
    main()

