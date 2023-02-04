import os

"""

paths to your text-docs
!do not rename keys!

"""

path = '\\'.join(os.path.abspath(__file__).split('\\')[:-3])

dictpaths = {
    'restore': f"{path}\\src\\conf\\docs\\restore_tables.txt",

    'dbconfig': f"{path}\\dbsettings.txt",

    'templates': f"{path}\\src\\conf\\docs\\templates.txt",

    'token': f"{path}\\token.txt",

    'tables': f"{path}\\src\\conf\\docs\\tables.txt",
}
