import pandas as pd
import json
from typing import Dict

# Filepath of 3 text files
WORD_FREQ_FILEPATH = "word_freq.txt"
WORD2IDX_FILEPATH = "word2idx.txt"
IDX2WORD_FILEPATH = "idx2word.txt"

# Python string punctuations
PUNCTUATIONS = "!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"


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
        Returns:
            None
        """
        self.word_freq = {}
        self.word2idx = {}
        self.idx2word = {}
        self.idx2label = self._load_idx2label(idx2label_filepath)
        self.corpus = self._get_corpus(corpus_filepath, self.idx2label)
        self.stopwords = self._get_stopwords(stopwords_filepath)
        self._add_freq_to_wordfreq(self.corpus["text"])

    def _get_corpus(self, corpus_filepath: str, label_df: pd.DataFrame) -> pd.DataFrame:
        """
        Merge the label dataframe and corpus dataframe return the corpus after joining.
        Args:
            corpus_filepath (str):  Path of the corpus file.
            label_df (pandas.DataFrame): Label data frame.

        Returns:
            pandas.DataFrame: Corpus dataframe after join, with a label_name column.
        """
        # Cast the datatype of label column in label dataframe to int same data type with corpus
        label_df["label"] = label_df["label"].astype(int)
        corpus_df = pd.read_csv(corpus_filepath)
        # Merge corpus and label dataframe
        joined_df = pd.merge(corpus_df, label_df, on="label", how="inner")
        return joined_df

    def add_file(self, add_file_path: str) -> None:
        # YOUR CODES START HERE
        """
        Add the word from a file to vocabulary and update the keys and word frequency.
        Args:
            add_file_path (str): The path of the file containing the added words.

        Returns:
            This function does not return anything. It saves the vocabulary and word frequency by save method.
        """
        added_corpus = self._get_corpus(corpus_filepath=add_file_path, label_df=self.idx2label)
        texts = added_corpus["text"]
        self._add_freq_to_wordfreq(texts=texts)

    def _add_freq_to_wordfreq(self, texts):
        """
        This function update the word frequency of TextProcessor when initiating instance or adding file.
        Args:
            texts (Iterable[str]): A list or pandas Series of text documents to be processed.

        Returns:
            This function return nothing. It is used for updating word frequency.
        """
        for text in texts:
            vocabs = self.get_vocabs(text=text, stopwords=self.stopwords)
            if not vocabs:
                continue

            # Update the value in the vocabulary dictionary
            for vocab, freq in vocabs.items():
                self.word_freq[vocab] = self.word_freq.get(vocab, 0) + freq
        self.save()

    def delete_file(self, delete_file_path) -> None:
        # YOUR CODES START HERE
        """
        Delete the words frequency from a delete file and save the vocabulary and word frequency.
        Args:
            delete_file_path: The path of the file containing the deleted words.

        Returns:
            This function does not return anything. It saves the vocabulary and word frequency by save method.
        """
        deleted_corpus = self._get_corpus(corpus_filepath=delete_file_path, label_df=self.idx2label)
        texts = deleted_corpus["text"]

        # dict of delete word
        for text in texts:
            vocabs = self.get_vocabs(text=text, stopwords=self.stopwords)
            if not vocabs:
                continue
            for word, freq in vocabs.items():
                if word in self.word_freq:
                    new_freq = self.word_freq[word] - freq
                    # If the frequency minus to 0 remove the word from dictionary
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
            This function does not return anything. It loads the vocabulary and word frequency.
        """
        self.word_freq = self._load_word_freq(WORD_FREQ_FILEPATH)
        self.word2idx = self._load_word2idx(WORD2IDX_FILEPATH)
        self.idx2word = self._load_idx2word(IDX2WORD_FILEPATH)

    def _load_word_freq(self, filepath) -> Dict[str, int]:
        """
        Load the file word_freq.txt.
        Args:
            filepath: the path of the file containing the word frequency.

        Returns:
            Dict[str, int]: Dict of word frequency.
        """
        # Load word frequency dict
        word_freq = {}
        with open(filepath, "r") as f:
            for line in f:
                word, count = line.strip().split()
                word_freq[word] = int(count)
        return word_freq

    def _load_word2idx(self, filepath) -> Dict[str, int]:
        """
        Load the file word2idx.txt.
        Args:
            filepath: The path of the file containing the word and index.

        Returns:
            Dict[str, int]: Dict of words and its index.
        """
        # Load word2idx dict
        word2idx = {}
        with open(filepath, "r") as f:
            for line in f:
                word, index = line.strip().split()
                word2idx[word] = int(index)
        return word2idx

    def _load_idx2word(self, filepath) -> Dict[int, str]:
        # Load idx2word dict
        """
        Load the file idx2word.txt.
        Args:
            filepath: The path of the file containing the index and word.

        Returns:
            Dict[int, str]: Dict of indexes and words.
        """
        idx2word = {}
        with open(filepath, "r") as f:
            for line in f:
                index, word = line.strip().split()
                idx2word[int(index)] = word
        return idx2word

    def save(self) -> None:
        """
        Save the vocabulary and word frequency , word2idx, and idx2word to
        word_freq.txt, word2idx.txt, and idx2word.txt.

        Returns:
            This function does not return anything. It save the vocabulary and word frequency.
        """
        # YOUR CODES START HERE
        # Clear all data in word2idx and idx2word for preventing duplicate with old data
        self.word2idx.clear()
        self.idx2word.clear()

        word_sorted_by_name = sorted(self.word_freq.keys())

        for index, word in enumerate(word_sorted_by_name):
            self.word2idx[word] = index
            self.idx2word[index] = word

        # Save 3 files
        self._save_word_freq(WORD_FREQ_FILEPATH)
        self._save_word2idx(WORD2IDX_FILEPATH)
        self._save_idx2word(IDX2WORD_FILEPATH)

    def _save_word_freq(self, filepath) -> None:
        """
        Save the word frequency.
        Args:
            filepath: The path of saving file.

        Returns:
            This function does not return anything.
        """
        word_sorted_by_freq = self.get_word_sorted_by_freq()
        # Save word frequency
        with open(filepath, 'w') as f:
            # use join with generator expression
            f.write("".join((f"{word} {freq}\n" for word, freq in word_sorted_by_freq)))

    def _save_word2idx(self, filepath) -> None:
        """
        Save the dictionary word2idx.
        Args:
            filepath: The path of saving file.

        Returns:
            This function does not return anything.
        """
        # Save word2idx
        with open(filepath, 'w') as f:
            # use join with generator expression
            f.write("".join(f"{word} {index}\n" for word, index in self.word2idx.items()))

    def _save_idx2word(self, filepath) -> None:
        """
        Save the dictionary idx2word.
        Args:
            filepath: The path of saving file.

        Returns:
            This function does not return anything.
        """
        # Save idx2word
        with open(filepath, 'w') as f:
            # use join with generator expression
            f.write("".join(f"{index} {word}\n" for index, word in self.idx2word.items()))

    def get_word_sorted_by_freq(self) -> list[tuple]:
        """
        Get the list of word sorted by frequency.
        Returns:
            list[tuple]: a list of tuple (word, frequency).
        """

        # This closure function to get key in the element of iterator for sorting
        def get_frequency(element):
            return element[1]

        word_sorted_by_freq = sorted(self.word_freq.items(), key=get_frequency, reverse=True)
        return word_sorted_by_freq

    def _get_stopwords(self, stopwords_file: str) -> list[str]:
        """
        This function gets all the stop words from the file.

        Args:
            stopwords_file (str): the file name containing the stop words.

        Returns:
             list[str]: a list of strings (the stop words).
        """
        stopwords = []

        with open(stopwords_file, "r") as f:
            for line in f:
                word = line.strip().lower()
                stopwords.append(word)

        return stopwords

    def get_vocabs(self, text: str, stopwords: list[str]) -> Dict[str, int]:
        """
        This function splits the text into words and count number of time each word appears.

        Args:
            text (str): the unformatted text string.
            stopwords (list[str]): Words to be filtered out.

        Returns:
            Dict[str, int]: A dictionary contain words and its amount.
        """
        if text is None or len(text) == 0:
            return {}

        # PROCESS: process the word list and generate a word dictionary containing its count
        words = self._get_words(text, PUNCTUATIONS)
        words_dict = {}

        for word in words:
            # SUBPROCESS: skip the word if word length < 2, word contains number or word is a stopword
            word_size = len(word)
            if word_size < 2 or word in stopwords or self._check_word_has_number(word):
                continue

            # SUBPROCESS: add / update word (lowercase) into dictionary
            formatted_word = word.lower()
            if formatted_word not in words_dict.keys():
                words_dict[formatted_word] = 1
            else:
                words_dict[formatted_word] += 1

        # --- MAIN OUTPUT: return the result tuple (if the dictionary is not empty)
        return words_dict

    def _get_words(self, text: str, delimiters: str) -> list[str]:
        """
        This function extract a list of (lowercase) words from the input text.

        Args:
            text (str): the input text string.
            delimiters (str): the symbols / characters that should be filtered from the word.

        Returns:
            list[str]: a list of lowercase words.
        """
        words = []
        word_buffer = ""
        # iterate each character, form into a word and add to word list
        for char in text:
            # while buffer is empty, skip the character if it is a blank space or a delimiters
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

        return words

    def _check_word_has_number(self, word: str) -> bool:
        """
        This function check if a word contain a number (digit).

        Args:
            word (str): the word to be checked.

        Returns:
            bool: a boolean check if that function has a number or not.

        """
        for char in word:
            if char.isdigit():
                return True

        return False

    def _load_idx2label(self, filepath):
        """
        Load the file containing indexes and their labels.
        Args:
            filepath (str):  path of the idx2label file.
        Returns:
            pd.DataFrame: DataFrame mapping label ids to label names.
        """
        with open(filepath) as f:
            mapping_dict = json.load(f)
        label_df = pd.DataFrame(mapping_dict.items(), columns=["label", "label_name"])
        return label_df

    # ========== GETTERS & SETTERS ==========
    def get_word_freq(self) -> Dict[str, int]:
        """
        Get the word frequency.
        Returns:
            Dict[str, int]: A dictionary contain words and its amount.
        """
        return self.word_freq

    def set_word_freq(self, word_freq: Dict[str, int]) -> None:
        """
        Set the word frequency.
        Args:
            word_freq (Dict[str, int]): a dictionary contain words and its amount which want to set.

        Returns:
            This function does not return anything.
        """
        self.word_freq = word_freq

    def get_word2idx(self) -> Dict[str, int]:
        """
        Get the word2idx.
        Returns:
            Dict[str, int]: A dictionary contain words and its index.
        """
        return self.word2idx

    def set_word2idx(self, word2idx: Dict[str, int]) -> None:
        """
        Set the word2idx.
        Args:
            word2idx (Dict[str, int]): a dictionary contain words and its index.

        Returns:
            This function does not return anything.
        """
        self.word2idx = word2idx

    def get_idx2word(self) -> Dict[int, str]:
        """
        Get the idx2word.
        Returns:
            Dict[int, str]: A dictionary contain indexes and words.
        """
        return self.idx2word

    def set_idx2word(self, idx2word: Dict[int, str]) -> None:
        """
        Set the idx2word.
        Args:
            idx2word (Dict[int, str]): a dictionary contain indexes and words.

        Returns:
            This function does not return anything.
        """
        self.idx2word = idx2word

    def get_stopwords(self) -> list[str]:
        """
        Get the stopwords.
        Returns:
            list[str]: a list of strings (the stop words).
        """
        return self.stopwords

    def set_stopwords(self, stopwords: list[str]) -> None:
        """
        Set the stopwords.
        Args:
            stopwords (list[str]): a list of strings (the stop words).
        Returns:
            This function does not return anything.
        """
        self.stopwords = stopwords


if __name__ == "__main__":
    tp = TextProcessor(
        stopwords_filepath="data/stop_words_english.txt",
        corpus_filepath="data/ag_news_test.csv",
        idx2label_filepath="data/idx2label.json",
    )
    print(len(tp.word_freq))
    print(tp.corpus)
