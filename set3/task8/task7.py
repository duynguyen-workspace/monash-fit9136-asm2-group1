import pandas as pd
import json
from typing import Dict


def get_vocabs(text: str, stopwords: list) -> tuple[tuple[str], tuple[int]]:
    """
    This function splits the text into words and count number of time each word appears

    Params:
        1. text: <str> the unformatted text string
        2. stopwords: <str> the word to be filtered out

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
        # SUBPROCESS: skip the word if word length < 2, word contains number or word is a stopword
        word_size = len(word)
        if word_size < 2 or word in stopwords or check_word_has_number(word):
            continue

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
    the_word_lst.sort()  # sorted all the words

    if the_word_lst[0] is None:  # remove the first item (which is an empty string '')
        the_word_lst.pop(0)

    the_count_lst = []
    for word in the_word_lst:
        the_count_lst.append(words_dict[word])

    # Type casting from List -> Tuple
    the_word_lst = tuple(the_word_lst)
    the_count_lst = tuple(the_count_lst)
    result = (the_word_lst, the_count_lst)

    return result


def get_words(text: str, delimiters: str) -> list:
    """
    This function extract a list of (lowercase) words from the input text

    Params:
        1. text: <str> the input text string
        2. delimiters: <str> the symbols / characters that should be filtered from the word

    Returns:
        words: <list> a list of lowercase words
    """
    words = []
    word_buffer = ""
    # iterate each character, form into a word and add to word list
    for char in text:
        # while buffer is empty, skip the character if it is a blank space or a delimeter
        if len(word_buffer) == 0 and (char.isspace() or char in delimiters):
            continue

        # add character to buffer and extract word to the list
        if char not in delimiters and not char.isspace():
            word_buffer += char
        else:
            # SUBPROCESS: add character to buffer, extract word to the list and reset buffer
            word = word_buffer.lower()
            words.append(word)
            word_buffer = ""

    # SUBPROCESS: Add the remaining buffer (last word) to list
    if word_buffer:
        words.append(word_buffer.lower())

    # print(words)
    return words


def check_word_has_number(word: str) -> bool:
    """
    This function check if a word contain a number (digit)

    Params:
        1. word: <str> the word to be checked

    Returns:
        - <bool>: a boolean check if that function has a number or not

    """
    for char in word:
        if char.isdigit():
            return True

    return False


def load_idx2label(idx2label_filepath):
    """
    Load the file containing indexes and their labels.
    Args:
        idx2label_filepath (str):  path of the idx2label file.
    Returns:
        label_df (pandas.DataFrame): DataFrame mapping label ids to label names.
    """
    with open(idx2label_filepath) as f:
        mapping_dict = json.load(f)
    label_df = pd.DataFrame(mapping_dict.items(), columns=["label", "label_name"])
    return label_df


def get_stopwords(stopwords_file: str) -> list[str]:
    """
    This function gets all the stop words from the file

    Params:
        1. stopwords_file: <str> the file name containing the stop words

    Return:
        stopwords: <list> a list of strings (the stop words)
    """
    stopwords = []

    with open(stopwords_file, "r", encoding="utf8") as f:
        for line in f:
            word = line.strip().lower()
            stopwords.append(word)

    return stopwords


def get_corpus(corpus_filepath, label_df):
    """
    Merge the label dataframe and corpus dataframe return the corpus after joining
    Args:
        corpus_filepath (str):  path of the corpus file.
        label_df (pandas.DataFrame): label data frame.

    Returns:
        pandas.DataFrame: corpus dataframe after joining abd have label_name column.
    """
    # Cast the datatype of label column in label dataframe to int same data type with corpus
    label_df["label"] = label_df["label"].astype(int)
    corpus_df = pd.read_csv(corpus_filepath)
    # Merge corpus and label dataframe
    joined_df = pd.merge(corpus_df, label_df, on="label", how="inner")
    return joined_df


class TextProcessor:
    """
    Text Processor class for processing word in corpus in each label.

    Instance Variables:
        word_freq (dict): The dictionary containing the words and their frequencies.
        word2idx (dict): The dictionary containing the words and their indexes.
        idx2word (dict): The dictionary containing keys are indexes and values are words.
        stopwords (list): list of stop words.
        idx2label (pandas.DataFrame): DataFrame mapping label ids to label names.
    """

    def __init__(
            self,
            stopwords_filepath: str,
            corpus_filepath: str,
            idx2label_filepath: str
    ) -> None:
        # YOUR CODES START HERE
        """
        Create a new TextProcessor instance.
        Args:
            stopwords_filepath: Path of the stop words file.
            corpus_filepath: Path of the corpus file.
            idx2label_filepath: Path of the idx2label file.
        """
        self.word_freq = {}
        self.word2idx = {}
        self.idx2word = {}
        self.idx2label = load_idx2label(idx2label_filepath)
        self.corpus = get_corpus(corpus_filepath, self.idx2label)
        self.stopwords = get_stopwords(stopwords_filepath)
        self.add_freq_to_wordfreq(self.corpus["text"])

    def add_file(self, add_file_path: str) -> None:
        # YOUR CODES START HERE
        """
        Add the word from a file to vocabulary and update the keys and word frequency.
        Args:
            add_file_path: str: The path of the file containing the added words.

        Returns:
            This function does not return anything. It saves the vocabulary and word frequency by save method
        """
        added_corpus = get_corpus(corpus_filepath=add_file_path, label_df=self.idx2label)
        texts = added_corpus["text"]
        self.add_freq_to_wordfreq(texts=texts)

    def add_freq_to_wordfreq(self, texts):
        """
        This function update the word frequency of TextProcessor when initiating instance or adding file
        Args:
            texts (Iterable[str]): A list or pandas Series of text documents to be processed.

        Returns:
            This function return nothing. It is used for updating word frequency.
        """
        for text in texts:
            vocabs = get_vocabs(text=text, stopwords=self.stopwords)
            if not vocabs:
                continue

            vocabs, freqs = vocabs
            # Update the value in the vocabulary dictionary
            for vocab, freq in zip(vocabs, freqs):
                self.word_freq[vocab] = self.word_freq.get(vocab, 0) + freq
        self.save()

    def delete_file(self, delete_file_path) -> None:
        # YOUR CODES START HERE
        """
        Delete the words frequency from a delete file and save the vocabulary and word frequency.
        Args:
            delete_file_path: The path of the file containing the deleted words.

        Returns:
            This function does not return anything. It saves the vocabulary and word frequency by save method
        """
        deleted_corpus = get_corpus(corpus_filepath=delete_file_path, label_df=self.idx2label)
        texts = deleted_corpus["text"]

        # dict of delete word
        for text in texts:
            vocabs = get_vocabs(text=text, stopwords=self.stopwords)
            if not vocabs:
                continue
            words, freqs = vocabs
            for word, freq in zip(words, freqs):
                if word in self.word_freq:
                    new_freq = self.word_freq[word] - freq
                    # if the frequency minus to 0 remove the word from dictionary
                    if new_freq > 0:
                        self.word_freq[word] = new_freq
                    else:
                        self.word_freq.pop(word, None)

        self.save()

    def load(self) -> None:
        # YOUR CODES START HERE
        """
        Load the vocabulary and word frequency from provided file paths
        and update value in word2idx, word_freq, idx2word
        of the instance.
        Returns:
        This function does not return anything. It load the vocabulary and word frequency.
        """
        # Load word frequency dict
        word_freq = {}
        with open("word_freq.txt", "r") as f:
            for line in f:
                word, count = line.strip().split()
                word_freq[word] = int(count)
        self.word_freq = word_freq

        # Load word2idx dict
        word2idx = {}
        with open("word2idx.txt", "r") as f:
            for line in f:
                word, index = line.strip().split()
                word2idx[word] = int(index)
        self.word2idx = word2idx

        # Load idx2word dict
        idx2word = {}
        with open("idx2word.txt", "r") as f:
            for line in f:
                index, word = line.strip().split()
                idx2word[int(index)] = word
        self.idx2word = idx2word

    def save(self) -> None:
        """
        Save the vocabulary and word frequency , word2idx, and idx2word to
        word_freq.txt, word2idx.txt, and idx2word.txt.
        This function does not return anything. It save the vocabulary and word frequency.
        """
        # YOUR CODES START HERE
        # Clear all data in word2idx and idx2word for preventing duplicate with old data
        self.word2idx.clear()
        self.idx2word.clear()

        word_sorted_by_freq = self.get_word_sorted_by_freq()
        word_sorted_by_name = sorted(self.word_freq.keys())

        for index, word in enumerate(word_sorted_by_name):
            self.word2idx[word] = index
            self.idx2word[index] = word

        # Save word frequency
        with open("word_freq.txt", 'w') as f:
            # use join with generator expression
            f.write("".join((f"{word} {freq}\n" for word, freq in word_sorted_by_freq)))

        # Save word2idx
        with open("word2idx.txt", 'w') as f:
            # use join with generator expression
            f.write("".join(f"{word} {index}\n" for word, index in self.word2idx.items()))

        # Save idx2word
        with open("idx2word.txt", 'w') as f:
            # use join with generator expression
            f.write("".join(f"{index} {word}\n" for index, word in self.idx2word.items()))

    def get_word_sorted_by_freq(self):
        # This closure function to get key in the element of iterator for sorting
        def get_frequency(element):
            return element[1]

        word_sorted_by_freq = sorted(self.word_freq.items(), key=get_frequency, reverse=True)
        return word_sorted_by_freq

if __name__ == "__main__":
    tp = TextProcessor(
        stopwords_filepath="data/stop_words_english.txt",
        corpus_filepath="data/ag_news_test.csv",
        idx2label_filepath="data/idx2label.json",
    )
    print(len(tp.word_freq))
    print(tp.corpus)
