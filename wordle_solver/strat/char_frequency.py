import pandas as pd
from collections import Counter

class WordFrequency:
    
    @staticmethod
    def organize(word_list: list, word_length: int) -> pd.DataFrame:   
        vowels = set("aeiou")

        # Determines which is the most frequent char for each position
        position_metrics = [{key: value / sum(Counter(k[i] for k in word_list).values()) for key, value in Counter(k[i] for k in word_list).items()} for i in range(word_length)]
        
        # Determines the number of unique characters in each word.
        unique_characters = [len(set(k)) for k in word_list]
        
        # Determines the number of vowels in each word.
        vowel_count = [sum(1 for letter in word if letter in vowels) for word in word_list]
        
        # Links the position metrics with the word list.
        organize_metrics = [[b.get(a[i], 0) for i, b in enumerate(position_metrics)] for a in word_list]
            
        # Combines the word list and organize_metrics
        new_words = [[word, uniq, vow, *metrics] for word, uniq, metrics, vow in zip(word_list, unique_characters, organize_metrics, vowel_count)]
        # Sorts the list based on all the metrics
        # 1 = Unique characters
        # 2 = Number of vowels
        # 3 = Pos 1
        # 4 = Pos 2
        # 5 = Pos 3
        # 6 = Pos 4
        # 7 = Pos 5
        new_words = sorted(new_words, key=lambda x: (x[1], x[3], x[4], x[6], x[5], x[7], x[2]), reverse=True)

        # Converts the list to a dataframe, and returns the top 10 results
        new_words = pd.DataFrame(new_words, columns=['word', 'unique_chars', 'vowel_count', 'pos_1', 'pos_2', 'pos_3', 'pos_4', 'pos_5'])

        return new_words