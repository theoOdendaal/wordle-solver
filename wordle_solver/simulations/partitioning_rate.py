from tqdm import tqdm

class PartitioningRateSolver:
    
    def __init__(self, population: list[str]) -> None:
        self.population = population
        
    def solve(self) -> list[float]:
        self.results = []
        for base_word in tqdm(self.population): # Answer
            remaining_population = []
            
            for iter_word in self.population: # Guess
                residual_population = self.population
                
                for i, (a, b) in enumerate(zip(base_word, iter_word)):
                    if a == b:
                        residual_population = [word for word in residual_population if word[i] == a]
                    elif b in a:
                        residual_population = [word for word in residual_population if b in word and word[i] != b]
                    else:
                        residual_population = [word for word in residual_population if word[i] != b]
                
                remaining_population.append(len(residual_population))
            self.results.append(sum(remaining_population) / len(remaining_population))

        return self.results
