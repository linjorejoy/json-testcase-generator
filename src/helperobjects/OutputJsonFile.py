import helpermodules.PreferencesJsonHandler as PreferencesJsonHandler
class OutputJsonFile:

    def __init__(self, file_name:str = None, variable_dictionary:dict={}, comment:str = ""):
        self.should_be_generated  = True
        self.file_name = file_name
        self.temp_file_name = file_name if file_name else "file_name"
        self.status = ""
        self.errors = ""
        self.comment = comment
        self.variable_dictionary = variable_dictionary

    def dictionary(self):
        dict_to_return = self.__dict__.copy()
        
        reportJsonType = PreferencesJsonHandler.get_data_from_settings("reportJsonType")

        if reportJsonType =="minimal":
            del(dict_to_return["status"])
            del(dict_to_return["errors"])
            del(dict_to_return["file_name"])
            del(dict_to_return["should_be_generated"])
            
        elif reportJsonType =="medium":
            del(dict_to_return["status"])
            del(dict_to_return["errors"])
            del(dict_to_return["file_name"])

        
        return dict_to_return