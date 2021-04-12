class OutputJsonFile:

    def __init__(self, file_name:str = None, variable_dictionary:dict={}):
        self.should_be_generated  = True
        self.file_name = file_name
        self.variable_dictionary = variable_dictionary