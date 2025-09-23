import pandas as pd
import json
from typing import Dict
import re
from typing import Tuple, List, Set, Optional


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
        self.stopwords = self.get_stopwords(stopwords_filepath)
        self.idx2label = self.load_idx2label(idx2label_filepath)
        self.add_file(corpus_filepath)

    def get_stopwords(self, stopwords_file: str) -> List[str]:
        """
        This function gets all the stop words from the file

        Args:
            1. stopwords_file: <str> the file name containing the stop words

        Return:
            stopwords: <list> a list of strings (the stop words)
        """
        stopwords = []

        with open(stopwords_file, "r",encoding="utf8") as f:
            for line in f:
                word = line.strip().lower()
                stopwords.append(word)

        return stopwords

    def load_idx2label(self, idx2label_filepath):
        with open(idx2label_filepath) as f:
            mapping_dict = json.load(f)
        label_df = pd.DataFrame(mapping_dict.items(), columns=["label", "label_name"])
        return label_df

    def add_file(self, add_file_path: str) -> None:
        # YOUR CODES START HERE
        word_find = re.compile(r"[a-zA-Z]+")

        self.corpus_df = pd.read_csv(add_file_path)
        self.idx2label["label"] = self.idx2label["label"].astype(int)

        corpus_table = self.corpus_df
        label_table = self.idx2label
        stopwords = self.stopwords

        joined_table = pd.merge(corpus_table, label_table, on="label", how="inner")

        texts = joined_table["text"]

        for text in texts:
            tokens = word_find.findall(text)
            for i in range(len(tokens)):
                tokens[i] = tokens[i].lower()
                if tokens[i] in stopwords or len(tokens[i]) < 2:
                    continue
                self.word_freq[tokens[i]] = self.word_freq.get(tokens[i], 0) + 1

        def get_frequency(word):
            return word[1]

        word_sorted_by_freq = sorted(self.word_freq.items(), key=get_frequency, reverse=True)
        word_sorted_by_name = sorted(self.word_freq.keys())

        for i, w in enumerate(word_sorted_by_name):
            self.word2idx[w] = i

        with open("word_freq.txt", 'w') as f:
            # use join with generator expression
            f.write("".join((f"{word} {freq}\n" for word, freq in word_sorted_by_freq)))

        with open("word2idx.txt", 'w') as f:
            # use join with generator expression
            f.write("".join(f"{word} {index}\n" for word, index in self.word2idx.items()))

    def delete_file(self, delete_file_path) -> None:
        # YOUR CODES START HERE
        pass

    def load(self) -> None:
        # YOUR CODES START HERE
        pass

    def save(self) -> None:
        # YOUR CODES START HERE
        pass


if __name__ == "__main__":
    tp = TextProcessor(
        stopwords_filepath="data/stop_words_english.txt",
        corpus_filepath="data/ag_news_test.csv",
        idx2label_filepath="data/idx2label.json",
    )
    print(len(tp.word_freq))