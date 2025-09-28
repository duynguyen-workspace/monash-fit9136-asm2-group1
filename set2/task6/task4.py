from typing import Tuple, List, Set, Optional
import os


def get_stopwords(stopwords_file: str) -> List[str]:
    """
    This function gets all the stop words from the file 

    Args:
        1. stopwords_file (str): the file name containing the stop words

    Return:
        stopwords (List[str]): a list of strings (the stop words)
    """
    if not stopwords_file:
        return []

    stopwords = []

    with open(stopwords_file, "r") as f:
        for line in f:
            word = line.strip().lower()
            stopwords.append(word)

    return stopwords


def get_vocabs(text: str, stopwords: List) -> Tuple[Tuple[str], Tuple[int]]:
    """
    This function splits the text into words and count number of time each word appears.
    Exclude any word that is a stopword

    Args:
        1. text (str): the unformatted text string
        2. stopwords (str): the word to be filtered out

    Returns:
        vocabs (Tuple[Tuple[str], Tuple[int]]): A tuple that contains 2 tuples
        - the_word_list: list of words in the text string
        - the_count_list: number of iteration that each word appears
    """
    if not text:
        return ()

    # process the text, extract the word list and generate a dictionary containing word count
    words = get_words(text)
    words_dict = {}

    for word in words:
        # Skip if word is a stopword
        if word in stopwords:
            continue

        # add / update word into dictionary
        if word not in words_dict.keys():
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


def get_words(text: str) -> List[str]:
    """
    This function extract a list of (lowercase) cleaned words from the input text
    based on the given requirements

    Args:
        1. text (str): the input text string

    Returns:
        words (List[str]): a list of lowercase words

    Requirements:
        1. all words have been converted to lowercase
        2. clean all the punctuations and contractions
        3. filtering out numbers and words composed entirely of digits
        4. discarding words with a length less than 2
    """
    # CONSTANTS
    PUNTUATIONS = "!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"

    # iterate each character, form into a word and add to word list
    words = []

    word_buffer = ""
    for char in text:
        # While buffer is empty -> skip the character if it is a blank space / a delimeter
        if not word_buffer and (char.isspace() or char in PUNTUATIONS):
            continue

        # Add character to buffer, extract (lowercase) word to list, and reset buffer
        if char not in PUNTUATIONS and not char.isspace():
            word_buffer += char
        else:
            # check if buffer has a valid length and contain no number
            word = word_buffer.lower()

            if len(word) >= 2 and not check_word_has_number(word):
                words.append(word)

            word_buffer = ""  # reset buffer

    # Add the remaining buffer (last word) to list (must satisfy requirements)
    if word_buffer and len(word_buffer) >= 2 and not check_word_has_number(word_buffer):
        words.append(word_buffer.lower())

    return words


def check_word_has_number(word: str) -> bool:
    """
    This function check if a word contain a number (digit)

    Args:
        1. word (str): the word to be checked

    Returns:
        bool: a boolean check if that function has a number or not
    """
    for char in word:
        if char.isdigit():
            return True

    return False


def process_mini_dataset(
        stopwords: Set[str],
        data_path: str = 'data',
        category: Optional[str] = None,
) -> Tuple[Tuple[str], Tuple[int]]:
    """
    This function read all the .txt files from the data path and generate a vocabulary list

    Args:
        1. stop_words (Set[str]): a list of word that should not be included in the vocab list
        2. data_path (str): the path to the 'data' folder that contains the .txt files
        3. category (str): the category name

    Return:
        vocabs (Tuple[Tuple[str], Tuple[int]]): a tuple of vocabulary consists of two tuples:
            + (str) the list of vocabularies name
            + (int) the count of each vocabulary appears
            (same return type as get_vocabs function)

    Notes:
        1. if no category
        --> generate vocabularies from all text files (accross all categories)
        2. if a category is provided
        --> generate vocabullaries from all the text file in that category folder
    """

    # get all the files / folders in the data path
    all_files_in_dir = os.listdir(data_path)
    curr_data_path = data_path

    # @CASE 1: no category provide --> get vocabs from all txt files of all categories
    if category and category in all_files_in_dir:
        curr_data_path = os.path.join(data_path, category)
        all_files_in_dir = os.listdir(curr_data_path)
        text = get_text_from_files(curr_data_path)

    # @CASE 2: a category is provided --> get vocabs from all .txt file of that category
    else:
        # get all the category folders (by checking non .txt file / folder)
        categories = []
        for file_name in all_files_in_dir:
            if not file_name.endswith(".txt"):
                categories.append(file_name)

        # concatenate all the .txt file from each category folder
        text = ""
        for category_name in categories:
            category_path = os.path.join(curr_data_path, category_name)
            category_text = get_text_from_files(category_path)
            text += category_text

    # OUTPUT: get the vocabularies list
    vocabs = get_vocabs(text, stopwords)
    return vocabs


def get_text_from_files(data_path: str) -> str:
    """
    This function read all the .txt file inside the path and
    concatenate its content into a string

    Args:
        1. data_path (str): the path to the folder containing the files

    Returns:
        text (str): the content of all files in that folder
    """
    # Get all the files inside the directory
    all_files_in_dir = os.listdir(data_path)

    # Extract the text from each file and concatenate all of the content together
    text = ""
    for file_name in all_files_in_dir:
        file_path = os.path.join(data_path, file_name)

        with open(file_path, "r") as f:
            content = f.read().strip()
            text += f"{content} "

    return text


# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    # your testing code goes here
    stopwords = get_stopwords("data/stop_words_english.txt")
    # print(get_words("a b c 123 !@# apple ap pl e"))
    # print(get_vocabs("BUL, Afghanistan - Government troops intervened in Afghanistan's latest outbreak of deadly fighting between warlords, flying from the capital to the far west on U.S. and NATO airplanes to retake an air base contested in the violence, officials said Sunday...", stopwords))
    process_mini_dataset(stopwords, 'data', "Business")
    # process_mini_dataset(stopwords, 'data')
