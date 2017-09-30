#!/usr/bin/python
# coding:UTF-8
import sys
sys.path.append("..")
import service 
reload(sys)
sys.setdefaultencoding('utf-8')

name = "2088021020858327_settledetails_201707_50002017070400032007000004493931.csv"
print name[name.rfind("_")+1:name.rfind(".")]
# service.upzip("2017年7月.zip")

# service.loaddata("/data/graceland/upload/2017年7月/")

service.analyse_data(0)
