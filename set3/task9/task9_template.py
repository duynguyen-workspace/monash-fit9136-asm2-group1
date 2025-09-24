from task7 import TextProcessor
import math

class EssayScorer:
    def __init__(self, text_processor):
        pass

    def score_essay(self, prob_statement, file_path):
        pass

if __name__ == "__main__":
    tp = TextProcessor(
        stopwords_filepath="data/stop_words_english.txt",
        corpus_filepath="data/ag_news_test.csv",
        idx2label_filepath="data/idx2label.json",
    )
    scorer = EssayScorer(tp)
    prob_statement = "The impact of technology on education."
    score = scorer.score_essay(prob_statement, "/home/sample_essay.txt")
    print(score)

