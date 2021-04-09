class OutputJsonFile:

    def __init__(self, file_name:str = None, json_data:dict = None):
        self.should_be_generated  = True
        self.file_name = file_name
        self.json = json_data
        self.variable_dictionary = {}