# first, get it to find (in this case: assignment1.py)
# second, print out the location (including the dirname)
# ---- assume that the code to run is not in marking btw

# Import the os module, for the os.walk function
import os
 
# Set the directory you want to start from
rootDir = '/home/ian/marking'
for dirName, subdirList, fileList in os.walk(rootDir):
    for fname in fileList:
        if fname == "assignment1.py":
        	print("{0}/{1}/{2}".format(dirName,subdirList,fname))