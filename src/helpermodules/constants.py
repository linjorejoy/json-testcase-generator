
# Application requirements

CURRENT_VERSION = "V0.0.7"
ICON = "src/resources/favicon-32x32.ico"

# Initialzation

SCREEN_RATIO = 0.75

# Global requirements


FONTS = {
    "LARGE_FONT":{'font':{'family':"monospace", 'size':20, 'weight':'bold'}},
    "BUTTON_FONT":{'font':{'family':"monospace", 'size':10, 'weight':'bold'}},
    "LABEL_FONT":{'font':{'size':10, 'weight':'bold'}},
    "DEFAULT_TEXT_FONT":{'font':{'family':"Comic Sans MS", 'size':10, 'weight':'bold'}},
    "JSON_DATA_PREVIEW":{'font':{'family':"monospace", 'size':10, 'weight':'bold'}}
}

# Widget requirements

# Button

def default_func():
    print("Assign command to this button")

DEF_BUTTON_TEXT ="Button"
DEF_BUTTON_WIDTH = 25
DEF_BUTTON_FUNC = default_func

#  LabelFrame

DEF_LABELFRAME_TEXT = "Wrapper"
DEF_LABELFRAME_HEIGHT = "50"
DEF_LABELFRAME_EXPAND = "yes"
DEF_LABELFRAME_FILL = "both"

# Label
DEF_LABEL_TEXT = "Enter Something"


# Text
DEF_TEXT_TEXT = "Type Here"


# Upload Part

JSON_PREVIEW_INDENT=2
ACCEPTABLE_FILE_TYPES = (
    ("JSON files","*.json*"),
    ("all files","*.*")
)





