import os

"""

paths to your text-docs
!do not rename keys!

"""

path = '\\'.join(os.path.abspath(__file__).split('\\')[:-4])

dictpaths = {
    'dbconfig': f"{path}\\dbsettings.txt",

    'token': f"{path}\\token.txt"
}
