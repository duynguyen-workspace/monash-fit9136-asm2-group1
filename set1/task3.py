from typing import Tuple, List

def get_vocabs_simple(text: str) -> Tuple[Tuple[str], Tuple[int]]:
    """ (Simple Version)
    This function splits the text into words and count the number of time each word appears

    Params:
        1. text: <str> the unformatted text string
    
    Returns:
        vocabs: <Tuple[Tuple[str], Tuple[int]]> A tuple that contains 2 subtuples
        - the_word_list: list of words in the text string
        - the_count_list: number of iteration that each word appears

    Requirements:
        1. The given string already separates each word by a space
        2. Only unique words are recorded, no punctuation allowed
        3. The word list is sorted followed by the count list

    Assumptions:
        - "Simple strings" have words and punctuation marks concatenated using a single space
    """
    if not text:
        return ()
    
    # CONSTANTS
    PUNCTUATIONS = "!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"

    # Get the word list: seperate the words + punctuations by a single space
    words = text.split()

    # Filter out all the punctuations, add words to the dictionary and count their frequencies
    words_dict = {}
    for word in words:
        word = word.strip(PUNCTUATIONS) # filter punctuations

        if not word or word.isspace():
            continue
        
        if word not in words_dict.keys(): # # add / update word in dictionary
            words_dict[word] = 1
        else:
            words_dict[word] += 1
    
    # --- MAIN OUTPUT: return the result tuple (if the dictionary is not empty)
    if not words_dict:
        return ()

    # sorted all the words in ascending order
    the_word_lst = list(words_dict.keys())
    the_word_lst.sort() 

    # return two tuples of unique words and the word's count in sorted order
    the_count_lst = [words_dict.get(word) for word in the_word_lst]
    the_word_lst = tuple(the_word_lst)
    the_count_lst = tuple(the_count_lst)
    
    vocabs = (the_word_lst, the_count_lst)

    return vocabs

def get_vocabs(text: str) -> Tuple[Tuple[str], Tuple[int]]:
    """ (Complex Version)
    This function splits the text into words and count the number of time each word appears
    
    Params:
        1. text: <str> the unformatted text string

    Returns:
        vocabs: <Tuple[Tuple[str], Tuple[int]]> A tuple that contains 2 subtuples
        - the_word_list: list of words in the text string
        - the_count_list: number of iteration that each word appears

    Requirements:
        (Old)
        1. Only unique words are recorded, no punctuation allowed 
        2. The word list is sorted followed by the count list
        (New)
        3. All words are converted to lowercase.
        4. If punctuation directly follow a word, they are cleaned
        5. Contractions will always follow the correct English syntax
    """
    if not text:
        return ()

    # Process the word list and generate a word dictionary containing its count
    words = get_words(text)
    
    words_dict = {} 
    for word in words:
        formatted_word = word.lower()

        # Add / Update word (lowercase) into dictionary
        if formatted_word not in words_dict.keys():
            words_dict[formatted_word] = 1
        else:
            words_dict[formatted_word] += 1
    
    # --- MAIN OUTPUT: return the result tuple (if the dictionary is not empty)
    if not words_dict:
        return ()

    # sorted all the words in ascending order
    the_word_lst = list(words_dict.keys())
    the_word_lst.sort() 

    # return two tuples of unique words and the word's count in sorted order
    the_count_lst = [words_dict.get(word) for word in the_word_lst]
    the_word_lst = tuple(the_word_lst)
    the_count_lst = tuple(the_count_lst)
    
    vocabs = (the_word_lst, the_count_lst)

    return vocabs

def get_words(text: str) -> List[str]:
    """
    This function process the input text and extract a list of (cleaned) words

    Params:
        1. text: <str> the input text string

    Returns:
        words: <List[str]> a list of lowercase words

    Requirements:
        1. all words are in lowercase
        2. words have been cleaned (contains no punctuation in between)

    """
    # CONSTANTS
    PUNCTUATIONS = "!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"

    # iterate each character, compute them into a proper word and insert accordingly to word list
    words = []
    
    word_buffer = ""
    for char in text:
        # While buffer is empty -> skip the character if it is a blank space or a punctuation
        if not word_buffer and (char.isspace() or char in PUNCTUATIONS):
            continue

        # Add character to buffer, extract (lowercase) word to list, and reset buffer
        if char not in PUNCTUATIONS and not char.isspace():
            word_buffer += char
        else:
            word = word_buffer.lower()
            words.append(word)
            word_buffer = "" 
    
    # Add the remaining buffer (last word) to list 
    if word_buffer:
        words.append(word_buffer.lower())

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