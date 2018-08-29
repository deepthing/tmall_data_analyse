#!/usr/bin/python
#coding:UTF-8
import MySQLdb
import sys 
from decimal import *
sys.path.append("..")
sys.path.append("../..")
import tmall_data_analyse.settings as settings

def getBomCodes():
    db = MySQLdb.connect(host=settings.DATABASES.get('default').get('HOST'),
                            user=settings.DATABASES.get(
                                'default').get('USER'),
                            passwd=settings.DATABASES.get(
                                'default').get('PASSWORD'),
                            db=settings.DATABASES.get('default').get('NAME'),
                            charset="utf8",
                            local_infile=1)
    data = db.cursor()
    data.execute('''SELECT column_name FROM information_schema.columns WHERE TABLE_SCHEMA = 'tmall' AND table_name = 'BOM';''')
    bomCodes = data.fetchall()
    codes =bomCodes[3:len(bomCodes)-4]
    print(codes)
    return codes

def getlackBoms():
    db = MySQLdb.connect(host=settings.DATABASES.get('default').get('HOST'),
                            user=settings.DATABASES.get(
                                'default').get('USER'),
                            passwd=settings.DATABASES.get(
                                'default').get('PASSWORD'),
                            db=settings.DATABASES.get('default').get('NAME'),
                            charset="utf8",
                            local_infile=1)
    data = db.cursor(MySQLdb.cursors.DictCursor)
    data.execute('''SELECT * FROM temp_product_info''')
    lackBoms = data.fetchall()
    db.commit()
    data.close()
    db.close()
    return lackBoms
    
codes = getBomCodes()
lackBoms = getlackBoms()
db = MySQLdb.connect(host=settings.DATABASES.get('default').get('HOST'),
                        user=settings.DATABASES.get(
                            'default').get('USER'),
                        passwd=settings.DATABASES.get(
                            'default').get('PASSWORD'),
                        db=settings.DATABASES.get('default').get('NAME'),
                        charset="utf8",
                        local_infile=1)
data = db.cursor(MySQLdb.cursors.DictCursor)
for row in lackBoms:
    strr = "insert into BOM (product_name,"+str(row['cargo_code'].upper())+") values('"+row['product_name']+"',"+str(row['num']) +");"
    print(strr)
    data.execute(strr)
    print(row['product_name'],row['cargo_code'],row['num'])
db.commit()
data.close()
db.close()

print('上传缺失bom数据完毕')