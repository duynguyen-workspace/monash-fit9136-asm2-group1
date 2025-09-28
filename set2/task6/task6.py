from task4 import get_stopwords, get_vocabs
from task5 import (
    load_word_freq, load_word2idx, load_idx2word,
    save_word_freq, save_word2idx, save_idx2word   
)

# 3 constant file paths
WORD_FREQ_FILEPATH = "word_freq.txt"
WORD2IDX_FILEPATH = "word2idx"
IDX2WORD_FILEPATH = "idx2word.txt"

def updating_for_adding(
        stopwords_path: str,
        added_files: str | list,
        in_path: str,
        out_path: str
    ):
    """
    This function use for adding Files and Updating the Vocabulary
    Task includes:
        - Accept one or more new .txt files as input.
        - Extract the vocabulary from these new files.
        - Update the saved vocabulary file:
            * Add new words that are not currently in the vocabulary,
             with their corresponding frequency.
            * Increase the frequency of existing words if they appear
            in the new files.
    Args:
        stopwords_path (str): Path of file containing stopwords.
        added_files (str | list): Path of file or list files containing added words.
        in_path (str): Path of file containing old words.
        out_path (str): Path of file containing updated words.

    Returns:
        This function returns None. It saves the updated vocabulary to files.
    """
    if isinstance(added_files, str):
        added_files = [added_files]
    stopwords = get_stopwords(stopwords_path)
    word_freq = load_word_freq(f"{in_path}/{WORD_FREQ_FILEPATH}")
    for element in added_files:
        with open(element, "r") as f:
            text = f.read()

        vocabs = get_vocabs(text=text, stopwords=stopwords)
        if not vocabs:
            continue

        for word, freq in zip(vocabs[0], vocabs[1]):
            word_freq[word] = word_freq.get(word, 0) + freq


    words_list = list(word_freq.keys())
    freqs_list = [word_freq[word] for word in words_list]
    word = tuple(words_list)
    freq = tuple(freqs_list)
    save_word_freq(word, freq, f"{out_path}/{WORD_FREQ_FILEPATH}")
    save_word2idx(word, f"{out_path}/{WORD2IDX_FILEPATH}")
    save_idx2word(word, f"{out_path}/{IDX2WORD_FILEPATH}")


def updating_for_deleting(
        stopwords_path: str,
        excluded_files: str | list,
        in_path: str,
        out_path: str
    ):
    """
    This function use for deleting Files and Updating the Vocabulary.
    Task includes:
    - Accept one or more new .txt files as input.
    - Extract the vocabulary from these new files.
    - Update the saved vocabulary file:
        * Delete words which appear in deleted files,
        * Decrease the frequency of existing words if they appear in deleted files.
    Args:
        stopwords_path (str): Path of file containing stopwords.
        excluded_files (str | list): Path of file or list files containing deleted words.
        in_path (str): Path of file containing old words.
        out_path (str): Path of file containing updated words.

    Returns:
        This function returns None. It saves the updated vocabulary to files.
    """
    if isinstance(excluded_files, str):
        excluded_files = [excluded_files]
    stopwords = get_stopwords(stopwords_path)
    word_freq = load_word_freq(file_path=f"{in_path}/{WORD_FREQ_FILEPATH}")
    for element in excluded_files:
        with open(element, "r") as f:
            text = f.read()

        vocabs = get_vocabs(text=text, stopwords=stopwords)
        if not vocabs:
            continue

        for word, freq in zip(vocabs[0], vocabs[1]):
            if word in word_freq:
                new_freq = word_freq[word] - freq
                if new_freq > 0:
                    word_freq[word] = new_freq
                else:
                    word_freq.pop(word, None)


    words_list = list(word_freq.keys())
    freqs_list = [word_freq[word] for word in words_list]
    word = tuple(words_list)
    freq = tuple(freqs_list)
    save_word_freq(word, freq, f"{out_path}/{WORD_FREQ_FILEPATH}")
    save_word2idx(word, f"{out_path}/{WORD2IDX_FILEPATH}")
    save_idx2word(word, f"{out_path}/{IDX2WORD_FILEPATH}")

if __name__ == '__main__':
    add_files = [
        "./data/new_add0.txt",
        "./data/new_add1.txt"
    ]

    updating_for_adding(
        stopwords_path="./data/stop_words_english.txt",
        added_files=add_files,
        in_path="./data/old",
        out_path="./data/new"
    )

    updating_for_deleting(
        stopwords_path="./data/stop_words_english.txt",
        excluded_files="./data/new_delete0.txt",
        in_path="./data/old",
        out_path="./data/new"
    )
