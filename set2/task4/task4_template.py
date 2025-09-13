from typing import Tuple, List, Set, Optional
import os


def get_stopwords(stopwords_file: str) -> List[str]:
    pass


def get_vocabs(text: str, stopwords: List) -> Tuple[Tuple[str], Tuple[int]]:
    pass


def process_mini_dataset(
        stop_words: Set[str],
        data_path: str = 'data',
        category: Optional[str] = None,
    ):
    pass

# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    # your testing code goes here
    stopwords = get_stopwords("data/stop_words_english.txt")