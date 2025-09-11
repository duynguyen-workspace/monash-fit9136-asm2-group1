from typing import Tuple, List

def get_vocabs_simple(text: str) -> Tuple[Tuple[str], Tuple[int]]:
    """ (Simple Version)
    This function slits the string into words and count number of time each word appears

    Params:
        1. text: <str> the unformatted text string
    
    Returns:
        result: <tuple> A tuple that contains 2 tuples
        - the_word_list: list of words in the text string
        - the_count_list: number of iteration that each word appears
    """
    if text is None or len(text) == 0:
        return ()

    # PROCESS: seperate the words by the blank space in between
    words = text.split()

    # PROCESS: Check if word is (or contain) a punctuation and add it to dictionary for counting
    words_dict = {}

    for word in words:
        if len(word) == 0:
            continue
        
        # Add word to dictionary / update word count (if it is not a punctuation)
        if word != "," or word != ".":
            word = word.strip(",.")

            if word not in words_dict.keys():
                words_dict[word] = 1
            else:
                words_dict[word] += 1
    
    # --- MAIN OUTPUT: return the result tuple (if the dictionary is not empty)
    if len(words_dict) == 0:
        return ()

    # SUBPROCESS - return all the unique words and the word count in sorted order
    the_word_lst = list(words_dict.keys())
    the_word_lst.sort() # sorted all the words
    
    if the_word_lst[0] is None: # remove the first item (if it is an empty string '')
        the_word_lst.pop(0) 

    the_count_lst = []
    for word in the_word_lst:
        the_count_lst.append(words_dict[word])

    # Type casting from List -> Tuple
    the_word_lst = tuple(the_word_lst)
    the_count_lst = tuple(the_count_lst)
    result = (the_word_lst, the_count_lst)

    return result

def get_vocabs(text: str) -> Tuple[Tuple[str], Tuple[int]]:
    """ (Complex Version)
    This function slits the string into words and count number of time each word appears
    
    Params:
        1. text: <str> the unformatted text string
    
    Returns:
        result: <tuple> A tuple that contains 2 tuples
        - the_word_list: list of words in the text string
        - the_count_list: number of iteration that each word appears
    """
    if text is None or len(text) == 0:
        return ()
    
    # CONSTANTS
    PUNCTUATIONS = "!\"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~" # list of punctuations to check
    
    # PROCESS: split the word by blank space between
    words = text.split()
    
    words_dict = {} # initialise words dictionary for counting

    # PROCESS: Check if word is (or contain) a punctuation and add it to dictionary for counting
    for word in words:
        if word not in PUNCTUATIONS:
            # Remove all the punctuations that stick with the word
            cleaned_word = word.strip(PUNCTUATIONS)

            # If the word is empty --> pass to next one
            if len(cleaned_word) == 0:
                continue

            # Add word to dictionary / update word count
            formatted_word = cleaned_word.lower()
            if formatted_word not in words_dict.keys():
                words_dict[formatted_word] = 1
            else:
                words_dict[formatted_word] += 1
    
    # --- MAIN OUTPUT: return the result tuple (if the dictionary is not empty)
    if len(words_dict) == 0:
        return ()

    # SUBPROCESS - return all the unique words and the word count in sorted order
    the_word_lst = list(words_dict.keys())
    the_word_lst.sort() # sorted all the words

    if the_word_lst[0] is None: # remove the first item (which is an empty string '')
        the_word_lst.pop(0) 

    the_count_lst = []
    for word in the_word_lst:
        the_count_lst.append(words_dict[word])

    # Type casting from List -> Tuple
    the_word_lst = tuple(the_word_lst)
    the_count_lst = tuple(the_count_lst)
    result = (the_word_lst, the_count_lst)

    return result

# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    # the_example_str = "you are good at python , and you will be master of programming ."
    # the_example_str = ",. ? / ! # @"
    the_example_str = "apple,"
    print(get_vocabs_simple(the_example_str))
    print(get_vocabs(the_example_str))