# -*- coding: utf-8 -*-
import os
import sys
sys.path.append("..")
sys.path.append("../..")
import load_and_analyse.zip_util as zip
import tmall_data_analyse.settings as setting
import load_and_analyse.sql_templates as sql
import MySQLdb
import commands

# file_type = ['fee','inventory','myaccount','order','settlebatch','settledetails','settlefee','strade','tmallsodetails','tmallso','transaction']

def upzip(zipfilename):
    try:
        zip.extract(setting.BASE_FILE_PATH.get('upzip_path')+zipfilename,setting.BASE_FILE_PATH.get('upload_path'))
        os.rename(setting.BASE_FILE_PATH.get('upzip_path')+zipfilename,setting.BASE_FILE_PATH.get('backup_path')+zipfilename)
        return 'success'
    except Exception, e:
        print str(e)
        return 'false'

def loaddata(csvfilepath):
    if os.path.isdir(csvfilepath):
        os.chdir(csvfilepath)
        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                csvfilename = (os.path.join(csvfilepath,os.path.join(root, name))).replace("./","")
                #print csvfilename
                #print name
                db = MySQLdb.connect(setting.DATABASES.get('default').get('HOST'),
                    setting.DATABASES.get('default').get('USER'),
                    setting.DATABASES.get('default').get('PASSWORD'),
                    setting.DATABASES.get('default').get('NAME'),
                    charset='utf8')
                data = db.cursor(MySQLdb.cursors.DictCursor)

                load_data_to_db(db,data,csvfilename,name.lower())

                db.commit();
                data.close();
                db.close();

        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                os.remove((os.path.join(csvfilepath,os.path.join(root, name))).replace("./",""))
            for name in dirs:
                os.removedirs((os.path.join(csvfilepath,os.path.join(root, name))).replace("./",""))
                
    else:
        return

def load_data_to_db(db,data,filename,name):

    strr = ''
    if '.csv' in name:
        if 'settlefee' in name:
            strr = sql.sql_templates.type_settlefee
            strr = strr.replace("@templates_cut",""+name[name.rfind(".")-6:name.rfind(".")])
        elif 'inventory' in name:
            strr = sql.sql_templates.type_inventory
        elif 'myaccount' in name:
            strr = sql.sql_templates.type_myaccount
        elif 'order' in name:
            strr = sql.sql_templates.type_order
        elif 'settlebatch' in name:
            strr = sql.sql_templates.type_settlebatch
        elif 'settledetails' in name:
            strr = sql.sql_templates.type_settledetails
            strr = strr.replace("@templates_cut",""+name[name.rfind("_")+1:name.rfind(".")])
        elif 'fee' in name:
            strr = sql.sql_templates.type_fee
            strr = strr.replace("@templates_fee_date",name[3:7]+"-"+name[7:9]+"-01")
        elif 'strade' in name:
            strr = sql.sql_templates.type_strade
        elif 'tmallsodetails' in name:
            strr = sql.sql_templates.type_tmallsodetail
        elif 'tmallso' in  name:
            strr = sql.sql_templates.type_tmallso
        elif 'transaction' in name:
            strr = sql.sql_templates.tpye_transaction

    if strr != '':
        strr = strr.replace("@templates_filename",filename)
        print strr
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
    sql = "".join(["mysql -ubsztz -pbsztz tmall < ",name])
    print "commend",sql

    commands.getstatusoutput(sql)


def analyse_data(num):
    try:
        if(num ==0 or num == 1):
            print "初始化&&更新BOM信息表"
            execsql("load_and_analyse/sql/init.sql")
            execfile("load_and_analyse/bom.py")
            execfile("load_and_analyse/bom_price.py")
        if(num ==0 or num == 2):
            print "订单数量分析 - 状态分析"
            execsql("load_and_analyse/sql/t_order_analyse.sql")
        if(num ==0 or num == 3):
            print "订单数量分析 - 账号分析"
            execsql("load_and_analyse/sql/t_buyer_info.sql")
        if(num ==0 or num == 4):
            print "订单数量分析 - 区域分析"
            execsql("load_and_analyse/sql/t_order_area.sql")
        if(num ==0 or num == 5):
            print "订单金额分析 - 订单金额"
            execsql("load_and_analyse/sql/t_group_strade_info.sql")
            execsql("load_and_analyse/sql/t_order_amount.sql")
        if(num ==0 or num == 6):
           print "订单金额分析 - 订单费用"
           execsql("load_and_analyse/sql/t_fee_info.sql")
        if(num ==0 or num == 7):
            print "订单金额分析 - 月份金额"
            execsql("load_and_analyse/sql/t_monthly_order_amount.sql")
        if(num ==0 or num == 8):
            print "订单金额分析 - 月份费用"
            execsql("load_and_analyse/sql/t_fee_monthly_info.sql")
        if(num ==0 or num == 9):
            print "bom更新"
            execsql("load_and_analyse/sql/temp_product_info.sql")
            execfile("load_and_analyse/bom_update.py")
        if(num ==0 or num == 10):
            print "库存数量分析"
            execsql("load_and_analyse/sql/t_good_num_info.sql")
            execfile("load_and_analyse/inventory.py")
        if(num ==0 or num == 11):
            print "订单提取时间 - 金额统计"
            execsql("load_and_analyse/sql/t_settle_amount_info.sql")
        if(num ==0 or num == 12):
            print "订单提取时间 - 费用明细"
            execsql("load_and_analyse/sql/t_settle_fee_info.sql")
        if(num ==0 or num == 13):
            print "我的账户支出"
            execsql("load_and_analyse/sql/t_myaccount_monthly_info.sql")
        if(num ==0 or num == 14):
            print "库存数量分析 - 行转列"
            execsql("load_and_analyse/sql/init_t_period_num_info.sql")
            execfile("load_and_analyse/goods_num.py")
        
        print '执行完毕'
    except Exception,e:
        print str(e)

    
