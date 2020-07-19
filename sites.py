import numpy as np
import pandas as pd
from collections import  Counter
import xlrd
from machines import Machine
from products import Lot



class Site(object):
    def __init__(self,name,FDT,TT,Qtime,Htime):
        self.name = name
        self.FDT = FDT*60 #min
        self.TT = TT #S
        self.machines = []
        self.Qtime = Qtime*3600 #H
        self.Htime = Htime*3600 #H
        self.waiting_Lots_normal = []
        self.waiting_Lots_prime = []
        self.processing_Lots = []
    def load(self, new_machine):
        self.machines.append(new_machine)
        for i in range(len(self.machines[-1].products)):
            #print(len(self.machines[-1].products),self.machines[-1].products)
            if(self.machines[-1].products[i][0] == self.name):
                self.machines[-1].very_products.append(self.machines[-1].products[i][1])
        #print(self.machines[-1].name,self.machines[-1].very_products)
        return True
    # def run(self):
    #     for i in range(len(self.machines)):
    #         if(self.machines[i].check_status()):
    #             for j in range(len(self.waiting_Lots)):
    #                 if([self.name,waiting_Lots[-1].productID] in self.machines[i].products):
    def lot_in(self):
        for i in range(len(self.machines)):
            if(self.machines[i].cold_down_time <= 0):
                longest_stay_hour = 0
                index_of_the_lot = -1
                for i in range(len(self.waiting_Lots_prime)):
                    #print(self.waiting_Lots_prime[i].stay_S)
                    [index_of_the_lot,longest_stay_hour] = [index_of_the_lot,longest_stay_hour] if(self.waiting_Lots_prime[i].stay_S < longest_stay_hour) else [i,self.waiting_Lots_prime[i].stay_S]
                    # if(index_of_the_lot != -1):
                    #     print(self.name,longest_stay_hour,self.waiting_Lots_prime[index_of_the_lot].LotID)
                        
    def check(self,name): #check if the site contains certain machine that process this product
        list = []
        for i in range(len(self.machines)):
            list.append(self.machines[i].name)
        if(name in list):
            return True
        return False
            
