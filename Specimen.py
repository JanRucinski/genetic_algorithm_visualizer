#a class responsible for a single specimen
import random

class Specimen:

    def __init__(self, target, mutation_chance = 0.001, cross_chance=1):
        self.rgb = []
        self.str_history = []

        self.strength = [0, 0, 0]

        self.rgb = [random.randrange(0,255), random.randrange(0,255), random.randrange(0,255)]
        pass

        self.mutationChance = mutation_chance
        self.crossChance = cross_chance

        if(target != 0):
            self.target = target
            self.add_to_history()
        pass

    def mutation(self, color):
        if(color>2 or color<0):
            print("invalid color idx | mutation")
            return
        mutated = toBase2(self.rgb[color])
        counter = 0
        for x in mutated:
            if (random.uniform(0, 1) <= self.mutationChance):
                if x == 1 :
                    mutated[counter] = 0
                else:
                    mutated[counter] = 1
            counter+=1

        self.rgb[color] = toBase10(mutated)
        # print(toBase10(mutated))
        pass

    def crossover(self, other_os, color): 
        if (random.uniform(0, 1) > self.crossChance):
            return

        crossed1 = toBase2(self.rgb[color])
        crossed2 = toBase2(other_os.rgb[color])

        result = []
        counter = 0
        for x in crossed1:
            if (random.uniform(0, 1) > 0.5):
                result.append(crossed1[counter])
            else:
                result.append(crossed2[counter])
            counter += 1

        fit1 = self.fitness(color)
        backup = self.rgb[color]

        self.rgb[color] = toBase10 (result)

        fit2 = self.fitness(color)

        if(fit2 >= fit1):
            self.rgb[color] = backup
            for x in range(3):
                self.strength[x] += 5
                if(self.strength[x]>255):
                    self.strength[x] = 255
        else:
            for x in range(3):
                if(self.strength[x]<255):
                    self.strength[x] -= abs(fit2 - fit1)
                    if(self.strength[x] < 0):
                        self.strength[x] = 0
            

        self.add_to_history()
        # print(0)
        pass

    def fitness(self, color): #todo
        return abs(self.target.rgb[color] - self.rgb[color])

    def getSumOfFitness(self):
        return self.fitness(0) + self.fitness(1) + self.fitness(2)

    def getToRgb(self):
        ret = []
        for x in self.rgb:
            ret.append(toBase2(x))
        return from_rgb(ret)

    def getToRgbStren(self):
        ret = []
        for x in self.strength:
            ret.append(toBase2(x))
        return from_rgb(ret)

    def negative_color(self):
        return negative_rgb(self.rgb)

    def rgb_to_string(self):
        return str(self.rgb[0]) + "," + str(self.rgb[1]) + "," + str(self.rgb[2])

    def add_to_history(self):
        self.str_history.append(self.rgb_to_string() + "| difference: " + str(self.getSumOfFitness()))

    def get_history(self):
        return self.str_history

    def copy(self):
        return Specimen(self.target, rand=False, mutation_chance=self.mutationChance, cross_chance=self.crossChance, rgb=self.rgb)

def toBase10(color):
    ret = 0
    i = 7
    for x in color:
        ret += x*(2**i)
        i -= 1
    return ret
    
def toBase2(ip_val):
    i = 0
    ret = []
    while(i<8):
        ret.append(ip_val % 2)
        ip_val = ip_val // 2
        i += 1
    ret.reverse()
    return ret
    
def from_rgb(rgb):
    rgb = tuple([toBase10(rgb[0]) , toBase10(rgb[1]) ,toBase10(rgb[2])])
    return "#%02x%02x%02x" % rgb

def negative_rgb(rgb):
    ret = []
    for x in rgb:
        ret.append(toBase2 (255 - x))
    return from_rgb(ret)