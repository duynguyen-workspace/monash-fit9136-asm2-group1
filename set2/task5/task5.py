# copy your task5 code herefrom typing import Tuple

from typing import Tuple


def save_word_freq(word: Tuple[str], freq: Tuple[int], file_path: str = 'word_freq.txt'):
    """
    This function zips two tuples (words and frequencies) into an iterator,
    sorts the resulting pairs in descending order of frequency,
    and then joins its elements into a string for saving to word_freq.txt.
    Args:
        word: Tuple[str]: Tuple of word.
        freq: Tuple[int] (Tuple): Tuple of each word frequency.
        file_path: str='word_freq.txt' : file path to save word frequencies.
    Returns:
        None: The function does not return any value; it save the tuples after processing into a file.
    """
    # Zip two tuple into an iterator
    words = zip(word, freq)

    # Closure function to get element in tuple
    def get_frequency(element) :
        frequency = element[1]
        return frequency

    # Sorting in descending order of frequency with key is frequency
    sorted_words = sorted(words, key=get_frequency, reverse=True)

    with open(file_path, 'w') as f:
        # use join with generator expression 
        f.write("".join((f"{word} {freq}\n" for word, freq in sorted_words)))


def save_word2idx(word: Tuple[str], file_path: str = "word2idx.txt"):
    """
    This function generate a lookup table that assigns a unique index to each word based 
    on its alphabetical order (i.e., ascending order by word), and save it as word2idx.txt
    Args:
        word: Tuple[str]: Tuple of words.
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
        f.write("".join((f"{word[1]} {word[0]}\n" for word in enumerated_word)))


def save_idx2word(word: Tuple[str], file_path: str = "idx2word.txt"):
    """
    This function generate a lookup table that assigns a unique index to each word based 
    on its alphabetical order (i.e., ascending order by word) with reverse mapping, and save it as idx2word.txt
    Args:
        word (Tuple): Tuple of fruits.
    Returns:
        None: The function does not return any value; it save the tuples after processing into a file.
    """
    sorted_word = sorted(word)
    # Add index into list have tuple of index and word

    enumerated_word = enumerate(sorted_word)

    # Save file with index and alphabetical order
    with open(file_path, "w") as f:
        # use join with generator expression 
        f.write("".join((f"{word[0]} {word[1]}\n" for word in enumerated_word)))


def load_word_freq(file_path: str) -> dict:
    """
    Load the saved vocabulary from word_freq.txt and store it in a Python dictionary, 
    where the keys are words and the values are their frequencies.
    """
    word_list = dict()
    with open(file_path, "r") as f:
        for line in f.readlines():
            word = line.strip("\n").split(" ")
            word_list[word[0]] = int(word[1])
    return word_list


def load_word2idx(file_path: str):
    word_list = dict()
    with open(file_path, "r") as f:
        for line in f.readlines():
            word = line.split(" ")
            word_list[word[0]] = int(word[1])
    return word_list


def load_idx2word(file_path: str):
    word_list = dict()
    with open(file_path, "r") as f:
        for line in f.readlines():
            word = line.strip("\n").split(" ")
            word_list[int(word[0])] = (word[1])
    return word_list


def main():
    word = ('apple', 'dog', 'master')
    freq = (3, 10, 1)
    save_word_freq(word=word, freq=freq)
    save_word2idx(word=word)
    save_idx2word(word=word)


if __name__ == "__main__":
    main()
