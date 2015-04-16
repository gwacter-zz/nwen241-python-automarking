def add_vectors(vector_1, vector_2):
    """Returns a list object representing the result of adding two vectors together.

       Arguments:
       vector_1 -- list representing first vector
       vector_2 -- list representing second vector

       Error checking:
       Both arguments must be of type list.
       Both vectors must of the same length.
       Only vector elements of type int can be added together.
    """
      
    # variable used to determine if argument is in error
    bad_parameter = False

    # check that the argument types are compatible
    if not isinstance(vector_1,list):
        print("Error: first argument is not a list")
        bad_parameter = True

    if not isinstance(vector_2,list):
        print("Error: second argument is not a list")
        bad_parameter = True

    if bad_parameter:
        return None

    # check that the vectors are of the same size
    if len(vector_1) != len(vector_2):
        print("Error: lengths of the two vectors are different")
        return None

    # add the two vectors together
    vector_3 = []
    for index, val_vector_1 in enumerate(vector_1):
       val_vector_2 = vector_2[index]
       if isinstance(val_vector_1, int) and isinstance(val_vector_2, int):
          vector_3.append(val_vector_1 + val_vector_2)
       else:
          print("Error: attempted to add incompatible {0} to {1}".format(val_vector_1, val_vector_2))
          return None

    return vector_3

def print_frequency(some_text):
    """Prints a table of letter frequencies within a string. 

       Non-letter characters are ignored.
       Table is sorted alphabetically.
       Letter case is ignored.
       Two blank spaces will separate the letter from its count.

       Returns None in all cases.

       Argument:
       some_text -- string containing the text to be analysed.

       Error checking:
       The argument must be a string object.
    """
    if not isinstance(some_text,str):
       print("Error: only accepts strings")
       return None

    # a string is turned into an list of characters
    chars = list(some_text) # extract the characters
    frequency = {} # empty dictionary
    # loop over the characters in the string
    for char in chars:
        # ignore non alphabetical characters
        if char.isalpha():
            char_lower = char.lower() # normalise it 
            # update the entry in the frequency table (probably more elegant solution than this!)
            if char_lower not in frequency.keys():
                frequency[char_lower] = 1
            else:
                frequency[char_lower] = frequency[char_lower]+1
    characters = list(frequency.keys())

    # dictionary is unsorted (unless you use OrderedDictionary)
    characters.sort()
    for char in characters:
        print("{}  {}".format(char,frequency[char]))
    return None

def verbing(some_text):
    """Returns a string where the each word has ing added to it if it is 3 or more characters or length and 
       ly to shorter words.

       Argument:
       some_text -- string containing the text to be analysed.

       Error checking:
       The argument must be a string object.
    """
    if not isinstance(some_text,str):
       print("Error: only accepts strings")
       return None
    words = some_text.split()
    # enumerate is necessary because I want to know the index
    #   of the word in the list to overwrite
    for pos,word in enumerate(some_text.split()):
        if len(word) >= 3:
            words[pos] = word + "ing"
        else:
            words[pos] = word + "ly"
    new_text = ' '.join(words)
    return(new_text)

def verbing_file(file_name):
    """Returns the contents of a given file after applying the verbing function to each
       line in the file.

       Argument:
       file_name -- name of the file (assumed to exist in same directory from where the 
                    python script is executed.

       Error checking:
       The argument must be a string object.
       File must exist and be readable (note no need to distinguish these cases).    
    """
    if not isinstance(file_name,str):
       print("Error: only accepts strings")
       return None

    # this try except catches ALL errors, doesn't distinguish WHY there is a failure
    try:  
       fin = open(file_name, "r")
       content = fin.read()
       fin.close()
    except:
        print("Error reading from file {}".format(file_name))
        return None

    # split into lines (this removes the trailing end of line)
    new_content=""
    for line in content.splitlines():
       # apply verbing to the line (minus the \n) and add missing \n back so prints correctly
       new_content = new_content + verbing(line) + "\n"
    return new_content
    
