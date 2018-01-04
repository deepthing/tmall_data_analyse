#!/usr/bin/python
# coding:UTF-8
import sys
import service 
reload(sys)
sys.setdefaultencoding('utf-8')

# name = "2088021020858327_settledetails_201707_50002017070400032007000004493931.csv"
# print name[name.rfind("_")+1:name.rfind(".")]
# service.upzip("2017年7月.zip")

#service.loaddata("/Users/dengliang/Downloads/导入数据0104/12月份/")
# service.loaddata("/Users/dengliang/Downloads/201709/")
# service.loaddata("/Users/dengliang/Downloads/201710/")

service.analyse_data(0)
