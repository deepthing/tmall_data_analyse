# -*- coding: utf-8 -*-
import os
import sys
sys.path.append("..")
import load_and_analyse.zip_util as zip
import tmall_data_analyse.settings as setting
import load_and_analyse.sql_templates as sql
import MySQLdb

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

