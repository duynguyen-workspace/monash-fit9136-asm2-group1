import pandas as pd
import json
from typing import Dict, List, Optional

# CONSTANTS - file paths to write
WORD_FREQ_FILEPATH = "word_freq.txt"
WORD2IDX_FILEPATH = "word2idx.txt"
IDX2WORD_FILEPATH = "idx2word.txt"


class TextProcessor:
    """
    Text Processor Class - processing word in corpus.

    Instance Variables:
        1. word_freq (dict): The dictionary containing the words and their frequencies.
        2. word2idx (dict): The dictionary containing the words and their indexes.
        3. idx2word (dict): The dictionary containing keys are indexes and values are words.
        4. stopwords (list): list of stop words.
        5. idx2label (pandas.DataFrame): DataFrame mapping label ids to label names.
        6. corpus (pandas.DataFrame): DataFrame of all the text data, 
        containing 4 columns: id, text, label, label_name
        7.
    """

    def __init__(
            self,
            stopwords_filepath: str,
            corpus_filepath: str,
            idx2label_filepath: str
        ) -> None:
        # YOUR CODES START HERE
        """
        ========== TextProcessor Constructor ==========
        
        Initialise a new TextProcessor instance.

        Args:
            1. stopwords_filepath: Path of the stop words file.
            2. corpus_filepath: Path of the corpus file.
            3. idx2label_filepath: Path of the idx2label file.
            
        Returns:
            None
        """
        # Initialise instance variables
        self.word_freq = {}
        self.word2idx = {}
        self.idx2word = {}
        
        # Extract stopwords, idx2label, and corpus texts
        self.stopwords = self.extract_stopwords(stopwords_filepath)
        self.idx2label = self._load_idx2label(idx2label_filepath)
        self.corpus = self._get_corpus(corpus_filepath, self.idx2label)
        
        # Update word_freq from the extracted corpus texts
        self._add_freq_to_wordfreq(self.corpus["text"])
        
        # Update word2idx and idx2word dictionaries
        self._update_word_idx_dicts()

    
    # ========== ADD FILE FUNCTION WITH PRIVATE HELPER ==========
    def add_file(self, add_file_path: str) -> None:
        # YOUR CODES START HERE
        """
        This function add new words from a file, update its frequency accordingly and overwrite 
        the saved files to match with the updated word_freq.
        
        Args:
            add_file_path (str): The path of the file containing the added words.

        Returns:
            This function does not return anything. It saves the vocabulary and word frequency by save method.
        """
        # Extract the corpus text to add / update from the text file
        added_corpus = self._get_corpus(corpus_filepath=add_file_path, label_df=self.idx2label)
        corpus_texts = added_corpus["text"]
        
        # Add word / Update word frequencies and overwrite files
        self._add_freq_to_wordfreq(corpus_texts)
        self.save()
        

    def _add_freq_to_wordfreq(self, corpus_texts) -> None:
        """
        This function update the word frequency of TextProcessor when initiating instance or adding file.
        Args:
            texts (Iterable[str]): A list or pandas Series of text documents to be processed.

        Returns:
            This function return nothing. It is used for updating word frequency.
        """
        added_text = ' '.join(corpus_texts)
        added_word_freq = self.extract_wordfreq(text=added_text, stopwords=self.stopwords)
        
        if not added_word_freq:
            return None

        # Insert / Update freq value for each vocab into the word_freq dictionary
        for vocab, freq in added_word_freq.items():
            self.word_freq[vocab] = self.word_freq.get(vocab, 0) + freq
    
    # ========== DELETE FILE FUNCTION WITH PRIVATE HELPER ==========
    def delete_file(self, delete_file_path) -> None:
        # YOUR CODES START HERE
        """
        Delete the words frequency from a delete file and save the vocabulary and word frequency.
        
        Args:
            delete_file_path: The path of the file containing the deleted words.

        Returns:
            This function does not return anything. It saves the vocabulary and word frequency by save method.
        """
        if delete_file_path is None:
            return None
        
        deleted_corpus = self._get_corpus(corpus_filepath=delete_file_path, label_df=self.idx2label)
        deleted_texts = deleted_corpus["text"]

        # Delete word / update word frequencies and overwrite files
        self._delete_freq_from_wordfreq(deleted_texts)
        self.save()
        
    def _delete_freq_from_wordfreq(self, corpus_texts) -> None:
        """
        This function update the word frequency of TextProcessor when deleting file.
        
        Args:
            texts (Iterable[str]): A list or pandas Series of text documents to be processed.

        Returns:
            This function return nothing. It is used for updating word frequency.
        """
            
        deleted_text = ' '.join(corpus_texts)
        deleted_word_freq = self.extract_wordfreq(text=deleted_text, stopwords=self.stopwords)
        
        if not deleted_word_freq:
            return None

        #         
        for word, freq in deleted_word_freq.items():
            if word in self.word_freq.keys():
                new_freq = self.word_freq[word] - freq
                
                # Remove word from dictionary if the new freq drop to 0 or below
                if new_freq > 0:
                    self.word_freq[word] = new_freq
                else:
                    self.word_freq.pop(word, None)

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
    
    # ========== LOAD FILE FUNCTION WITH PRIVATE HELPERS ==========
        
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
    
    # ========== SAVE FILE FUNCTION WITH PRIVATE HELPERS ==========
    def save(self) -> None:
        """
        Save the vocabulary and word frequency , word2idx, and idx2word to
        word_freq.txt, word2idx.txt, and idx2word.txt.

        Returns:
            This function does not return anything. It save the vocabulary and word frequency.
        """
        # Update word2idx and idx2word dictionaries to prevent duplications
        self._update_word_idx_dicts()

        # Save 3 files
        self._save_word_freq(WORD_FREQ_FILEPATH)
        self._save_word2idx(WORD2IDX_FILEPATH)
        self._save_idx2word(IDX2WORD_FILEPATH)

    def _save_word_freq(self, filepath: Optional[str] = 'word_freq.txt') -> None:
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
            List[tuple]: a list of tuple (word, frequency).
        """

        # This closure function to get key in the element of iterator for sorting
        def get_frequency(element):
            return element[1]

        word_sorted_by_freq = sorted(self.word_freq.items(), key=get_frequency, reverse=True)
        return word_sorted_by_freq

    # ==================== PUBLIC HELPERS ====================
    
    def extract_stopwords(self, stopwords_file: str) -> List[str]:
        """
        This function gets all the stopwords from the file.

        Args:
            stopwords_file (str): the file name containing the stop words.

        Returns:
            List[str]: a list of strings (the stop words).
        """
        stopwords = []

        with open(stopwords_file, "r") as f:
            for line in f:
                word = line.strip().lower()
                stopwords.append(word)

        return stopwords

    def extract_wordfreq(self, text: str, stopwords: list[str]) -> Dict[str, int]:
        """
        This function splits the text into words and count number of time each word appears.
        Exclude any word that is a stopword

        Args:
            text (str): the unformatted text string.
            stopwords (list[str]): Words to be filtered out.

        Returns:
            Dict[str, int]: A dictionary contain words and its amount.
        """
        if not text:
            return {}

        # process the text, extract the word list and generate a dictionary containing word count
        words = self._get_words(text)
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
        return words_dict

    # ==================== PRIVATE HELPERS ====================
    def _get_corpus(self, corpus_filepath: str, label_df: pd.DataFrame) -> pd.DataFrame:
        """
        This function process the merging of the label dataframe and corpus dataframe 
        and return the existing corpus with a new column: label_name
        
        Args:
            1. corpus_filepath (str):  Path of the corpus file.
            2. label_df (pandas.DataFrame): Label data frame.

        Returns:
            pandas.DataFrame: Corpus dataframe after join, with a label_name column.
        """
        # Cast the datatype of label column in label dataframe to int same data type with corpus
        label_df["label"] = label_df["label"].astype(int)
        corpus_df = pd.read_csv(corpus_filepath)
        
        # Merge corpus and label dataframe
        joined_df = pd.merge(corpus_df, label_df, on="label", how="inner")
        return joined_df
    
    def _update_word_idx_dicts(self) -> None:
        """
        This function clear the existing data in word2idx and idx2word dictionaries,
        and update its content based on the current word_freq to prevate duplicate data
        
        Args:
            None
            
        Returns:
            None -> This function directly update the 2 instance variables
        """    
        # Clear all data in word2idx and idx2word for preventing duplicate with old data
        self.word2idx.clear()
        self.idx2word.clear()

        # Update word2idx & idx2word dictionaries, store content in alphebetical order
        word_sorted_by_name = sorted(self.word_freq.keys())

        for index, word in enumerate(word_sorted_by_name):
            self.word2idx[word] = index
            self.idx2word[index] = word
    
    def _get_words(self, text: str) -> List[str]:
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

                if len(word) >= 2 and not self._check_word_has_number(word):
                    words.append(word)
                    
                word_buffer = "" # reset buffer
            
        # Add the remaining buffer (last word) to list (must satisfy requirements)
        if word_buffer and len(word_buffer) >= 2 and not self._check_word_has_number(word_buffer):
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

    # ==================== GETTERS & SETTERS ====================
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

    def get_stopwords(self) -> List[str]:
        """
        Get the stopwords.
        
        Returns:
            List[str]: a list of strings (the stop words).
        """
        return self.stopwords

    def set_stopwords(self, stopwords: List[str]) -> None:
        """
        Set the stopwords.
        
        Args:
            stopwords (List[str]): a list of strings (the stop words).
            
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
