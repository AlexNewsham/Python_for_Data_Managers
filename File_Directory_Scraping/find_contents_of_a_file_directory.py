import os
from pathlib import Path

#directory (replace 'C:/MyFilePath' with your directory mapping)
dir = 'C:/MyFilePath'

#set the basepath variable for the loop through
basepath = Path(dir)

#print, loop and output
print(str("FILES FOUND IN THE FILE DIRECTORY " + dir + ' ARE AS FOLLOWS:'))
files_in_basepath = basepath.iterdir()
for item in files_in_basepath:
    if item.is_file():
        print(item.name)