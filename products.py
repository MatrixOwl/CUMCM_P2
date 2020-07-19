# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from collections import  Counter
import xlrd


#整个系统开始运行的时间是5月1日 7:30

class Lot(object):
    def __init__(self,LotID,productID,version,oper,state,EQID,quantity,stay_hour,priority):
        self.all_sites = [0, 1200, 1300, 1400, 1800, 2200, 3200, 3300, 3400, 2401, 3402, 3600, 3800, 4200, 4300, 4400, 4800, 5200, 5300, 5400, 5800, 5900]
        self.LotID = LotID
        self.productID = productID
        self.version = version
        self.site = self.all_sites.index(oper)
        self.state = state
        self.EQID = EQID
        self.quantity = quantity
        self.stay_S = stay_hour*3600
        self.priority = priority
        self.process_time = 0
    def run(self):
        if(self.state == 'WAIT'):
            self.stay_S += 600
        if(self.state == 'RUN'):
            self.process_time += 600;
        return True



lots = []

data = xlrd.open_workbook('overall.xlsx')
table = data.sheets()[1]

for i in range(1,table.nrows):
    lots.append(Lot(table.cell(i,0).value,int(table.cell(i,1).value),table.cell(i,2).value,int(table.cell(i,3).value),table.cell(i,4).value,table.cell(i,5).value,int(table.cell(i,6).value),table.cell(i,7).value,table.cell(i,8).value))
table = data.sheets()[2]

for i in range(1,table.nrows):
    if(table.cell(i,0).value == 20180501):
        lots.append(Lot(table.cell(i,3).value,int(table.cell(i,1).value),0,0,'WAIT',0,int(table.cell(i,4).value),0,0))
    elif(table.cell(i,0).value == 20180502):
        lots.append(Lot(table.cell(i,3).value,int(table.cell(i,1).value),0,0,'WAIT',0,int(table.cell(i,4).value),-24,0))
    elif(table.cell(i,0).value == 20180503):
        lots.append(Lot(table.cell(i,3).value,int(table.cell(i,1).value),0,0,'WAIT',0,int(table.cell(i,4).value),-48,0))



