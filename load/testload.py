#!/usr/bin/python
# coding:UTF-8
import sys
import service 
reload(sys)
sys.setdefaultencoding('utf-8')

# name = "2088021020858327_settledetails_201707_50002017070400032007000004493931.csv"
# print name[name.rfind("_")+1:name.rfind(".")]
# service.upzip("201801.zip")

#service.readcsv("/Users/dengliang/work/tmall/201804/fee_201804.csv")
service.loaddata("/Users/dengliang/work/tmall/tmall_data_analyse/upload/")
# service.loaddata("/Users/dengliang/Downloads/201710/")

# service.loaddata("C:/Users/alooyang/Desktop/2018")

# service.analyse_data(0)
