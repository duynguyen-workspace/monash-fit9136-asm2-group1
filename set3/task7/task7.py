import pandas as pd
import json
from typing import Dict

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

        # SUBPROCESS: add character to buffer and extract word to the list
        if char not in delimeters and not char.isspace():
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

class TextProcessor:
    vocab = {}

    def __init__(
            self,
            stopwords_filepath: str,
            corpus_filepath: str,
            idx2label_filepath: str
    ) -> None:
        # YOUR CODES START HERE
        self.word_freq = {}
        self.word2idx = {}
        self.idx2word = {}
        self.corpus_df = None
        self.stopwords = get_stopwords(stopwords_filepath)
        self.idx2label = self.load_idx2label(idx2label_filepath)
        self.add_file(corpus_filepath)

    def load_idx2label(self, idx2label_filepath):
        with open(idx2label_filepath) as f:
            mapping_dict = json.load(f)
        label_df = pd.DataFrame(mapping_dict.items(), columns=["label", "label_name"])
        return label_df

    def add_file(self, add_file_path: str) -> None:
        # YOUR CODES START HERE
        self.corpus_df = pd.read_csv(add_file_path)
        self.idx2label["label"] = self.idx2label["label"].astype(int)

        corpus_table = self.corpus_df
        label_table = self.idx2label
        stopwords = self.stopwords

        joined_table = pd.merge(corpus_table, label_table, on="label", how="inner")

        texts = joined_table["text"]

        for text in texts:
            vocabs = get_vocabs(text=text,stopwords=stopwords)
            if not vocabs:
                continue

            vocabs, freqs = vocabs
            for vocab,freq in zip(vocabs, freqs):
                self.word_freq[vocab] = self.word_freq.get(vocab, 0) + freq
        self.save()


    def delete_file(self, delete_file_path) -> None:
        # YOUR CODES START HERE
        pass

    def load(self) -> None:
        # YOUR CODES START HERE

        word_freq = {}
        with open("word_freq.txt","r",encoding="utf-8") as f:
            for line in f:
                word, count = line.strip().split()
                word_freq[word] = int(count)
        self.word_freq = word_freq


        word2idx = {}
        with open("word2idx.txt", "r",encoding="utf-8") as f:
            for line in f:
                word, index = line.strip().split()
                word2idx[word] = int(index)
        self.word2idx = word2idx


        idx2word = {}
        with open("idx2word.txt", "r",encoding="utf-8") as f:
            for line in f:
                index, word = line.strip().split()
                idx2word[int(index)] = word
        self.idx2word = idx2word

    def save(self) -> None:
        # YOUR CODES START HERE
        def get_frequency(word):
            return word[1]

        word_sorted_by_freq = sorted(self.word_freq.items(), key=get_frequency, reverse=True)
        word_sorted_by_name = sorted(self.word_freq.keys())

        for index, word in enumerate(word_sorted_by_name):
            self.word2idx[word] = index
            self.idx2word[index] = word

        with open("word_freq.txt", 'w') as f:
            # use join with generator expression
            f.write("".join((f"{word} {freq}\n" for word, freq in word_sorted_by_freq)))

        with open("word2idx.txt", 'w') as f:
            # use join with generator expression
            f.write("".join(f"{word} {index}\n" for word, index in self.word2idx.items()))

        with open("idx2word.txt", 'w') as f:
            # use join with generator expression
            f.write("".join(f"{index} {word}\n" for index, word in self.idx2word.items()))

if __name__ == "__main__":
    tp = TextProcessor(
        stopwords_filepath="data/stop_words_english.txt",
        corpus_filepath="data/ag_news_test.csv",
        idx2label_filepath="data/idx2label.json",
    )
    print(len(tp.word_freq))