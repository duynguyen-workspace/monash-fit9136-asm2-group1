from task4 import get_stopwords, get_vocabs
from task5 import (
    load_word_freq, load_word2idx, load_idx2word,
    save_word_freq, save_word2idx, save_idx2word   
)

import os

def updating_for_adding(
        stopwords_path: str,
        added_files: str | list,
        in_path: str,
        out_path: str
    ):
    if isinstance(added_files, str):
        added_files = [added_files]
    stopwords = get_stopwords(stopwords_path)
    word_freq = load_word_freq(file_path=os.path.join(in_path, "word_freq.txt"))
    for element in added_files:
        with open(element, "r") as f:
            text = f.read()

        vocabs = get_vocabs(text=text, stopwords=stopwords)
        if not vocabs:
            continue  

        for w, c in zip(vocabs[0], vocabs[1]):
            word_freq[w] = word_freq.get(w, 0) + c


    words_list = list(word_freq.keys())
    freqs_list = [word_freq[w] for w in words_list]
    word = tuple(words_list)
    freq = tuple(freqs_list)
    save_word_freq(word, freq, os.path.join(out_path, "word_freq.txt"))
    save_word2idx(word, os.path.join(out_path, "word2idx.txt"))
    save_idx2word(word, os.path.join(out_path, "idx2word.txt"))
  


def updating_for_deleting(
        stopwords_path: str,
        excluded_files: str | list,
        in_path: str,
        out_path: str
    ):
    if isinstance(excluded_files, str):
        excluded_files = [excluded_files]
    stopwords = get_stopwords(stopwords_path)
    word_freq = load_word_freq(file_path=os.path.join(in_path, "word_freq.txt"))
    for element in excluded_files:
        with open(element, "r") as f:
            text = f.read()

        vocabs = get_vocabs(text=text, stopwords=stopwords)
        if not vocabs:
            continue  

        for w, c in zip(vocabs[0], vocabs[1]):
            if w in word_freq:
                new_val = word_freq[w] - c
                if new_val > 0:
                    word_freq[w] = new_val
                else:
                    word_freq.pop(w, None)


    words_list = list(word_freq.keys())
    freqs_list = [word_freq[w] for w in words_list]
    word = tuple(words_list)
    freq = tuple(freqs_list)
    save_word_freq(word, freq, os.path.join(out_path, "word_freq.txt"))
    save_word2idx(word, os.path.join(out_path, "word2idx.txt"))
    save_idx2word(word, os.path.join(out_path, "idx2word.txt"))



