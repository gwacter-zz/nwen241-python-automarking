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
    fout.write('ASSIGNMENT 1: NWEN241 : 2015\n')
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
    fout.write("Name conventions: X /5.\n")
    fout.write("Commenting: Y /5.\n")
    fout.write("Semi colons: Z /5.\n") 
    fout.write("CODE STYLE MARK = X + Y + Z\n")
    fout.write("="*40+"\n")    
    fout.write("COMMENTS:\n")
    fout.write("Good:\n")
    fout.write("\n"*3)
    fout.write("Bad:\n")
    fout.write("\n"*3)
    fout.write("="*40+"\n")    
    fout.write("MARKING NOTES:")
    fout.write("\n")
    fout.write("CORRECTNESS: The marking for correctness is based upon\n"
        "running the automated tests.\n"
        "\n"
        "We will double-check cases where there are a large number of \n"
        "failures just in case there is a file encoding problem or similar \n"
        "but other problems will result in lost marks.\n"
        "\n"
        "There are different numbers of tests for each function so we have \n"
        "applied a weighting to the tests.\n"
        "\n"
        "CODE STYLE: The marking for the code style is based upon the \n"
        "conventions we asked you to use when completing this assignment:\n"
        "\n"
        "Naming conventions Follow these formats: function_name,\n"
        "function_parameter_name and local_var_name.\n"
        "\n"
        "- Use comments to document anything non-obvious.\n"
        "\n"
        "- Don't put commands on same line separated by semicolons.\n"
        "\n"
        "Generally a mark of 0 means you didn't follow the convention\n"
        "anywhere in the assignment, mark of 1 means you did it at least\n"
        "once, mark of 2 means you did it at least once in more than\n"
        "one function, mark of 3 means that you did it at least once in\n"
        "all functions, mark of 4 means that there was only one place\n"
        "where you didn't do it and mark of 5 meant no errors anywhere\n"
        "\n"
        "COMMENTS: You should receive some short comments highlighting\n"
        "something good and something bad about your solution. This might be\n"
        "stylistic or advice on problems to correct for next time. Where you\n"
        "have lost marks for say style we will tell you why.\n"
        "\n"
        "FINAL MARKS: We will calculate a final weighted mark that reflects\n"
        "a 90:10 ratio between marks for correctness and marks for style.")
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
