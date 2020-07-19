# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from collections import  Counter
import xlrd
from enum import Enum
import random


class Machine(object):
    def __init__(self,name,site):
        self.all_sites = [0, 1200, 1300, 1400, 1800, 2200, 3200, 3300, 3400, 2401, 3402, 3600, 3800, 4200, 4300, 4400, 4800, 5200, 5300, 5400, 5800, 5900]
        self.name = name
        self.site = self.all_sites.index(site)
        self.products = []
        self.all_possible_sites = []
        self.cold_down_time = 0
        self.switch_time = {'MSP': [5,2,0], 'ITO': [0,2,0], 'PHL': [20,15,10] ,'CVD': [360,2,0], 'DRY': [60,2,0], 'WET': [10,2,0],'STR': [10,2,0], 'OVN': [0,5,0]} #[不同站点间，同站点不同ID，同站点同ProductID不同版本] 单位分钟
        self.bar_chart = []
        self.very_products = []
    def site_push(self, new_site):
        self.all_possible_sites.append(new_site)
        return True
    def product_push(self,site_index,productID):
        self.products.append([site_index,productID])
        return True
    def move(self,time):
        self.cold_down_time += time
        return True
    def switch(self,case):
        self.cold_down_time += self.switch_time[self.name[:-3]][case]
    def check_status(self):
        if(self.cold_down_time > 0):
            return False
        return True
    def run(self):
        if(self.cold_down_time>0):
            self.cold_down_time -= 600
        if(self.cold_down_time <0):
            self.cold_down_time = 0;
    def random_locate(self):
        self.site = self.all_sites.index(random.choice(self.all_possible_sites))



machines = []

data = xlrd.open_workbook('machines.xlsx')
num_of_catagories = len(data.sheets())
for i in range(num_of_catagories):
    table = data.sheets()[i]
    num_of_rows = table.nrows
    num_of_cols = table.ncols
    #print(num_of_rows,num_of_cols)
    for i in range(2,num_of_cols): 
        machines.append(Machine(table.cell(0,i).value,0)) #以机器名称实例化Machine
        for j in range(num_of_rows):
            if(table.cell(j,i).value == 'Y'):
                machines[len(machines)-1].product_push(int(table.cell(j,0).value),int(table.cell(j,1).value))
                if(len(machines[-1].all_possible_sites)==0):
                    machines[len(machines)-1].all_possible_sites.append(int(table.cell(j,0).value))
                elif(machines[-1].all_possible_sites[-1] != table.cell(j,0).value):
                    machines[len(machines)-1].all_possible_sites.append(int(table.cell(j,0).value))
        # print(machines[len(machines)-1].name,machines[len(machines)-1].all_possible_sites,machines[len(machines)-1].products)


