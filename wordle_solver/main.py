from pathlib import Path
import pandas as pd
import re

# Custom modules
from population import ResidualPotentialAnswers
from strat.char_frequency import WordFrequency
from strat.max_unknown import MaxUnknown
from simulations.partitioning_rate import PartitioningRateSolver

pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)

# Constants
WORD_LENGTH = 5

def initial_transformation(words: list[str], word_length: int) -> list[str]:
    words = [word.lower().strip() for word in words]
    words = [word for word in words if re.fullmatch(r'\w+', word) and len(word) == word_length]
    return words
  
if __name__ == '__main__':
    
    # Imports the word text file
    script_path = Path(__file__).parent.absolute()
    file_name = 'words.txt'
    df_words = pd.read_csv(Path(script_path, file_name), sep = '|')
    df_words = df_words.astype(str)
    
    #model = PartitioningRateSolver(df_words['word'].tolist())
    #model.solve()
    #results = [[key, val] for key, val in zip(model.population, model.results)]
    #results = sorted(results, key=lambda x: (x[1]))
    #print(results)
    #input("")
    
    organize_method = MaxUnknown
    residual_method = ResidualPotentialAnswers
    
         
    population = initial_transformation(df_words['word'].tolist(), WORD_LENGTH)
    population = residual_method(population=population)
    print(organize_method.organize(population.population, word_length=WORD_LENGTH).head(10))
    
    while True:
        
        last_guess = input('Last guess: ').lower()
        char_flag = [int(char) for char in input("Char flag: ")]

        population.filter(last_guess, char_flag)
        
        print(organize_method.organize(population.population, word_length=WORD_LENGTH).head(10))
    