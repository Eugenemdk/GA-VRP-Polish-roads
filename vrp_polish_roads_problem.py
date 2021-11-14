
#Metaheuristic method
import random
from random import randrange
from time import time 


#General representation of genetic class
# genetic algorithm. It includes the following attributes:
# - genes: list of possible genes in a chromosome
# - individuals_length: length of each chromosome
# - decode: method that receives the genotype (chromosome) as input and returns
#    the phenotype (solution to the original problem represented by the chromosome) 
# - fitness: method that returns the evaluation of a chromosome (acts over the
#    genotype)
# - mutation: function that implements a mutation over a chromosome
# - crossover: function that implements the crossover operator over two chromosomes
#=====================================================================================================================================

class Problem_Genetic(object):
    
    def __init__(self,genes,individ_length,decode,fitness):
        self.genes= genes
        self.individ_length= individ_length
        self.decode= decode
        self.fitness= fitness

    def mutation(self, chromosome, prob):
            
            def inverse_mutation(chromosome_aux):
                chromosome = chromosome_aux
                
                index_first = randrange(0,len(chromosome))
                index_second = randrange(index_first,len(chromosome))
                
                chromosome_mid = chromosome[index_first:index_second]
                chromosome_mid.reverse()
                
                chromosome_result = chromosome[0:index_first] + chromosome_mid + chromosome[index_second:]
                
                return chromosome_result
        
            aux = []
            for _ in range(len(chromosome)):
                if random.random() < prob :
                    aux = inverse_mutation(chromosome)
            return aux

    def crossover(self,parent_first, parent_sec):

        def process_gen_repeated(copy_child_first,copy_child2):
            count_first=0
            for gen_first in copy_child_first[:pos]:
                repeat = 0
                repeat = copy_child_first.count(gen_first)
                if repeat > 1:#If need to fix repeated gen
                    count_sec=0
                    for gen_sec in parent_first[pos:]:#Choose next available gen
                        if gen_sec not in copy_child_first:
                            child_first[count_first] = parent_first[pos:][count_sec]
                        count_sec+=1
                count_first+=1

            count_first=0
            for gen_first in copy_child2[:pos]:
                repeat = 0
                repeat = copy_child2.count(gen_first)
                if repeat > 1:#If need to fix repeated gen
                    count_sec=0
                    for gen_sec in parent_sec[pos:]:#Choose next available gen
                        if gen_sec not in copy_child2:
                            child_sec[count_first] = parent_sec[pos:][count_sec]
                        count_sec+=1
                count_first+=1

            return [child_first,child_sec]

        pos=random.randrange(1,self.individ_length-1)
        child_first = parent_first[:pos] + parent_sec[pos:] 
        child_sec = parent_sec[:pos] + parent_first[pos:] 
        
        return  process_gen_repeated(child_first, child_sec)
    
   
def decodeVRP(chromosome):    
    list=[]
    for (k,v) in chromosome:
        if k in cars[:(num_cars-1)]:
            list.append(frontier)
            continue
        list.append(cities.get(k))
    return list


def penalty_capacity(chromosome):
        actual = chromosome
        value_penalty = 0
        capacity_list = []
        index_cap = 0
        overloads = 0
        
        for i in range(0,len(cars)):
            init = 0
            capacity_list.append(init)
            
        for (k,v) in actual:
            if k not in cars:
                capacity_list[int(index_cap)]+=v
            else:
                index_cap+= 1
                
            if  capacity_list[index_cap] > capacity_trucks:
                overloads+=1
                value_penalty+= 100 * overloads
        return value_penalty

def fitnessVRP(chromosome):
    
    def distanceTrip(index,city):
        w = distances.get(index)
        return  w[city]
        
    actualChromosome = chromosome
    fitness_value = 0
   
    penalty_cap = penalty_capacity(actualChromosome)
    for (key,value) in actualChromosome:
        if key not in cars:
            nextCity_tuple = actualChromosome[key]
            if list(nextCity_tuple)[0] not in cars:
                nextCity= list(nextCity_tuple)[0]
                fitness_value+= distanceTrip(key,nextCity) + (50 * penalty_cap)
    return fitness_value



#  Here We defined the requierements functions that the Genetic algorithm needs to work with 
# The function receives as input:
# * problem_genetic: an instance of the class Problem_Genetic, with
#     the optimization problem that we want to solve.
# * k: number of participants on the selection tournaments.
# * opt: max or min, indicating if it is a maximization or a
#     minimization problem.
# * ngen: number of generations (halting condition)
# * size: number of individuals for each generation
# * ratio_cross: portion of the population which will be obtained by
#     means of crossovers. 
# * prob_mutate: probability that a gene mutation will take place.
#=====================================================================================================================================


def genetic_algorithm_t(Problem_Genetic,k,opt,ngen,size,ratio_cross,prob_mutate):
    
    def initial_population(Problem_Genetic,size):   
        def generate_chromosome():
            chromosome=[]
            for i in Problem_Genetic.genes:
                chromosome.append(i)
            random.shuffle(chromosome)
            return chromosome
        return [generate_chromosome() for _ in range(size)]
            
    def new_generation_t(Problem_Genetic,k,opt,population,n_parents,n_directs,prob_mutate):
        
        def tournament_selection(Problem_Genetic,population,n,k,opt):
            winners=[]
            for _ in range(n):
                elements = random.sample(population,k)
                winners.append(opt(elements,key=Problem_Genetic.fitness))
            return winners
        
        def cross_parents(Problem_Genetic,parents):
            childs=[]
            for i in range(0,len(parents),2):
                childs.extend(Problem_Genetic.crossover(parents[i],parents[i+1]))
            return childs
    
        def mutate(Problem_Genetic,population,prob):
            for i in population:
                Problem_Genetic.mutation(i,prob)
            return population
                        
        directs = tournament_selection(Problem_Genetic, population, n_directs, k, opt)
        crosses = cross_parents(Problem_Genetic,
                                tournament_selection(Problem_Genetic, population, n_parents, k, opt))
        mutations = mutate(Problem_Genetic, crosses, prob_mutate)
        new_generation = directs + mutations
        
        return new_generation
    
    population = initial_population(Problem_Genetic, size)
    n_parents = round(size*ratio_cross)
    n_parents = (n_parents if n_parents%2==0 else n_parents-1)
    n_directs = size - n_parents
    
    for _ in range(ngen):
        population = new_generation_t(Problem_Genetic, k, opt, population, n_parents, n_directs, prob_mutate)
    
    bestChromosome = opt(population, key = Problem_Genetic.fitness)
    print("Chromosome: ", bestChromosome)
    genotype = Problem_Genetic.decode(bestChromosome)
    print ("Solution: " , (genotype,Problem_Genetic.fitness(bestChromosome)))
    return (genotype,Problem_Genetic.fitness(bestChromosome))




# Modify the standard version of genetic algorithms developed in the previous step, by choosing only one of the following:
# Genetic Algorithm with Varying Population Size

def genetic_algorithm_t2(Problem_Genetic,k,opt,ngen,size,ratio_cross,prob_mutate,dictionary):
    
    def initial_population(Problem_Genetic,size):  
        
        def generate_chromosome():
            chromosome=[]
            for i in Problem_Genetic.genes:
                chromosome.append(i)
            random.shuffle(chromosome)
            #Adding to dictionary new generation
            dictionary[str(chromosome)]=1
            return chromosome
        
        return [generate_chromosome() for _ in range(size)]
            
    def new_generation_t(Problem_Genetic,k,opt,population,n_parents,n_directs,prob_mutate):
        def tournament_selection(Problem_Genetic,population,n,k,opt):
            winners = []
            for _ in range(int(n)):
                elements = random.sample(population,k)
                winners.append(opt(elements,key=Problem_Genetic.fitness))
            for winner in winners:
                #For each winner, if exists in dictionary, we increase his age
                if str(winner) in dictionary:
                    dictionary[str(winner)]=dictionary[str(winner)]+1
                else:
                    dictionary[str(winner)]=1
            return winners
        
        def cross_parents(Problem_Genetic,parents):
            childs=[]
            #Each time that some parent are crossed we add their two sons to dictionary 
            for i in range(0,len(parents),2):
                childs.extend(Problem_Genetic.crossover(parents[i],parents[i+1]))
                parent = str(parents[i])
                if parent not in dictionary:
                    dictionary[parent]=1
                    
                dictionary[str(childs[i])] = dictionary[parent]
                
                del dictionary[str(parents[i])]

            return childs
    
        def mutate(Problem_Genetic,population,prob):
            j = 0
            copy_population=population
            
            #Each time that some parent is crossed
            for crom in population:
                Problem_Genetic.mutation(crom,prob)
                
                parent = str(crom) 
                if parent in dictionary:
                    #We add the new chromosome mutated
                    dictionary[str(population[j])] = dictionary[parent]
                    
                    #remove old parent 
                    del dictionary[str(copy_population[j])]
                    j+=j
                    
            return population
        
        directs = tournament_selection(Problem_Genetic, population, n_directs, k, opt)
        crosses = cross_parents(Problem_Genetic,tournament_selection(Problem_Genetic, population, n_parents, k, opt))
        mutations = mutate(Problem_Genetic, crosses, prob_mutate)
        new_generation = directs + mutations
        
        #Adding new generation of mutants to dictionary.
        
        for ind in new_generation:
            age = 0
            crom = str(ind)
            if crom in dictionary:
                age+= 1
                dictionary[crom]+= 1
            else:
                dictionary[crom] = 1
        return new_generation
  
    population = initial_population(Problem_Genetic, size )
    n_parents= round(size*ratio_cross)
    n_parents = (n_parents if n_parents%2==0 else n_parents-1)
    n_directs = size - n_parents
    
    for _ in range(ngen):
        population = new_generation_t(Problem_Genetic, k, opt, population, n_parents, n_directs, prob_mutate)
        
    bestChromosome = opt(population, key = Problem_Genetic.fitness)
    print("Chromosome: ", bestChromosome)
    genotype = Problem_Genetic.decode(bestChromosome)
    print ("Solution:" , (genotype,Problem_Genetic.fitness(bestChromosome)),dictionary[(str(bestChromosome))] ," GENERATIONS.")
	
    return (genotype,Problem_Genetic.fitness(bestChromosome)
            + dictionary[(str(bestChromosome))]*50) #Updating fitness with age too
    

 

# Run over the same instances both the standard GA (from first part) as well as the modified version (from second part).
# Compare the quality of their results and their performance. Due to the inherent randomness of GA, the experiments performed over each instance should be run several times.
#====================================================================================================================================

def VRP(k):
    VRP_PROBLEM = Problem_Genetic([(0,10),(1,10),(2,10),(3,10),(4,10),(5,10),(6,10),(7,10),
                                   (cars[0],capacity_trucks)],
                                  len(cities), lambda x : decodeVRP(x), lambda y: fitnessVRP(y))
    
    def first_part_GA(k):
        cont  = 0
        print ("---------------------------------------------------------Executing FIRST PART of vrp --------------------------------------------------------- \n")
        print("Capacity of trucks = ",capacity_trucks)
        print("Frontier = ",frontier)
        print("")
        start_time_t2 = time()
        while cont <= k: 
            genetic_algorithm_t(VRP_PROBLEM, 2, min, 200, 100, 0.8, 0.05)
            cont+=1
        final_time_t2 = time()
        print("\n") 
        print("Total time: ",(final_time_t2 - start_time_t2)," secs.\n")
    
    def second_part_GA(k):
        print ("---------------------------------------------------------Executing SECOND PART: VRP --------------------------------------------------------- \n")
        print("Capacity of trucks = ",capacity_trucks)
        print("Frontier = ",frontier)
        print("")
        cont = 0
        tiempo_inicial_t2 = time()
        while cont <= k: 
            genetic_algorithm_t2(VRP_PROBLEM, 2, min, 200, 100, 0.8, 0.05,{})
            cont+=1
        tiempo_final_t2 = time()
        print("|n") 
        print("Total time: ",(tiempo_final_t2 - tiempo_inicial_t2)," secs.\n")
    
    
    first_part_GA(k)
    print("------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    second_part_GA(k)

#---------------------------------------- AUXILIARY DATA FOR TESTING --------------------------------
cities={0:'Bialostok',1:'Bielsko-Biala',2:'Chrzanow',
        3:'Gdansk',4:'Gdynia',5:'Gliwice',
        6:'Gromnik',7:'Katowice',8:'Kielce',
        9:'Krosno',10:'Krynica',11:'Lublin',
        12:'Lodz',13:'Malbork',14:'Nowy Targ',
        15:'Olsztyn',16:'Poznan',17:'Pulawy',
        18:'Radom',19:'Rzeszow',20:'Sandomierz',
        21:'Szczecin',22:'Szczucin',23:'Szklarska Poreba',
        24:'Tarnow',25:'Warsaw',26:'Wieliczka',
        27:'Wroclaw',28:'Zakopane',29:'Zamosc'
        }

#Distance between each pair of cities

w0 = [1,554,504,490,526,541,343,557,310,334,84,193,396,474,601,295,639,168,270,355,241,921,365,856,374,252,440,659,586,207]
w1 = [554,1,71,448,474,17,285,5,246,358,617,445,220,389,125,457,298,425,285,334,366,577,232,382,287,314,121,183,198,496]
w2 = [504,71,1,464,495,70,216,75,195,288,562,381,216,407,61,443,351,365,235,264,302,640,165,452,217,277,64,250,133,431]
w3 = [490,448,464,1,40,432,523,447,399,586,572,548,257,59,515,198,266,501,392,582,508,462,486,503,555,327,433,392,567,603]
w4 = [526,474,495,40,1,459,562,473,437,625,609,587,292,90,547,233,268,541,431,620,548,438,523,500,593,367,466,405,601,642]
w5 = [541,17,70,432,459,1,279,19,234,353,604,435,203,374,128,440,289,414,272,330,357,572,226,384,283,299,112,181,201,488]
w6 = [343,285,216,523,562,279,1	,289,125,78,381,178,282,475,184,415,512,179,140,62,105,816,55,659,37,214,170,451,147,220]
w7 = [557,5,75,447,473,19,289,1,250,363,620,449,221,389,129,458,295,429,288,338,370,573,237,378,291,317,125,179,202,501]
w8 = [0,246,195,399,437,234,125,250,1,191,371,213,163,350,200,300,410,184,40,184,141,714,96,586,158,102,131,378,210,270]
w9 = [334,358,288,586,625,353,78,363,191,1,355,146,353,540,249,460,589,167,195,29,102,893,132,735,74,265,246,527,197,170]
w10 = [84,617,562,572,609,604,381,620,371,355,1,210,473,557,552,377,719,203,333,380,276,1004,412,933,407,326,499,733,527,199]
w11 = [193,445,381,548,587,435,178,449,213,146,210,1,362,513,359,385,616,48,188,171,79,918,219,798,201,228,324,590,324,59]
w12 = [396,220,216,257,292,203,282,221,163,353,473,362,1,202,261,238,256,323,176,343,299,557,237,461,309,148,176,267,310,420]
w13 = [474,389,407,59,90,374,475,389,350,540,557,513,202,1,458,195,225,467,348,534,467,456,435,467,505,287,376,340,511,569]
w14 = [0,125,61,515,547,128,184,129,200,249,552,359,261,458,1,475,411,350,239,222,281,699,141,505,176,294,87,307,74,404]
w15 = [295,457,443,198,233,440,415,458,300,460,377,385,238,195,475,1,402,338,276,464,366,650,395,642,451,202,390,479,504,434]
w16 = [639,298,351,266,268,289,512,295,410,589,719,616,256,225,411,402,1,578,429,572,550,305,460,243,531,401,358,156,482,675]
w17 = [168,425,365,501,541,414,179,429,184,167,203,48,323,467,350,338,578,1,153,187,74,878,210,768,207,184,305,561,325,103]
w18 = [0,285,235,392,431,272,140,288,40,195,333,188,176,348,239,276,429,153,1,193,124,732,124,615,176,74,171,409,244,247]
w19 = [355,334,264,582,620,330,62,338,184,29,380,171,343,534,222,464,572,187,193,1,118,876,113,712,47,266,224,506,168,198]
w20 = [241,366,302,508,548,357,105,370,141,102,276,79,299,467,281,366,550,74,124,118,1,853,141,724,134,181,245,515,252,132]
w21 = [921,577,640,462,438,572,816,573,714,893,1004,918,557,456,699,650,305,878,732,876,853,1,763,268,833,697,657,398,772,977]
w22 = [365,232,165,486,523,226,55,237,96,132,412,219,237,435,141,395,460,210,124,113,141,763,1,605,73,195,115,396,124,0]
w23 = [856,382,452,503,500,384,659,378,586,735,933,798,461,467,505,642,243,768,615,712,724,268,605,1,666,607,490,210,577,0]
w24 = [374,287,217,555,593,283,37,291,158,74,407,201,309,505,176,451,531,207,176,47,134,833,73,666,1,250,179,460,126,236]
w25 = [252,314,277,327,367,299,214,317,	102,265,326,228,148,287,294,202,401,184,74,266,181,697,195,607,250,1,215,408,310,286]
w26 = [440,121,64,433,466,112,170,125,131,246,499,324,176,376,87,390,358,305,171,224,245,657,115,490,179,215,1,282,136,376]
w27 = [659,183,250,392,405,181,451,179,378,527,733,590,267,340,307,479,156,561,409,506,515,398,396,210,460,408,282,1,380,646]
w28 = [486,198,133,567,601,201,147,202,210,197,527,324,310,511,74,504,482,325,244,168,252,772,124,577,126,310,136,380,1,362]
w29= [207,496,431,603,642,488,220,501,270,170,199,59,420,569,404,434,675,103,247,198,132,977,267,855,236,286,376,646,362,1]

distances = {0:w0,1:w1,2:w2,3:w3,4:w4,5:w5,6:w6,7:w7,8:w8,9:w9,10:w10,11:w11,12:w12,13:w13,14:w14,15:w15,16:w16,17:w17,18:w18,19:w19,20:w20,21:w21,22:w22,23:w23,24:w24,25:w25,26:w26,27:w27,28:w28,29:w29}

capacity_trucks = 1000
cars = ['truck','truck','truck','truck','truck']
num_cars = len(cars)
frontier = "---------"

if __name__ == "__main__":

    # Constant that is an instance object 
    genetic_problem_instances = 10
    print("EXECUTING ", genetic_problem_instances, " INSTANCES ")
    VRP(genetic_problem_instances)
    