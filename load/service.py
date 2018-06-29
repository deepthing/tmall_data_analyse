# -*- coding: utf-8 -*-
import os
import sys
sys.path.append("..")
sys.path.append("../..")
import tmall_data_analyse.settings as setting
import MySQLdb
import subprocess

from . import sql_templates as sql
from . import zip_util as zip
import csv
import vis.models as models
import datetime
import tmall_data_analyse.settings as settings

num_process = 0

# file_type = ['fee','inventory','myaccount','order','settlebatch','settledetails','settlefee','strade','tmallsodetails','tmallso','transaction']

def upzip(zipfilename):
    try:
        zip.extract(setting.BASE_FILE_PATH.get('upzip_path')+zipfilename,setting.BASE_FILE_PATH.get('upload_path'))
        os.rename(setting.BASE_FILE_PATH.get('upzip_path')+zipfilename,setting.BASE_FILE_PATH.get('backup_path')+zipfilename)
        return 'success'
    except Exception as e:
        print(str(e))
        return 'false'

def readcsv(csvfilename):
    try:
        with open(csvfilename,newline='',encoding='utf-8') as f:
            reader = csv.reader(f)
            returnlist = []
            for row in reader:
                #print(row)
                returnlist.append(row)
            return returnlist
    except UnicodeDecodeError as identifier:
        try:
            with open(csvfilename,newline='',encoding='GB2312') as f:
                reader = csv.reader(f)
                returnlist = []
                for row in reader:
                    #print(row)
                    returnlist.append(row)
                return returnlist
        except UnicodeDecodeError as identifier:
            with open(csvfilename,newline='',encoding='GBK') as f:
                reader = csv.reader(f)
                returnlist = []
                for row in reader:
                    #print(row)
                    returnlist.append(row)
                return returnlist    
    

def loaddata(csvfilepath):
    if os.path.isdir(csvfilepath):
        os.chdir(csvfilepath)
        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                
                csvfilename = (os.path.join(csvfilepath,os.path.join(root, name))).replace("./","")
                csvfilename = csvfilename.replace(".\\","")
                csvfilename = csvfilename.replace("\\","/")
                print (csvfilename)
                print (name)
                db = MySQLdb.connect(setting.DATABASES.get('default').get('HOST'),
                    setting.DATABASES.get('default').get('USER'),
                    setting.DATABASES.get('default').get('PASSWORD'),
                    setting.DATABASES.get('default').get('NAME'),
                    charset='utf8')
                data = db.cursor(MySQLdb.cursors.DictCursor)

                load_data_to_db(db,data,csvfilename,name.lower())

                db.commit()
                data.close()
                db.close()

        # for root, dirs, files in os.walk(".", topdown=False):
        #     for name in files:
        #         os.remove((os.path.join(csvfilepath,os.path.join(root, name))).replace("./",""))
        #     for name in dirs:
        #         os.removedirs((os.path.join(csvfilepath,os.path.join(root, name))).replace("./",""))
                
    else:
        return

def load_csv_file(csvfilename,name):
    csvfilename = csvfilename.replace(".\\","")
    csvfilename = csvfilename.replace("\\","/")
    print (csvfilename)
    db = MySQLdb.connect(host = setting.DATABASES.get('default').get('HOST'),
        user = setting.DATABASES.get('default').get('USER'),
        passwd = setting.DATABASES.get('default').get('PASSWORD'),
        db = setting.DATABASES.get('default').get('NAME'),
        local_infile = 1)
    data = db.cursor(MySQLdb.cursors.DictCursor)

    load_data_to_db(db,data,csvfilename,name.lower())

    db.commit()
    data.close()
    db.close()

def load_data_to_db(db,data,filename,name):

    strr = ''
    if '.csv' in name:
        dateIndex =name.rfind("_")+1
        print(name)
        print("当前年:"+name[dateIndex:dateIndex+4])
        print("当前月:"+name[dateIndex+4:dateIndex+6])
        if 'settlefee' in name:
            strr = sql.sql_templates.type_settlefee
            print(name+" get date:"+name[name.rfind(".")-6:name.rfind(".")])
            model_filter = models.LoadSettlefeeInfo.objects.filter(settle_time=name[dateIndex:dateIndex+6]).delete()
            #print(len(model_filter))
            strr = strr.replace("@templates_cut",""+name[dateIndex:dateIndex+6])
        elif 'inventory' in name:
            models.LoadInventoryInfo.objects.filter(period__contains=name[dateIndex:dateIndex+4]+"-"+name[dateIndex+4:dateIndex+6]).delete()
            strr = sql.sql_templates.type_inventory
        elif 'myaccount' in name:
            models.LoadMyaccountInfo.objects.filter(trans_date__range=(getStartAndEndDate(name))).delete()
            strr = sql.sql_templates.type_myaccount
        elif 'order' in name:
            models.LoadOrderInfo.objects.filter(order_time__contains=name[dateIndex:dateIndex+4]+"-"+name[dateIndex+4:dateIndex+6]).delete()
            strr = sql.sql_templates.type_order
        elif 'settlebatch' in name:
            print(getStartAndEndDate(name))
            models.LoadSettlebatchInfo.objects.filter(settle_date__range=(getStartAndEndDate(name))).delete()
            strr = sql.sql_templates.type_settlebatch
        elif 'settledetail' in name:
            models.LoadSettledetailsInfo.objects.filter(settlement_time__range=(getStartAndEndDate(name))).delete()
            strr = sql.sql_templates.type_settledetails
            print(name+" get date:"+name[name.rfind("_")+1:name.rfind(".")])
            strr = strr.replace("@templates_cut",""+name[name.rfind("_")+1:name.rfind(".")])
        elif ('fee' in name) and ('settlefee' not in name):
            models.LoadFeeInfo.objects.filter(fee_date__contains=name[dateIndex:dateIndex+4]+"-"+name[dateIndex+4:dateIndex+6]).delete()
            strr = sql.sql_templates.type_fee
            print(name+" get date:"+name[4:8]+"-"+name[8:10]+"-01")
            strr = strr.replace("@templates_fee_date",name[4:8]+"-"+name[8:10]+"-01")
        elif 'strade' in name:
            models.LoadStradeInfo.objects.filter(payment_time__range=(getStartAndEndDate(name))).delete()
            strr = sql.sql_templates.type_strade
        elif 'tmallsodetails' in name:
            models.LoadTmallsodetailInfo.objects.filter(order_create_time__range=(getStartAndEndDate(name))).delete()
            models.LoadTmallsodetailInfo.objects.filter(order_create_time = None).delete()
            strr = sql.sql_templates.type_tmallsodetail
        elif ('tmallso' in  name) and ('tmallsodetails' not in name):
            models.LoadTmallsoInfo.objects.filter(create_time__contains=name[dateIndex:dateIndex+4]+"-"+name[dateIndex+4:dateIndex+6]).delete()
            strr = sql.sql_templates.type_tmallso
        elif 'transaction' in name:
            models.LoadTransactionInfo.objects.filter(in_out_time__contains=name[dateIndex:dateIndex+4]+"-"+name[dateIndex+4:dateIndex+6]).delete()
            strr = sql.sql_templates.tpye_transaction

    if strr != '':
        strr = strr.replace("@templates_filename",filename)
        print(filename)
        print(strr)
        data.execute(strr)

def getStartAndEndDate(name):
    dateIndex =name.find("_")+1
    startDate = datetime.date(int(name[dateIndex:dateIndex+4]),int(name[dateIndex+4:dateIndex+6]),1)
    if int(name[dateIndex+4:dateIndex+6])<=11:
        endDate = datetime.date(int(name[dateIndex:dateIndex+4]),int(name[dateIndex+4:dateIndex+6])+1,1)
    else:
        endDate = datetime.date(int(name[dateIndex:dateIndex+4])+1,1,1) 
    print(startDate,endDate) 
    return startDate,endDate


def readfile(name):
    file = open(name)
    strr = ""
    try:
        strr = file.read()
        #print(strr)
    finally:
        file.close()
    return str(strr)

def execsql(sqlfile):
    db = MySQLdb.connect(host = setting.DATABASES.get('default').get('HOST'),
    user = setting.DATABASES.get('default').get('USER'),
    passwd = setting.DATABASES.get('default').get('PASSWORD'),
    db = setting.DATABASES.get('default').get('NAME'),
    local_infile = 1)
    data = db.cursor(MySQLdb.cursors.DictCursor)

    data.executemany(readfile(sqlfile),"")

    db.commit()
    data.close()
    db.close()

def execfile(filename):
    exec(open(filename).read())




def analyse_data():
    global num_process
    try:
        print("开始执行")
        num_process = 0
        print("1:初始化")
        execsql(os.path.join(settings.BASE_DIR,"load/sql/init.sql"))
        num_process = 5
        execsql(os.path.join(settings.BASE_DIR,"load/sql/init2.sql"))
        num_process = 10
        print("1:初始化，完成")
        
        print("2:计算myaccount的各项费用明细")
        execsql(os.path.join(settings.BASE_DIR,"load/sql/t_other_fee_info2.sql"))
        num_process = 20
        print("3:找BOM缺失并补充")
        execsql(os.path.join(settings.BASE_DIR,"load/sql/bom.sql"))
        num_process = 30
        print("4:BOM金额计算")
        execfile(os.path.join(settings.BASE_DIR,"load/bom_price.py"))
        num_process = 35
        execfile(os.path.join(settings.BASE_DIR,"load/bom.py"))
        num_process = 40
        print("5:计算货品库存数量和金额")
        execsql(os.path.join(settings.BASE_DIR,"load/sql/t_good_num_info.sql"))
        num_process = 50
        execfile(os.path.join(settings.BASE_DIR,"load/inventory.py"))
        num_process = 70
        print("6:验证BOM分解数据和菜鸟数据是否一致，并修正BOM回到节点4")
        execsql(os.path.join(settings.BASE_DIR,"load/sql/bom2.sql"))
        num_process = 75
        print("7:计算每个自然期间的提取金额和税率")
        execsql(os.path.join(settings.BASE_DIR,"load/sql/t_settle_amount_info.sql"))
        num_process = 80
        execsql(os.path.join(settings.BASE_DIR,"load/sql/rate.sql"))
        num_process = 90
        print("8:生成每个自然期间的订单五大费用明细")
        execsql(os.path.join(settings.BASE_DIR,"load/sql/t_fee_info.sql"))
        num_process = 100
        
        print('执行完毕')
    except Exception as e:
        raise

def analyse_data_process():
    global num_process
    return num_process
    
    
