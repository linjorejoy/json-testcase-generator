import re

PATTERN = r"\$[^\s]*?\$"

def get_all_variables(string: str = None):
    
    if string is None or string == "":
        return None

    variables = list(set(re.findall(PATTERN, string)))
    variables.sort()

    return variables
    