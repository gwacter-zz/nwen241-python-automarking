def run_test():
    from subprocess import Popen, PIPE

    p = Popen(["ls", "-1"], stdout=PIPE)
    output, err = p.communicate()
    print("="*40)
    print(output.decode(), end='')
    print("="*40)

def walk_submissions():
    # first, get it to find (in this case: assignment1.py)
    # second, print out the location (including the dirname)
    # ---- assume that the code to run is not in marking btw

    # assumes that have copied the assignment file to makring 
    # subdirectory and that the output from running the marking
    # scriptt will also be placed there

    # Import the os module, for the os.walk function
    import os

    # Set the directory you want to start from
    rootDir = '/home/ian/submit'
    for dirpath, dirnames, fileList in os.walk(rootDir):
        for fname in fileList:
            if fname == "assignment1.py":
                if "marking" in dirpath:
        	        print("{0}/{1}".format(dirpath,fname))

    run_test()

# TODO
#
# - will have separate program to copy results (safer this way)
# - test script is assumed to be in the current directory
# - copy original results to user marking directory
# - create a summary of the results (calculate the score too)

if __name__ == "__main__":
    walk_submissions()