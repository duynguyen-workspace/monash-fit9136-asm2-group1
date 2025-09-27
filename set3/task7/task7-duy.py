import pandas as pd
import json
from typing import Dict, List

class TextProcessor:
    """ TextProcessor class """
    
    def __init__(
        self,
        stopwords_filepath: str,
        corpus_filepath: str,
        idx2label_filepath: str
        ) -> None:
        """

        """

        # Instance variables
        self.word_freq = {}
        self.word2idx = {}
        self.idx2word = {}
        self.idx2label = None
        self.corpus = None

        # Initialize corpus, concatenate all texts and generate vocabulary list
        self._init_corpus(corpus_filepath, idx2label_filepath)
        
        self._set_stopwords(stopwords_filepath)
        self.corpus_text = ' '.join(self.corpus["text"])
        self.word_freq = self._get_word_freq(self.corpus_text, self.stopwords)

        # Update word2idx & idx2word dictionaries
        word_lst = list(self.word_freq.keys())
        word_lst.sort()

        for index, word in enumerate(word_lst):
            self.word2idx[word] = index
            self.idx2word[index] = word


    def add_file(self, add_file_path: str) -> None:
        """
        """
        if not add_file_path:
            return None
        
        # 
        new_df = pd.read_csv(add_file_path)
        # check if df is empty

        new_corpus_text = ' '.join(new_df['text'])
        new_word_freq = self._get_word_freq(new_corpus_text, self.stopwords)

        for curr_word, curr_freq in new_word_freq.items():
            if curr_word in self.word_freq.keys():
                self.word_freq[curr_word] += int(curr_freq)
            else:
                self.word_freq[curr_word] = int(curr_freq)
        
        # Overwrite current files 
        self.save()


    def delete_file(self, delete_file_path) -> None:
        # YOUR CODES START HERE
        if delete_file_path is None:
            return None
        
        # 
        new_df = pd.read_csv(delete_file_path)
        new_corpus_text = ' '.join(new_df['text'])
        new_word_freq = self._get_word_freq(new_corpus_text, self.stopwords)

        for curr_word, curr_freq in new_word_freq.items():
            if curr_word in self.word_freq.keys():
                new_freq_value = self.word_freq[curr_word] - int(freq[idx])

                if new_freq_value <= 0:
                    self.word_freq.pop(curr_word)
                else:
                    self.word_freq[curr_word] -= int(curr_freq)
        
        # Overwrite current files 
        self.save()


    def load(self) -> None:
        """
        """
        self._load_word_freq()
        self._load_word2idx()
        self._load_idx2word()

    def save(self) -> None:
        """
        """
        self._save_word_freq()
        self._save_word2idx()
        self._save_idx2word()

    # ========== LOAD FILES FUNCTIONS ==========
    def load_idx2label(self, idx2label_filepath: str = 'data/idx2label.json'):
        """
        """
        with open(idx2label_filepath) as f:
            mapping_dict = json.load(f)
        label_df = pd.DataFrame(mapping_dict.items(), columns=["label", "label_name"])
        return label_df

    def _load_word_freq(self, file_path: str = 'word_freq.txt') -> dict:
        """
        """
        word_freq_dict = {}
        with open(file_path, "r") as f:
            for line in f:
                word, freq = line.split()
                word_freq_dict[word] = int(freq)
    
        self.word_freq = word_freq_dict

    def _load_word2idx(self, file_path: str = 'word2idx.txt') -> dict:
        """
        """
        word2idx_dict = {}
        with open(file_path, "r") as f:
            for line in f:
                word, idx = line.split()
                word2idx_dict[word] = int(idx)
        
        self.word2idx = word2idx_dict


    def _load_idx2word(self, file_path: str = 'idx2word.txt') -> dict:
        """
        """
        idx2word_dict = {}
        with open(file_path, "r") as f:
            for line in f:
                idx, word = line.split()
                idx2word_dict[int(idx)] = word
        
        self.idx2word = idx2word_dict

    # ========== SAVE FILES FUNCTIONS ==========
    def _save_word_freq(self, file_path: str = 'word_freq.txt') -> None:
        """
        """
        # PROCESS: No file created if word or freq tuple is empty, and word + freq tuples has different size 
        if self.word_freq is None or len(self.word_freq) == 0: 
            return

        # PROCESS: write a new line for each word with the following format: word<space>frequency
        with open(file_path, "w") as f:
            for word, freq in enumerate(self.word_freq):
                f.write(f"{word} {freq}\n")

    def _save_word2idx(self, file_path: str = 'word2idx.txt') -> None:
        """
        """
        # PROCESS: No file created if word or freq tuple is empty, and word + freq tuples has different size 
        if self.word_freq is None or len(self.word_freq) == 0: 
            return
        
        with open(file_path, "w") as f:
            for word, index in enumerate(self.word2idx):
                f.write(f"{word} {index}\n")

    def _save_idx2word(self, file_path: str = 'idx2word.txt') -> None:
        """
        """
        # PROCESS: No file created if word or freq tuple is empty, and word + freq tuples has different size 
        if self.word_freq is None or len(self.word_freq) == 0: 
            return
        
        with open(file_path, "w") as f:
            for word, index in enumerate(self.word2idx):
                f.write(f"{index} {word}\n")
                
    # ========== PUBLIC HELPERS ===========
    def extract_word_freq(self, text: str, stopwords: List[str]) -> Dict[str, int]:
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
        if len(words_dict) != 0:
            return words_dict

    # ========== PRIVATE HELPERS ==========
    def _init_corpus(self, corpus_filepath: str, idx2label_filepath: str) -> None:
        """
        Initialise corpus and create a new column: "label_name" (mapping from json file)
        """
        self.corpus = pd.read_csv(corpus_filepath)

        with open(idx2label_filepath, "r") as f:
            labels = json.load(f)
        
        self.corpus['label_name'] = self.corpus['label'].astype(str).map(labels).fillna('Unknown')

        # print(repr(self.corpus))

    def _set_stopwords(self, stopwords_filepath: str) -> None:
        """
        This function gets all the stop words from the file and update to the instance variable stopwords

        Params:
            1. stopwords_file: <str> the file name containing the stop words

        Return:
            stopwords: <list> a list of strings (the stop words)
        """
        stopwords = []

        with open(stopwords_filepath, "r") as f:
            for line in f:
                word = line.strip().lower()
                stopwords.append(word) 

        self.set_stopwords(stopwords)
         
    def _get_words(self, text: str, delimeters: str) -> list:
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

    def _check_word_has_number(self, word: str) -> bool:
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

    # ========== GETTERS & SETTERS ==========
    def get_word_freq(self) -> Dict[str, int]:
        """Getter for word_freq dictionary."""
        return self.word_freq
    
    def set_word_freq(self, word_freq: Dict[str, int]) -> None:
        """Setter for word_freq dictionary."""
        self.word_freq = word.freq
    
    def get_word2idx(self) -> Dict[str, int]:
        """Getter for word2idx dictionary."""
        return self.word2idx
    
    def set_word2idx(self, word2idx: Dict[str, int]) -> None:
        """Setter for word2idx dictionary."""
        self.word2idx = word2idx
    
    def get_idx2word(self) -> Dict[int, str]:
        """Getter for idx2word dictionary."""
        return self.idx2word
    
    def set_idx2word(self, idx2word: Dict[int, str]) -> None:
        """Setter for idx2word dictionary."""
        self.idx2word = idx2word

    def get_stopwords(self) -> List[str]:
        """Getter for stopwords list."""
        return self.stopwords

    def set_stopwords(self, stopwords: List[str]) -> None:
        """Setter for stopwords list."""
        self.stopwords = stopwords
    

if __name__ == "__main__":
    
    tp = TextProcessor(
        stopwords_filepath="data/stop_words_english.txt",
        corpus_filepath="data/ag_news_test.csv",
        idx2label_filepath="data/idx2label.json",
    )
    