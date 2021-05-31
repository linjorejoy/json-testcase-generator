class OutputJsonFile:

    def __init__(self, file_name:str = None, variable_dictionary:dict={}, comment:str = ""):
        self.should_be_generated  = True
        self.file_name = file_name
        self.temp_file_name = file_name
        self.status = ""
        self.errors = ""
        self.comment = comment
        self.variable_dictionary = variable_dictionary