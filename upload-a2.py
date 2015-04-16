# Copies specified files from the local copy of the submit directory
# to the remote one
#
# assume format of remotepath is something like:
# /vol/submit/nwen241_2015T1/Assignment_1

def upload(studentname, localpath, remotepath, fname):
    # studentname is the username of the student 
    # localpath is the root of the assignment containing students
    # remotepath is localpath's counterpart on the remote machine
    # fname is the name of the file to upload
    #
    # assume that remote name include user@host:

    qualified_fname = os.sep+studentname+os.sep+"marking"+os.sep+fname
    local_fname = localpath+qualified_fname
    remote_fname = remotepath+qualified_fname

    # do the copying
    exec_list = ["scp", local_fname , remote_fname]
    subprocess.call(exec_list)

    # change the permissions
    #exec_list = ["ssh", "ian@circa.ecs.vuw.ac.nz", ""]
    return 
 
def copy_files(submitdir, fname):
    """ Loop through the student marking directory.

        Copy specified file to matching directory
        """
    all_students = os.listdir(submitdir)
    for student in all_students:
        upload(student, submitdir, \
            "ian@circa.ecs.vuw.ac.nz:/vol/submit/nwen241_2015T1/Assignment_1", \
            fname)

        
#TODO
#
# - will have separate program to copy results (safer this way)
# - changes
# - copy original results to user marking directory
# - create a summary of the results (calculate the score too)
#

if __name__ == "__main__":
    import os
    import re
    import subprocess 

    # Set the directory where the student submissions are found
    submitdir = '/home/ian/submit'
#    copy_files(submitdir,"marksheet")
#    copy_files(submitdir,"testresults")
    copy_files(submitdir,"test-script.txt")