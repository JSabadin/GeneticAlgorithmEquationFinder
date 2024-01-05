import random
import re

def replace_operators(string):
    # Dictionary with possible operators combinations to replace
    operators = {"++": "+", "--": "+",
                 "**": "*", "//": "/",
                 "/*": "/", "*/": "*",

                 "+-" : "-", "-+":"-",
                 "-/" : "-", "/-":"/", 
                 "+/" : "+", "/+" :"/",
                 "+*":"+", "*+":"*",
                 "-*":"-","*-":"*",
                 "+-":"-", "-+": "-"
                    }
    for op in operators:
        if op in string:
            string = string.replace(op, operators[op])
    return string



class GA:
    def __init__(self, max_terms, target):
        self.max_terms = max_terms
        self.target = target 
        self.min_num = 1
        self.max_num =  int(target)
        self.pop_size = 1000
        self.num_iter = 200
        self.crossover_rate = 0.7
        self.mutation_rate = 0.2
        self.max_fitness = 100

        if self.max_terms == 1:
            self.max_num = self.target * 2


    def population_init(self):
        # Creating population of random equations
        self.pop = []
        for i in range(self.pop_size):
            equation = ""
            num_terms = self.max_terms
            for j in range(num_terms):
                term =  str(random.randint(self.min_num, self.max_num))
                if j == 0:
                   equation += "+" + term 
                else:
                    operator = random.choice(["+","-","*","/"])
                    equation += operator + term
            self.pop.append(equation) 

    
    def fitness_fun(self, equation):
        # Fitness function, which returns higher value for a equation with a result closer to the target
        try: 
            # eval() returns the result of the equation
            result = eval(equation)
            fitness = 1 / (abs(result - self.target) + 1/self.max_fitness)
        except:
            # If dividing by 0
            fitness = 0

        # If there are more numbers in equations then max_terms -> fitness is set to 0
        pattern = r'\d+'  # regular expression pattern to match digits
        matches = re.findall(pattern, equation) # Array of all the numbers in equation
        if len(matches) > self.max_terms:
            fitness = 0
        return fitness


    def selection(self,pop, fits):
        # Uses roulette wheel
        total_fit = sum(fits)
        sel_probs = [f / total_fit for f in fits]
        selected = []
        while len(selected) < len(pop):
            pick = random.uniform(0, 1)
            comulative_prob = 0
            for i, prob in enumerate(sel_probs):
                # Iterate over the individuals in the population, summing their selection probabilities until the cumulative probability exceeds the random generated number (pick).
                comulative_prob += prob
                if comulative_prob > pick:
                    # The comulative probability is higher then randomly generated number between 0 and 1
                    selected.append(pop[i])
                    break
        return selected

    def crossover(self, parent1, parent2):
        if random.uniform(0, 1) < self.crossover_rate:
            # We limit the cutting point
            min_len  = min(len(parent1), len(parent2))
            try:
                cuting_point = random.randint(0, min_len)
                child1 = parent1[:cuting_point] + parent2[cuting_point:]
                child2 = parent2[:cuting_point] + parent1[cuting_point:]
                #  replacing operators according to the dictionary ++,--,**,// ,...
                child1 = replace_operators(child1)
                child2 = replace_operators(child2)
                return child1, child2
            # Case when self.max_term = 1
            except: 
                return parent1, parent2
        else:
            return parent1, parent2
        

    
    def mutate_number_in_string(self, match):
        # This function is used as a tool in function mutation
        # It was made so the numbers in equation could change for example from 99 to 101.
        # So the mutation wouldnt cause too big change of phenotype  
        # It is mutating a number in a equation in a way that is adding or substracting some rand. int from it
        int_val = int(match.group(0))
        if random.random() < self.mutation_rate:
            new_val = int_val + random.randint(-2, 2)
            return str(new_val)
        else:
            return str(int_val)
    
    
    def mutation(self, individual):
        mutation = ""
        flag = 0 # for not mutating the first element for example +1 to *1.
        for element in individual:
            if (random.uniform(0, 1) < self.mutation_rate) & (not element.isnumeric()) &( flag != 0):
                mutation += random.choice(["+","-","*","/"])
            else: 
                mutation += element
            flag = 1
        mutation = replace_operators(mutation) # When we have //, or **,...
        # Mutating numbers in a equation. For example 199 could be transformed into 201.
        mutation = re.sub(r'\d+', self.mutate_number_in_string, mutation) #Replacing numbers in mutation string with respect to mutate_number_in_string()
        return mutation
    

    def evolve(self):
        # Initialising the random population of equations
        self.population_init()
        for i in range(self.num_iter):
            # Evaulating the population
            pop_fitness = [self.fitness_fun(equation) for equation in self.pop ]
            # Selecting the best individuals using the roulette wheel
            selected_pop = self.selection(self.pop,pop_fitness)
            # Defining new population
            new_pop = []
            while len(new_pop) < self.pop_size:
                # Choosing parents from best inviduals and cross their gens
                p1 = random.choice(selected_pop)
                p2 = random.choice(selected_pop)
                c1, c2 = self.crossover(p1,p2)
                # Perform mutations
                new_pop.append(self.mutation(c1))
                new_pop.append(self.mutation(c2))
            self.pop = new_pop
            best_eq = max(self.pop, key=self.fitness_fun)
            print("Iter", i+1, "Best equation:", best_eq, "Result:", eval(best_eq))
            if self.fitness_fun(best_eq) == self.max_fitness:
                final_iter = i + 1
                break

        best_eq = max(self.pop, key=self.fitness_fun)
        print("\n Final equation:", best_eq, "Result:", eval(best_eq))


import numpy as np

if __name__ == "__main__":
    # Defining Genetic alghorithm GA(Number of terms,Result we want)
    GA = GA(5, 33)
    GA.evolve()




