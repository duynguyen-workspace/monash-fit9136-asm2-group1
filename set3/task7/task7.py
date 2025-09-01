import pandas as pd
import json
from typing import Dict


class TextProcessor:
    
    def __init__(
        self,
        stopwords_filepath: str,
        corpus_filepath: str,
        idx2label_filepath: str
        ) -> None:
        # YOUR CODES START HERE
        pass
        
    def add_file(self, add_file_path: str) -> None:
        # YOUR CODES START HERE
        pass

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
    
    tp = TextProcessing(
        stopwords_filepath="data/stop_words_english.txt",
        corpus_filepath="data/ag_news_test.csv",
        idx2label_filepath="data/idx2label.json",
    )
    
