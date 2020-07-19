# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from collections import  Counter
import xlrd
from machines import Machine
from products import Lot
from sites import Site



machines = []
lots = []
sites = []

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
        #print(machines[len(machines)-1].name,machines[len(machines)-1].all_possible_sites,machines[len(machines)-1].products)



data = xlrd.open_workbook('overall.xlsx')
table = data.sheets()[1]
for i in range(1,table.nrows):
    lots.append(Lot(table.cell(i,0).value,int(table.cell(i,1).value),table.cell(i,2).value,int(table.cell(i,3).value),table.cell(i,4).value,table.cell(i,5).value,int(table.cell(i,6).value),table.cell(i,7).value,table.cell(i,8).value))

table = data.sheets()[2]
for i in range(1,table.nrows):
    if(table.cell(i,0).value == 20180501):
        lots.append(Lot(table.cell(i,3).value,int(table.cell(i,1).value),0,1200,'WAIT','XXXX',int(table.cell(i,4).value),0,0))
    elif(table.cell(i,0).value == 20180502):
        lots.append(Lot(table.cell(i,3).value,int(table.cell(i,1).value),0,1200,'WAIT','XXXX',int(table.cell(i,4).value),-24,0))
    elif(table.cell(i,0).value == 20180503):
        lots.append(Lot(table.cell(i,3).value,int(table.cell(i,1).value),0,1200,'WAIT','XXXX',int(table.cell(i,4).value),-48,0))


data = xlrd.open_workbook('overall.xlsx')
table = data.sheets()[3]
for i in range(1,table.nrows):
    sites.append(Site(int(table.cell(i,0).value),int(table.cell(i,2).value),int(table.cell(i,3).value),int(table.cell(i,4).value),int(table.cell(i,5).value)))


for i in range(len(machines)):  #随机分配机器
    machines[i].random_locate()
    sites[machines[i].site-1].load(machines[i])


    

for i in range(len(lots)):
    if(lots[i].state == 'RUN'):
        for j in range(len(machines)):
            if (machines[j].name == lots[i].EQID):
                machines[j].cold_down_time += (lots[i].quantity-1)*sites[lots[i].site-1].TT + sites[lots[i].site-1].FDT
                sites[lots[i].site-1].processing_Lots.append(i)
                lots[i].stay_S = 0
        # if(sites[lots[i].site-1].check(lots[i].EQID)):
        #     print('Yes')
        #     machines (lots[i].quantity-1)*sites[lots[i].site-1].TT + sites[lots[i].site-1].FDT
        # else:
        #     print('No')
    elif(lots[i].priority == 1):
        sites[lots[i].site-1].waiting_Lots_prime.append(i)
    else:
        sites[lots[i].site-1].waiting_Lots_normal.append(i)

PM_list = ['MSP300','ITO100','ITO200','WET900','WETB00','OVN200']
PM_time = [8,18,18,8,8,10]


for i in range(len(machines)):
    if(machines[i].name in PM_list):
        machines[i].cold_down_time += PM_time[PM_list.index(machines[i].name)]*3600


for t in range(9*24*6):
    for i in range(len(machines)): #update machine with time
        machines[i].run()
    for i in range(len(lots)): #update lots with time
        lots[i].run()
        if(lots[i].site <= 20 and lots[i].process_time>(lots[i].quantity-1)*sites[lots[i].site-1].TT + sites[lots[i].site-1].FDT):
            # out
            lots[i].state = 'WAIT'
            lots[i].process_time = 0
            lots[i].site += 1
            if(lots[i].priority == 1):
                sites[lots[i].site-1].waiting_Lots_prime.append(i)
            else:
                sites[lots[i].site-1].waiting_Lots_normal.append(i)
        if(lots[i].site == 21 and lots[i].process_time>(lots[i].quantity-1)*sites[lots[i].site-1].TT + sites[lots[i].site-1].FDT): #out
            lots[i].state = 'DONE'
            lots[i].process_time = 0
            for j in range(len(sites[20].processing_Lots)):
                if(lots[sites[20].processing_Lots[j]].state == 'DONE'):
                    sites[20].processing_Lots.remove(i)
                    break
    for i in range(len(sites)):
        for j in range(len(sites[i].machines)):
            if(sites[i].machines[j].cold_down_time <= 0):
                # print(sites[i].machines[j].very_products)
                longest_stay_hour = 0
                index_of_the_lot = -1
                for k in range(len(sites[i].waiting_Lots_prime)):
                    #print(self.waiting_Lots_prime[i].stay_S)
                    [index_of_the_lot,longest_stay_hour] = [index_of_the_lot,longest_stay_hour] if(lots[sites[i].waiting_Lots_prime[k]].stay_S < longest_stay_hour) else [k,lots[sites[i].waiting_Lots_prime[k]].stay_S]
                if(index_of_the_lot != -1 and lots[sites[i].waiting_Lots_prime[index_of_the_lot]].productID in sites[i].machines[j].very_products):
                    lots[sites[i].waiting_Lots_prime[index_of_the_lot]].state = 'RUN'
                    lots[sites[i].waiting_Lots_prime[index_of_the_lot]].stay_S = 0
                    lots[sites[i].waiting_Lots_prime[index_of_the_lot]].process_time = 0
                    lots[sites[i].waiting_Lots_prime[index_of_the_lot]].EQID = sites[i].machines[j].name
                    sites[i].machines[j].cold_down_time += (lots[sites[i].waiting_Lots_prime[k]].quantity-1)*sites[i].TT + sites[i].FDT
                    # print(index_of_the_lot,len(sites[i].waiting_Lots_prime))
                    del sites[i].waiting_Lots_prime[index_of_the_lot]
            if(sites[i].machines[j].cold_down_time <= 0):
                # print(sites[i].machines[j].very_products)
                longest_stay_hour = 0
                index_of_the_lot = -1
                for k in range(len(sites[i].waiting_Lots_normal)):
                    #print(self.waiting_Lots_normal[i].stay_S)
                    [index_of_the_lot,longest_stay_hour] = [index_of_the_lot,longest_stay_hour] if(lots[sites[i].waiting_Lots_normal[k]].stay_S < longest_stay_hour) else [k,lots[sites[i].waiting_Lots_normal[k]].stay_S]
                if(index_of_the_lot != -1 and lots[sites[i].waiting_Lots_normal[index_of_the_lot]].productID in sites[i].machines[j].very_products):
                    # print(sites[i].name,longest_stay_hour,lots[sites[i].waiting_Lots_normal[k]].LotID)
                    lots[sites[i].waiting_Lots_normal[k]].state = 'RUN'
                    lots[sites[i].waiting_Lots_normal[k]].stay_S = 0
                    lots[sites[i].waiting_Lots_normal[k]].process_time = 0
                    lots[sites[i].waiting_Lots_normal[k]].EQID = sites[i].machines[j].name
                    sites[i].machines[j].cold_down_time += (lots[sites[i].waiting_Lots_normal[k]].quantity-1)*sites[i].TT + sites[i].FDT
                    del sites[i].waiting_Lots_normal[index_of_the_lot]
    
    # print(len(sites[0].waiting_Lots_normal),len(sites[0].waiting_Lots_prime),len(sites[1].waiting_Lots_normal),len(sites[1].waiting_Lots_prime))

for i in range(len(sites)):
    print(sites[i].name,sites[i].waiting_Lots_normal,sites[i].waiting_Lots_prime)
count1 = 0
count2 = 0
count3 = 0
for i in range(len(lots)):
    if(lots[i].state == 'DONE'):
        count1 += 1
    if(lots[i].state == 'WAIT'):
        count2 += 1
    if(lots[i].state == 'RUN'):
        count3 += 1
print(count1,count2,count3)