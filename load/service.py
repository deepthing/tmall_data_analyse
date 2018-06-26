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
            #print(name)
            #print(name[dateIndex:dateIndex+4]+"_"+name[dateIndex+4:dateIndex+6])
            models.LoadInventoryInfo.objects.filter(period__contains=name[dateIndex:dateIndex+4]+"-"+name[dateIndex+4:dateIndex+6]).delete()

            strr = sql.sql_templates.type_inventory
        elif 'myaccount' in name:
            
            startDate = datetime.date(int(name[dateIndex:dateIndex+4]),int(name[dateIndex+4:dateIndex+6]),1)
            if int(name[dateIndex+4:dateIndex+6])<=11:
                endDate = datetime.date(int(name[dateIndex:dateIndex+4]),int(name[dateIndex+4:dateIndex+6])+1,1)
            else:
                endDate = datetime.date(int(name[dateIndex:dateIndex+4])+1,1,1) 
            print(startDate,endDate)
            models.LoadMyaccountInfo.objects.filter(trans_date__range=(startDate,endDate)).delete()
            
            strr = sql.sql_templates.type_myaccount
        elif 'order' in name:
            strr = sql.sql_templates.type_order
        elif 'settlebatch' in name:
            strr = sql.sql_templates.type_settlebatch
        elif 'settledetail' in name:
            strr = sql.sql_templates.type_settledetails
            print(name+" get date:"+name[name.rfind("_")+1:name.rfind(".")])
            strr = strr.replace("@templates_cut",""+name[name.rfind("_")+1:name.rfind(".")])
        elif ('fee' in name) and ('settlefee' not in name):
            strr = sql.sql_templates.type_fee
            print(name+" get date:"+name[4:8]+"-"+name[8:10]+"-01")
            strr = strr.replace("@templates_fee_date",name[4:8]+"-"+name[8:10]+"-01")
        elif 'strade' in name:
            strr = sql.sql_templates.type_strade
        elif 'tmallsodetails' in name:
            strr = sql.sql_templates.type_tmallsodetail
        elif ('tmallso' in  name) and ('tmallsodetails' not in name):
            strr = sql.sql_templates.type_tmallso
        elif 'transaction' in name:
            strr = sql.sql_templates.tpye_transaction

    if strr != '':
        strr = strr.replace("@templates_filename",filename)
        print(filename)
        print(strr)
        data.execute(strr)

def readfile(name):
    file = open(name)
    strr = ""
    try:
        strr = file.read()
    finally:
        file.close()
    return str(strr)

def execsql(name):
    sql = "".join(["mysql -u bsztz -pbsztz tmall> ",name])
    print("commend",sql)

    subprocess.getstatusoutput(sql)


def analyse_data(num):
    try:
        print("开始执行")
        exec(compile(open("load_and_analyse/inventory.py").read(), "load_and_analyse/inventory.py", 'exec'))
        print('执行完毕')
    except Exception as e:
        print(str(e))

    
