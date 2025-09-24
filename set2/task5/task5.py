from typing import Tuple


def save_word_freq(word: Tuple[str], freq: Tuple[int], file_path: str = 'word_freq.txt'):
    """
    This function zips two tuples (words and frequencies) into an iterator,
    sorts the resulting pairs in descending order of frequency,
    and then joins its elements into a string for saving to word_freq.txt.
    Args:
        word: Tuple[str]: Tuple of word.
        freq: Tuple[int] (Tuple): Tuple of each word frequency.
        file_path: str='word_freq.txt' : File path to save word frequencies.
    Returns:
        None: The function does not return any value; it save the tuples after processing into a file.
    """
    # Zip two tuples into an iterator
    words = zip(word, freq)

    # Closure function to get element in tuple
    def get_frequency(element):
        frequency = element[1]
        return frequency

    # Sorting in descending order of frequency with key is frequency
    sorted_words = sorted(words, key=get_frequency, reverse=True)

    with open(file_path, 'w') as f:
        # use join with generator expression 
        f.write("".join((f"{wrd} {frq}\n" for wrd, frq in sorted_words)))


def save_word2idx(word: Tuple[str], file_path: str = "word2idx.txt"):
    """
    This function generate a lookup table that assigns a unique index to each word based 
    on its alphabetical order (i.e., ascending order by word), and save it as word2idx.txt
    Args:
        word: Tuple[str]: Tuple of words.
        file_path: str='word2idx.txt' : File path to save word frequencies.
    Returns:
        None: The function does not return any value; it save the tuples after processing into a file.
    """

    # Sorting word base on it index
    sorted_word = sorted(word)
    # Create an interator contain many tuples with each tuple have (index, word)
    enumerated_word = enumerate(sorted_word)
    # Save file with alphabetical order and index
    with open(file_path, "w") as f:
        # Use join with generator expression
        f.write("".join((f"{element[1]} {element[0]}\n" for element in enumerated_word)))


def save_idx2word(word: Tuple[str], file_path: str = "idx2word.txt"):
    """
    This function generate a lookup table that assigns a unique index to each word based 
    on its alphabetical order (i.e., ascending order by word) with reverse mapping, and save it as idx2word.txt
    Args:
        word: Tuple[str]: Tuple of words.
        file_path: str='idx2word.txt' : File path to save word frequencies.
    Returns:
        None: The function does not return any value; it save the tuples after processing into a file.
    """

    # Sorting word base on it index
    sorted_word = sorted(word)
    # Create an interator contain many tuples with each tuple have (index, word)
    enumerated_word = enumerate(sorted_word)

    # Save file with index and alphabetical order
    with open(file_path, "w") as f:
        # use join with generator expression 
        f.write("".join((f"{element[0]} {element[1]}\n" for element in enumerated_word)))


def load_word_freq(file_path: str) -> dict:
    """
    Load the saved vocabulary from file path and store it in a Python dictionary,
    where the keys are words and the values are their frequencies.
    Args:
        file_path: The file path to load the vocabulary from.
    Returns:
        This function does not return any value; it loads the vocabulary from file path.
    """
    word_list = dict()
    with open(file_path, "r") as f:
        for line in f.readlines():
            element = line.strip("\n").split(" ")
            word_list[element[0]] = int(element[1])
    return word_list


def load_word2idx(file_path: str):
    """
    Load the saved vocabulary from file path and store it in a Python dictionary, where the keys are words and
    the values are their indexes.
    Args:
        file_path: The file path to load the vocabulary from.

    Returns:
        This function does not return any value; it loads the vocabulary from file path.
    """
    word_list = dict()
    with open(file_path, "r") as f:
        for line in f.readlines():
            element = line.split(" ")
            word_list[element[0]] = int(element[1])
    return word_list


def load_idx2word(file_path: str):
    """
    Load the saved vocabulary from file path and store it in a Python dictionary, where the keys are indexes and
    the values are words.
    Args:
        file_path: The file path to load the vocabulary from.

    Returns:
        This function does not return any value; it loads the vocabulary from file path.
    """
    word_list = dict()
    with open(file_path, "r") as f:
        for line in f.readlines():
            element = line.strip("\n").split(" ")
            word_list[int(element[0])] = (element[1])
    return word_list


if __name__ == "__main__":
    word = ('apple', 'dog', 'master')
    freq = (3, 10, 1)
    save_word_freq(word=word, freq=freq)
    save_word2idx(word=word)
    save_idx2word(word=word)
