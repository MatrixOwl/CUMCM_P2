import random
from operator import itemgetter
import numpy as np




def build_init_pop_with_rules(Updata_num):
    """
    :param Updata_num: unmber of the update of equipments
    :return: init Gene
    """
    All_Gene = []
    for _ in range(Updata_num):
        Gene_data = []
        can_choose = [[1, 6], [2, 7, 14, 18], [5, 13], [9, 11, 15], [3, 8, 10, 19], [4, 12, 16, 20]]
        m_num = [9, 13, 13, 16, 11, 10]
        for i in range(6):
            for j in range(m_num[i]):
                rc = random.choice(can_choose[i])
                Gene_data.append(rc)
        All_Gene.append(Gene_data)

    return All_Gene


class Gene:
    def __init__(self, data):
        self.data = data  # is a N*78 matrix


##########


class GA:
    def __init__(self, parameter):
        """
        :param parameter: this is a list and it needs: crossPB, mutPB, NGEN, popSize, max, min, Update_num, Rules
        """
        self.parameter = parameter

        max = self.parameter[4]
        min = self.parameter[5]
        self.bound = []
        self.bound.append(min)
        self.bound.append(max)

        self.Update_num = parameter[6]
        self.Rules = parameter[7]

        pop = []
        for i in range(self.parameter[3]):

            data = build_init_pop_with_rules(self.Update_num)
            geneinfo = data

            fitness = self.evaluate(geneinfo)
            pop.append({'Gene': Gene(data=geneinfo), 'fitness': fitness})

        self.pop = pop
        self.bestindividual = self.selectBest(self.pop)

    def evaluate(self, geneinfo):
        """
        :param geneinfo: this is a list and it contain gene information
        :return: fitness
        """

        # HERE: we need a fitness function over here

        fitness = 0
        return fitness

    def selectBest(self, pop):
        """
        :param pop: this is a pop list
        :return: best one (like hunger games)
        """
        s_inds = sorted(pop, key=itemgetter('fitness'), reverse=True)
        return s_inds[0]

    def selection(self, individuals, k):
        """
        :param individuals: hunger game players
        :param k: how much individuals we choose
        :return: who we choose (sorry, but this is more like the hunger games)
        """
        s_inds = sorted(individuals, key=itemgetter('fitness'), reverse=True)
        sum_fits = sum(ind['fitness'] for ind in individuals)

        chosen = []
        for i in range(k):
            u = random.random() * sum_fits
            sum_ = 0
            for ind in s_inds:
                sum_ += ind['fitness']
                if sum_ >= u:
                    chosen.append(ind)
                    break
        chosen = sorted(chosen, key=itemgetter('fitness'))
        return chosen

    def crossoperate(self, offspring):
        """
        :param offspring: this is two Gene
        :return:Gene after crossover
        """
        dim = len(offspring[0]['Gene'].data[0])

        geninfo1 = offspring[0]['Gene'].data
        geninfo2 = offspring[1]['Gene'].data

        newoff1 = Gene(data=[])
        newoff2 = Gene(data=[])

        Rules = self.Rules

        Gene_temp1 = []
        Gene_temp2 = []
        for j in range(self.Update_num):
            geninfo1 = offspring[0]['Gene'].data[j]
            geninfo2 = offspring[1]['Gene'].data[j]
            temp1 = []
            temp2 = []
            '''
            for i in range(dim):
                if min(pos1, pos2) <= i < max(pos1, pos2):
                    temp1.append(geninfo1[i])
                    temp2.append(geninfo2[i])
                else:
                    temp1.append(geninfo2[i])
                    temp2.append(geninfo1[i])
            '''

            for Rule in Rules:
                pos1 = random.randrange(Rule[0], Rule[1])
                pos2 = random.randrange(Rule[0], Rule[1])
                for R in range(Rule[0], Rule[1]):
                    p = random.randrange(0, 1)
                    if min(pos1, pos2) <= R < max(pos1, pos2) and p <= self.parameter[0]:
                        temp1.append(geninfo2[R])
                        temp2.append(geninfo1[R])
                    else:
                        temp1.append(geninfo1[R])
                        temp2.append(geninfo2[R])

            Gene_temp1.append(temp1)
            Gene_temp2.append(temp2)

        newoff1.data = Gene_temp1
        newoff2.data = Gene_temp2

        return newoff1, newoff2

    def mutation(self, crossoff):
        """
        :param crossoff: this is one Gene
        :param bound:
        :return: Gene after mutation
        """
        dim = len(crossoff.data[0])

        pos_ = random.randrange(0, dim)

        for time_peace in range(self.Update_num):
            for Rule in self.Rules:
                for place in range(Rule[0], Rule[1]):
                    p = random.randrange(0, 1)
                    if p <= self.parameter[1]:
                        # pos = random.randrange(Rule[0], Rule[1])
                        replace = random.choice(Rule[2])
                        crossoff.data[time_peace][place] = replace

        # crossoff.data[pos] = random.random(bound[0][pos], bound[1][pos])

        return crossoff

    def GA_main(self):
        # :param parameter: this is a list and it needs: crossPB, mutPB, NGEN, popSize, max, min, Update_num, Rules
        crossPB = self.parameter[0]
        mutPB = self.parameter[1]
        NGEN = self.parameter[2]
        popSize = self.parameter[3]

        print('Let\'s start this fucking evolution!')

        for g in range(NGEN):
            print('------------------------- Generation {} ---------------------------------'.format(g))

            selectpop = self.selection(self.pop, popSize)
            nextoff = []
            while len(nextoff) != popSize:
                offspring = [selectpop.pop() for _ in range(2)]
                if random.random() < crossPB:
                    crossoff1, crossoff2 = self.crossoperate(offspring)
                    if random.random() < mutPB:
                        muteoff1 = self.mutation(crossoff1)
                        muteoff2 = self.mutation(crossoff2)
                        fit1 = self.evaluate(muteoff1)
                        fit2 = self.evaluate(muteoff2)
                        nextoff.append({'Gene': muteoff1, 'fitness': fit1})
                        nextoff.append({'Gene': muteoff2, 'fitness': fit2})
                    else:
                        fit1 = self.evaluate(crossoff1.data)
                        fit2 = self.evaluate(crossoff2.data)
                        nextoff.append({'Gene': crossoff1, 'fitness': fit1})
                        nextoff.append({'Gene': crossoff2, 'fitness': fit2})
                else:
                    nextoff.extend(offspring)

            self.pop = nextoff

            fits = [ind['fitness'] for ind in self.pop]
            best_ind = self.selectBest(self.pop)

            if best_ind['fitness'] > self.bestindividual['fitness']:
                self.bestindividual = best_ind

            print('Best individual found is {}, {}'.format(self.bestindividual['Gene'].data, self.bestindividual['fitness']))
            print('Max fitness of current pop: {}'.format(max(fits)))

        print('----------------END---------------------')


data = build_init_pop_with_rules(9)
g = Gene(data)
print(g.data)


'''
if __name__ == '__main__':
    #  :param parameter: this is a list and it needs: crossPB, mutPB, NGEN, popSize, max, min, Update_num, Rules
    ###########
    # bound is a leftover problem so it may useless for us but I think we should still keep it for a rainy day
    ###########
    parameter = []
    run = GA(parameter)
    run.GA_main()
'''