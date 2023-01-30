import os

"""

paths to your text-docs
!do not rename keys!

"""

path = '\\'.join(os.path.abspath(__file__).split('\\')[:-3])

dictpaths = {
    'restore': f"{path}\\src\\etc\\docs\\restore_tables.txt",

    'dbconfig': f"{path}\\dbsettings.txt",

    'templates': f"{path}\\src\\etc\\docs\\templates.txt",

    'token': f"{path}\\token.txt",

    'tables': f"{path}\\src\\etc\\docs\\tables.txt",

    "statements": f"{path}\\src\\etc\\docs\\statements",
    
    "statements_en": f"{path}\\src\\etc\\docs\\statements\\en.txt"
}
