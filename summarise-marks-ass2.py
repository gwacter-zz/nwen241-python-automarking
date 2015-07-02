# Loops thruough the submission directory and returns values
def extract_marks(studentdir):
    # change the current working directory to the one 
    # containing the student's work
    os.chdir(studentdir)

    print(studentdir, ",", end="")
    
    # open the markshee in the directory
    try:
        mfile = open("marksheet")
        minfo = mfile.read()
        mfile.close()
    except IOError:
        print("I/O error")
        return

    # extract STUDENT ID:
    # extract CORRECTNESS MARK
    # extract COE STYLE MARK =
    import re
    m1 = re.search("ID:(.+)",minfo)
    if m1:
       print(m1.group(1) + ",", end="")
    else:
        print("null,", end="")

    m2 = re.search("TOTAL = (.+) out",minfo)
    if m2:
       print(m2.group(1) + ",",end="")
    else:
        print("null", end="")
        
    m3 = re.search("GRADE (.+)",minfo)
    m4 = re.search("GRADE: (.+)",minfo)
    if m3:
        print(m3.group(1))
    elif m4:
        print(m4.group(1))
    else:
        print("null")

    return
 
def mark_students(submitdir):
    """ Loop through the student marking directory.
        """
    all_students = os.listdir(submitdir)
    all_students.remove("copyToMarking")
    for student in all_students:
            
        # construct the path to the individual student's submission
        studentdir = submitdir + os.sep + student + os.sep + "marking" + os.sep

        # extract the results
        extract_marks(studentdir)

if __name__ == "__main__":
    import os
    import re
    from subprocess import Popen, PIPE
    from collections import OrderedDict

    # Set the directory where the student submissions are found
    submitdir = '/vol/submit/nwen241_2015T1/Assignment_2'
    # Assume the tests are found in the current directory
    testdir = os.getcwd()
    mark_students(submitdir)
