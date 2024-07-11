
class ResidualPotentialAnswers:
    
    def __init__(self, population: list[str]) -> None:
        self.population = population
        
    def filter(self, guess: str, guess_flag: list[int]) -> None:
        
        if len(guess) != len(guess_flag):
            raise IndexError("Lenght of char_flag should correspond to length of guess.")
        
        for i, (guess_char, flag) in enumerate(zip(guess, guess_flag)):
            if flag == 0:
                self.population = [word for word in self.population if word[i] != guess_char]
            elif flag == 1:
                self.population = [word for word in self.population if (guess_char in word) and (word[i] != guess_char)]
            elif flag == 2:
                self.population = [word for word in self.population if word[i] == guess_char]
                