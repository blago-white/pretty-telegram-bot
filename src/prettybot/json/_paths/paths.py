import os

"""

paths to your text-docs
!do not rename keys!

"""

path = os.path.abspath(__file__).split('\\')
path = '\\'.join(path[:path.index('src')])

dictpaths = {
    'dbconfig': f"{path}\\dbsettings.txt",
    'token': f"{path}\\token.txt"
}
