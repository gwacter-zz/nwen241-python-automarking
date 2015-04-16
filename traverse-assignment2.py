# Assumes that the student code have been copied to the student directory.
#
# Notes -- means that we assume that a new name for the
#          test cases has been applied.
#

def run_test(studentdir, testdir):
    # execute the test script
    # returns the actual results of running the tests
    #    as well as a useful summary of passes and fails
    
    # initialise the results structure
    result = dict()

    # change the current working directory to the one 
    # containing the student's work
    os.chdir(studentdir)
    print(os.getcwd())

    # construct line for execution of tests
    exec_list = ["python3", "-m", "doctest", "-v", \
       testdir+os.sep+"test-script.txt"]

    # execute the tests themselves and capture the results
    p = Popen(exec_list, stdout=PIPE)
    output, err = p.communicate()
    output_string = output.decode()

    # save the raw output
    result["raw"] = output_string

    # setup the dictionaries
    result["fail"] = OrderedDict()
    result["success"] = OrderedDict()
    result["max"] = dict()
    result["multiplier"] = dict()

    # parse the test output into separate tests
    for line in output_string.split('\n'):
        # 
        # test output used to configure this part
        # format:
        #    TEST: Name_of_test MAX: x MULTIPLIER: y
        #
        # here x defines the number of expected correct results
        #      y is a multiplier to be applied
        match = re.search('TEST: (.+) MAX: (\d+) MULTIPLIER: (\d+)"', line)
        if match:
           unit_test = match.group(1)
           result["fail"][unit_test] = 0
           result["success"][unit_test] = 0
           result["max"][unit_test] = int(match.group(2))
           result["multiplier"][unit_test] = int(match.group(3))
        if re.search("^ok$",line):
            result["success"][unit_test] = result["success"][unit_test]+1
        elif re.search("^Failed example:$",line):
            result["fail"][unit_test] = result["fail"][unit_test]+1 

    return result
 
def write_marksheet(student_id, student_name, test_results):

    print("WRITING "+student_id+" "+student_name)
    fout = open("marking"+os.sep+"marksheet","w")
    fout.write('='*40+'\n')
    fout.write('ASSIGNMENT 2: NWEN241 : 2015\n')
    fout.write("\n")
    fout.write("Student ID:" + student_id + '\n')
    fout.write("Student Name:" + student_name + '\n')
    fout.write('='*40+'\n')
    fout.write("CORRECTNESS:\n")

    # maximum number of marks to be gained is "max"
    # each failure reduces this by one (with a min of zero)
    raw_output = test_results["raw"]
    failures = test_results["fail"]
    successes = test_results["success"]
    num_tests = test_results["max"]
    multipliers = test_results["multiplier"]
    total = 0

    for each_test in failures:
        mark = max(0, num_tests[each_test] - failures[each_test])
        weight = multipliers[each_test]
        score = mark * weight
        total = total + score
        fout.write("{0}: passed {1}/{4} cases, x {2} = {3}.\n".format(\
           each_test, mark, weight, score, num_tests[each_test]))
    fout.write("CORRECTNESS MARK = {0}\n".format(total))
    fout.write("="*40+"\n")
    fout.write("CODE STYLE:\n")

# MAKE THIS EASIER TO MARK!!!!

    fout.write("Name conventions:  /5.\n")
    fout.write("Commenting: Y /5.\n")
    fout.write("Semi colons: Z /5.\n") 
    fout.write("Parentheses: \n")
    fout.write("Whitespace: \n")
    fout.write("Classes: \n")
    fout.write("Strings: \n")
    fout.write("Imports: \n")
    fout.write("CODE STYLE MARK = X + Y + Z\n")
    fout.write("="*40+"\n")    
    fout.write("COMMENTS:\n")
    fout.write("\n")
    fout.write("="*40+"\n")    
    fout.close()

    print("WRITING "+student_id+" "+student_name + " raw_output")
    fout = open("marking"+os.sep+"testresults","w")    
    fout.write(raw_output)
    fout.close()

def process_student(fname):
    """
    Argument:

    fname -- userInfo.xml file

    Returns the student name and ID
    """
    f = open(fname)
    data = f.read()
    # get the student ID and name
    student_id = ""
    student_name = ""
    match = re.search("<ID>(\d+)</ID>",data)
    match1 = re.search("<Name>(.+)</Name>",data)
    if match != None:
        student_id = match.group(1)
        student_name = match1.group(1)
    f.close()  
    return student_id, student_name

def mark_students(submitdir, testdir):
    """ Loop through the student marking directory.

        Extract the student details and execute their
        code against the test script.
        """
    all_students = os.listdir(submitdir)
    for student in all_students:
        # construct the path to the individual student's submission
        studentdir = submitdir + os.sep + student + os.sep
        student_xml = studentdir + "marking" + os.sep + "userInfo.xml"

        # extract the student details
        student_id, student_name = process_student(student_xml)
        
        # run the tests agains the student submission
        results = run_test(studentdir, testdir)

        # write a marksheet for each student
        write_marksheet(student_id, student_name, results)

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
    from subprocess import Popen, PIPE
    from collections import OrderedDict

    # Set the directory where the student submissions are found
    submitdir = '/home/ian/submit'
    # Assume the tests are found in the current directory
    testdir = os.getcwd()
    mark_students(submitdir, testdir)
