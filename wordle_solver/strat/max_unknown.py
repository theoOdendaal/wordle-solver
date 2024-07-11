import pandas as pd
from collections import Counter

class MaxUnknown:
    
    @staticmethod
    def organize(word_list: list[str], word_length: int) -> pd.DataFrame:
        char_count = Counter("".join(word_list))
        char_sum = sum(char_count.values())
        char_count = {char: val / char_sum for char, val in char_count.items()}
        
        unique_chars = [len(set(word)) for word in word_list]
        char_coverage = [sum([char_count.get(char) for char in word]) for word in word_list]
        
        new_words = [[word, unique_count, coverage] for word, unique_count, coverage in zip(word_list, unique_chars, char_coverage)]
        
        new_words = sorted(new_words, key=lambda x: (x[1], x[2]), reverse=True)
        
        new_words = pd.DataFrame(new_words, columns=['word', 'unique_count', 'coverage'])
        
        return new_words
        
        