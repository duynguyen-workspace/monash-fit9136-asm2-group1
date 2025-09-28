from task7 import TextProcessor
import math
from typing import Dict

class EssayScorer:
    """ EssayScorer Class - mark essay by the marking criteria
    
    Instance variable:
        1. text_processor: the object use to process text and extract words for 
        essay marking purpose
    """
    
    def __init__(self, text_processor):
        """
        ========== EssayScorer Constructor ==========
        
        Initializes an EssayScorer with a TextProcessor instance.

        Args:
            1. text_processor (TextProcessor): A text-processor object that provides methods for
            word extraction, frequency counting, and stopword retrieval (relevant to this Task).
        """

        self.text_processor = text_processor

    def score_essay(self, prob_statement: str, file_path: str) -> Dict[str, float]:
        """
        This function scores an essay based on the scoring criteria.

        Args:
            1. prob_statement (str): The given problem statement that contains the topic words for essay evaluation.
            2. file_path (str): The path to where the essay text file is located.

        Returns:
            Dict[str, float]: A dictionary with component scores (length, relevance, rarity, 
                variety, penalty) and the total score (all are rounded to 2 decimals).
        
        Requirements:
            The scoring criteria to be evaluate for an essay are:
            - 1/ Length check
            - 2/ Relevance
            - 3/ Word rarity
            - 4/ Variety score
            - 5/ Filler penalty
        """

        # Check if prob_statement and file_path exists
        if not prob_statement:
            print("Missing problem_statement parameter or it is empty!")
            return {}

        if not file_path:
            print("Missing file_path parameter!")
            return {}
        
        # Extract the essay text from the file_path
        with open(file_path, "r") as f:
            essay = f.read().strip()

        if not essay:
            print("Essay is not found!")
            return {
                'length': 0.0,
                'relevance': 0.0,
                'rarity': 0.0,
                'variety': 0.0,
                'penalty': 0.0,
                'total_score': 0.0
            }

        # Calculate and all the component score + the final total score
        length_score = self._get_length_score(essay)
        relevance_score = self._get_relevance_score(prob_statement, essay)
        rarity_score = self._get_rarity_score(essay)
        variety_score = self._get_variety_score(essay)
        penalty_score = self._get_filler_penalty(essay)

        total_score = length_score + relevance_score + rarity_score + variety_score + penalty_score

        return {
            'length': length_score,
            'relevance': relevance_score,
            'rarity': rarity_score,
            'variety': variety_score,
            'penalty': penalty_score,
            'total_score': total_score
        }

    # ========== MAIN FUNCTIONS ========== 
    def _get_length_score(self, essay: str) -> float:
        """ Scoring Criteria 1 - Length Check
        
        This function get the essay's word count and evaluates the score for length check.

        Args:
            1. essay (str): The essay text.

        Returns:
            length_score (float): The length score (between 0.0 and 10.0).
            (rounded to 2 decimals)

        Requirements:
            The length score will be evaluate if the word count is:
            - Case 0: empty essay
                --> 0 mark
            - Case 1: between 300 and 500 words 
                --> 10 marks
            - Case 2: Shorter than 300 words / Longer than 500 words
                --> 10% deduction for every 20 words under / overshoot, cap at 0
        """
        if len(essay) == 0:
            return 0.0
        
        # Count total words appear in the essay
        essay_word_freq = self.text_processor.extract_word_freq(essay, [])
        word_count = sum(essay_word_freq.values())
        
        # Calculate the score and penalties if word count is under / overshoot 
        if word_count >= 300 and word_count <= 500:
            return 10.0

        word_diff = 300 - word_count if word_count < 300 else word_count - 500 # word_count difference
        penalty = word_diff / 20 # deduct 10% for every 20 words
        length_score = max(0.0, 10.0 - penalty)

        return length_score
    
    def _get_relevance_score(self, prob_statement: str, essay: str) -> float:
        """ Scoring Criteria 2 - Relevance Check
        
        This function get the topic words (excluding stopwords) of problem statement,
        measure the essay relevance to it, and compute the relevance score.

        Args:
            1. prob_statement (str): The given problem statement that contains the topic words for essay evaluation.
            2. essay (str): The essay text.

        Returns:
            relevance_score (float): Relevance score between 0.0 and 40.0.
            (rounded to 2 decimals)

        Requirement: 
            - Case 1: all topic words appear at least 3 times
                --> 40 marks
            - Case 2: some topic words appear
                --> let X = sum of all topic word count appear (cap at 3), and Y = max point for total topic words
                relevance_score = 40 * (X / Y)
            - Case 3: no topic words appear
                --> 0 mark
        """
        if len(essay) == 0:
            return 0.0

        # Get the topic words list from the problem statement
        stopwords = self.text_processor.get_stopwords()
        statement_word_freq = self.text_processor.extract_word_freq(prob_statement, stopwords)
        topic_words = statement_word_freq.keys()
        
        # Get all the topic words and count their appearance in the essay text
        essay_word_freq = self.text_processor.extract_word_freq(essay, self.text_processor.get_stopwords())
        count_dict = {word: freq for word, freq in essay_word_freq.items() if word in topic_words}
        
        if not count_dict:
            return 0.0 

        # Compute the relevance score by the formula
        max_topic_words = len(topic_words) * 3
        found_topic_words = sum(min(3, count) for count in count_dict.values())

        relevance_score = round(40 * (found_topic_words / max_topic_words), 2)

        return relevance_score

    def _get_rarity_score(self, essay: str) -> float:
        """ Scoring Criteria 3 - Rarity Check
        
        This function count the number of unique words (excluding stopwords) in the essay,
        measure with the corpus words_freq dictionary, and calculate the rarity score.

        Args:
            1. essay (str): The essay text.

        Returns:
            rarity_score (float): Rarity score between 0.0 and 30.0.
            (rounded to 2 decimals)

        Requirements: 
            Points conversion for word frequency appearance:
            - 0: -1 mark (use of unknown word)
            - 1-3: 5 marks (rare word)
            - 4-20: 4 marks
            - 21-50: 3 marks
            - 51-100: 2 marks
            - > 100: 1 mark
        """
        if len(essay) == 0:
            return 0.0
        
        # Get the unique words list from the essay and the word list from the TextProcessor corpus
        essay_word_freq = self.text_processor.extract_word_freq(essay, self.text_processor.get_stopwords())
        unique_words = essay_word_freq.keys()

        corpus_word_freq = self.text_processor.get_word_freq()
        corpus_words = corpus_word_freq.keys()

        # Calculate the rarity point with corresponding mapping with the frequency-points table
        total_rarity_points = 0
        for word in unique_words:
            if word not in corpus_words:
                total_rarity_points -= 1
                continue
            
            freq = self.text_processor.word_freq.get(word)
            
            if freq >= 1 and freq <= 3:
                total_rarity_points += 5
            elif freq >= 4 and freq <= 20:
                total_rarity_points += 4
            elif freq >= 21 and freq <= 50:
                total_rarity_points += 3
            elif freq >= 51 and freq <= 100:
                total_rarity_points += 2
            elif freq > 100:
                total_rarity_points += 1

        if total_rarity_points <= 0:
            return 0.0
            
        total_unique_words_points = len(unique_words) * 3
        rarity_points = round(min(30, 30 * (total_rarity_points / total_unique_words_points)), 2)

        return rarity_points

    def _get_variety_score(self, essay: str) -> float:
        """ Scoring Criteria 4 - Variety Check
        
        This function count the number of unique words (excluding stopwords) and also total words in the essay,
        to calculate the variety score.

        Args:
            1. essay (str): The essay text.

        Returns:
            variety_score (float): Variety score between 0.0 and 20.0. 
            (rounded to 2 decimals)

        Requirements: 
            Let U = number of unique non-stopwords, L = total non-stopwords appear
            --> variety_score = 20 * math.sqrt(U / L)
        """
        if len(essay) == 0:
            return 0.0
        
        # Get the word_count for unique words and all words appear (excluding stopwords)
        essay_word_freq = self.text_processor.extract_word_freq(essay, self.text_processor.get_stopwords())
        unique_words_count = len(essay_word_freq.keys())
        total_words_count = sum(essay_word_freq.values())
        
        # Compute variety score by the formula
        variety_score = round(20 * math.sqrt((unique_words_count / total_words_count)), 2)

        return variety_score
    
    def _get_filler_penalty(self, essay: str) -> float:
        """ Scoring Criteria 5 - Filler Penalty
        
        This function count the number of stopwords in the essay, and
        calculate the penalty (if occured) based on the percentage of stopword appearance.

        Args:
            1. essay: (str) The essay text.

        Returns:
            float: The filler penality: 0.0 or 10.0. 

        Requirements: 
            Subtract 10 marks if 50% of essay are stopwords
        """
        if len(essay) == 0:
            return 0.0
        
        # Count the number of stopwords and total word_count of the essay
        essay_word_freq = self.text_processor.extract_word_freq(essay, [])
        stopwords = self.text_processor.get_stopwords()
        essay_stopwords_freq = {word: freq for word, freq in essay_word_freq.items() if word in stopwords}
        
        # Calculate the percentage of stopwords appearance and compute the penalty if appear over 50%
        essay_stopwords_count = sum(essay_stopwords_freq.values())
        total_word_count = sum(essay_word_freq.values())
        
        if essay_stopwords_count / total_word_count >= 0.5:
            return -10.0

        return 0.0

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
