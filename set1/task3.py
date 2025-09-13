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
    PUNCTUATIONS = "!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"

    # PROCESS: process the word list and generate a word dictionary containing its count
    words = get_words(text, PUNCTUATIONS)
    words_dict = {} 

    for word in words:
        # SUBPROCESS: add / update word (lowercase) into dictionary
        formatted_word = word.lower()
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

def get_words(text: str, delimeters: str) -> list:
    """
    This function extract a list of (lowercase) words from the input text

    Params:
        1. text: <str> the input text string
        2. delimeters: <str> the symbols / characters that should be filtered from the word
    
    Returns:
        words: <list> a list of lowercase words

    """

    # PROCESS: iterate each character, form into a word and add to word list
    words = []
    word_buffer = ""

    for char in text:
        # SUBPROCESS: while buffer is empty, skip the character if it is a blank space or a delimeter
        if len(word_buffer) == 0 and (char.isspace() or char in delimeters):
            continue

        # SUBPROCESS: add character to buffer, extract word to the list and reset buffer
        if char not in delimeters and not char.isspace():
            word_buffer += char
        else:
            word = word_buffer.lower()
            words.append(word)
            word_buffer = "" 
    
    # SUBPROCESS: Add the remaining buffer (last word) to list 
    if word_buffer:
        words.append(word_buffer.lower())

    # print(words)
    return words

# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    # get_words("BUL, Afghanistan - Government troops intervened in Afghanistan's latest outbreak of deadly fighting between warlords, flying from the capital to the far west on U.S. and NATO airplanes to retake an air base contested in the violence, officials said Sunday...")
    # the_example_str = "you are good at python , and you will be master of programming ."
    # the_example_str = ",. ? / ! # @"
    the_example_str = "Hello, apple?! 'You you', yOU, heLLo, I've, At, apPle"
    # the_example_str = "BUL, Afghanistan - Government troops intervened in Afghanistan's latest outbreak of deadly fighting between warlords, flying from the capital to the far west on U.S. and NATO airplanes to retake an air base contested in the violence, officials said Sunday..."
    # print(get_vocabs_simple(the_example_str))
    print(get_vocabs(the_example_str))