from pathlib import Path
from turtle import position
from types import new_class
import pandas as pd
import numpy as np

from collections import Counter


pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)

# Constants
WORD_LENGTH = 5


def organize_words(word_list : list):
    # Strategically organizes words based on various metrics    
    vowels = set("aeiou")

    # Determines which is the most frequent char for each position
    position_metrics = [{key: value / sum(Counter(k[i] for k in word_list).values()) for key, value in Counter(k[i] for k in word_list).items()} for i in range(WORD_LENGTH)]
    
    # Determines how frequently each letter occurs in the population, without considering the population.
    #char_counter = Counter("".join(word_list))
    #total_occurrence = sum(char_counter.values())
    #normalized_occurrence = {key: value / total_occurrence for key, value in char_counter.items()}
    #occurrence_metrics = [np.prod([normalized_occurrence.get(k) for k in word]) for word in word_list]

    # The order is which columns are given preference in the sorting process is based on the position that contains the highest concentrated probability.
    #pos_rank = np.argsort([min(k.values()) for i, k in enumerate(position_metrics) if i > 1])[::-1]
    
    # Determines the number of unique characters in each word
    unique_characters = [len(set(k)) for k in word_list]
    
    # Determines the number of vowels in eahc word
    vowel_count = [sum(1 for letter in word if letter in vowels) for word in word_list]
    
    # Links the position metrics with the word list
    organize_metrics = [[b.get(a[i], 0) for i, b in enumerate(position_metrics)] for a in word_list]
        
    # Combines the word list and organize_metrics
    new_words = [[word, uniq, vow, *metrics] for word, uniq, metrics, vow in zip(word_list, unique_characters, organize_metrics, vowel_count)]
    #new_words = [[word, uniq, occ, vow, *metrics] for word, uniq, occ, metrics, vow in zip(word_list, unique_characters, occurrence_metrics, organize_metrics, vowel_count)]
    # Sorts the list based on all the metrics
    # 1 = Unique characters
    # 2 = Number of vowels
    # 3 = Pos 1
    # 4 = Pos 2
    # 5 = Pos 3
    # 6 = Pos 4
    # 7 = Pos 5
    
    new_words = sorted(new_words, key=lambda x: (x[1], x[3], x[4], x[6], x[5], x[7], x[2]), reverse=True)
    #new_words = sorted(new_words, key=lambda x: (x[1], x[3], x[4], x[2], x[pos_rank[2]], x[pos_rank[1]], x[pos_rank[0]]), reverse=True)

    # Converts the list to a dataframe, and returns the top 100 results
    new_words = pd.DataFrame(new_words, columns=['word', 'unique_chars', 'vowel_count', 'pos_1', 'pos_2', 'pos_3', 'pos_4', 'pos_5'])
    
    # Creates a new columns containing the probability of the word being correct
    #new_words['prob'] =     
    
    
    
    #new_words = new_words.loc[np.where(new_words['word'] == 'shape')]

    return new_words.head(10)
    
if __name__ == '__main__':
    
    # Imports the word text file
    script_path = Path(__file__).parent.absolute()
    file_name = 'words.txt'
    df_words = pd.read_csv(Path(script_path, file_name), sep = '|')
    df_words = df_words.astype(str)
    
    # Removes words with digits and special characters
    df_words = df_words[~df_words['word'].str.contains(r'\d|[^\w]')].reset_index(drop=True)
    
    # Lower case the word column and removes whitespaces
    df_words['word'] = df_words['word'].str.lower().str.strip()
    
    # Remove all words not of the desired length
    df_words = df_words[df_words['word'].str.len() == WORD_LENGTH]
    
    print(organize_words(df_words['word'].tolist()))
    
    while True:    

        # Obtains user input relating to the last guess
        last_guess = input('Last guess: ').lower()
        correct_letters = input('Which characters are correct irrespective of their position: ')
        correct_position = input('Which characters are in the correct position: ')
        if len(correct_position) == 0:
            correct_position = '-' * WORD_LENGTH

        # Filters the words population, based on those that incorrect
        correct_letters_counter = Counter(correct_letters)

        for i, k in enumerate(last_guess):
                if k in set(correct_letters):
                    if k == correct_position[i]:
                        df_words = df_words[df_words['word'].str[i] == k].reset_index(drop = True)
                    else:
                        cl_count = correct_letters_counter.get(k, 0)
                        # Add logic that filters if the letter count in the word column is the same as the cl_count !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        df_words = df_words[df_words['word'].str.contains(k)].reset_index(drop = True)
                        df_words = df_words[df_words['word'].str[i] != k].reset_index(drop = True)
                else:
                    df_words = df_words[~df_words['word'].str.contains(k)].reset_index(drop = True)
    
        print(organize_words(df_words['word'].tolist()))
        