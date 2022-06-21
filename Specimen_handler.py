#a class responsible for handling a list of specimens
from Specimen import *
import random
import copy


class SpecimenHandler:
    def __init__(self, target = 0, mutation_chance = 0.001, cross_chance=1, population_size = 50):
        self.specimens = []
        self.start_specimens = []

        if (target != 0):
            self.target = target
        else:
            self.target = Specimen(0)

        self.mutation_chance = mutation_chance
        self.cross_chance = cross_chance
        self.population_size = population_size
        self.create_population()

    def add_specimen(self, specimen):
        self.specimens.append(specimen)


    def create_population(self):
        for x in range(self.population_size):
            self.add_specimen(Specimen(self.target, self.mutation_chance, self.cross_chance))
        
        for specimen in self.specimens:
            self.start_specimens.append(copy.deepcopy(specimen))


    def iterate(self):
        for specimen in self.specimens:
            second_specimen = specimen

            while (second_specimen == specimen):
                randIdx = random.randrange(self.population_size)
                second_specimen = self.specimens[randIdx]

            color_to_change = random.randrange(3)
            specimen.crossover(second_specimen, color_to_change)
            specimen.mutation(color_to_change)

    def get_best_specimen(self):
        best_specimen = self.specimens[0]
        for specimen in self.specimens:
            if (specimen.getSumOfFitness() < best_specimen.getSumOfFitness()):
                best_specimen = specimen
        return best_specimen

    def get_specimens(self):
        return self.specimens

    def get_start_specimens(self):
        return self.start_specimens

    def get_population_size(self):
        return self.population_size

    def write_history_of_found_to_file(self, filename):
        with open(filename, "w") as file:
            for line in self.get_best_specimen().get_history():
                file.write(line + "\n")