from tkinter import Tk, Frame, filedialog, LabelFrame, Scrollbar
from tkinter import Text, Button, Label
from tkinter import ttk
from tkinter import RIGHT, LEFT, END, TOP
from tkinter import X, Y, N, WORD
import json


"""

my_notebook.select(get_data_frame)
"""

TEMPLATE_JSON_FILE = ""
JSON_STR = ""
JSON_STR_TO_PRINT = ""
WINDOW_HEIGHT = 650
WINDOW_WIDTH = 800



    

def main():

    def select_file():
        global TEMPLATE_JSON_FILE
        global JSON_STR
        filename = filedialog.askopenfilename(initialdir = "E:/my_works/programming/python/JSON_Test_Case_Generator",
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

        json_string_label.delete("1.0",END)
        json_string_label.insert(END, JSON_STR_TO_PRINT)
        json_string_label.config(state="disabled")
        file_name_label.configure(text=TEMPLATE_JSON_FILE)


    root = Tk()
    root.title("JSON Testcase Creator v0.0.1")
    root.geometry("1000x650")

    # Notebook
    my_notebook = ttk.Notebook(master=root)
    my_notebook.pack(pady="6")







    # Get Data Frame
    get_data_frame = Frame(my_notebook, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)


    wrapper_top = LabelFrame(get_data_frame, text="Upload", height="50")

    upload_file_label = Label(wrapper_top, width=30, text="Please Upload the JSON Template File : ", font=("bold", 10))
    upload_file_label.place(x=250,y=0)

    # Upload File
    select_file_button = Button(wrapper_top, text="Select File", command=select_file, width=20)
    select_file_button.place(x=500,y=0)

    file_name_label = Label(wrapper_top, text=TEMPLATE_JSON_FILE, font=("bold", 6))
    file_name_label.place(x=700)
    wrapper_top.pack(fill="both", expand="yes")



    wrapper_body = LabelFrame(get_data_frame, text="File", height="580")

    vertical_scroll = Scrollbar(wrapper_body, orient="vertical")

    vertical_scroll.pack(side=RIGHT, fill=Y)

    json_str = "Please Select a JSON File"

    json_string_label = Text(wrapper_body, width=200, height=200, wrap=WORD, yscrollcommand=vertical_scroll.set)
    json_string_label.insert(END, json_str)
    json_string_label.pack(side=TOP, fill=X)
    
    vertical_scroll.config(command=json_string_label.yview)
    wrapper_body.pack(fill="both", expand="yes")






    # Process Data Frame

    process_data_frame = Frame(my_notebook, width=1000, height=650)

    








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

