#!/usr/bin/python
#coding:UTF-8
import MySQLdb
from decimal import *
import sys
sys.path.append("..")
sys.path.append("../..")
import tmall_data_analyse.settings as settings
import imp
 
imp.reload(sys)
#sys.setdefaultencoding('utf-8')



def insertDetail(goods_code,goods_id,num,price,total):
	db = MySQLdb.connect(host=settings.DATABASES.get('default').get('HOST'),
						user=settings.DATABASES.get(
							'default').get('USER'),
						passwd=settings.DATABASES.get(
							'default').get('PASSWORD'),
						db=settings.DATABASES.get('default').get('NAME'),
						charset="utf8",
						local_infile=1)
	detail = db.cursor(MySQLdb.cursors.DictCursor)
	rate = 100
	if float(total) > 0 :
		rate = round((float(num) * float(price) / float(total)) *100,6)
	value=[goods_code,goods_id,num,rate]
	detail.execute('insert into bom_detail (product_name,goods_id,goods_count,rate) values(%s,%s,%s,%s)',value);
	db.commit();
	detail.close();
	db.close();


def getFieldsList():
	db = MySQLdb.connect(host=settings.DATABASES.get('default').get('HOST'),
						user=settings.DATABASES.get(
							'default').get('USER'),
						passwd=settings.DATABASES.get(
							'default').get('PASSWORD'),
						db=settings.DATABASES.get('default').get('NAME'),
						charset="utf8",
						local_infile=1)
	fields = db.cursor(MySQLdb.cursors.DictCursor)
	fields.execute("desc bom")
	data = fields.fetchall();
	lst = [];
	result = [];
	for row in data:
		lst.append(row["Field"])
	for i in range(3,len(lst)):
		result.append(lst[i])
	return result

def getPriceByGoodsId(goods_id):
	db = MySQLdb.connect(host=settings.DATABASES.get('default').get('HOST'),
						user=settings.DATABASES.get(
							'default').get('USER'),
						passwd=settings.DATABASES.get(
							'default').get('PASSWORD'),
						db=settings.DATABASES.get('default').get('NAME'),
						charset="utf8",
						local_infile=1)
	detail = db.cursor(MySQLdb.cursors.DictCursor)
	value=[goods_id]
	detail.execute('select price from t_bas_sku_price where sku_id =%s',value);
	if detail.rowcount ==0:
		 return "0"
	else:
		row = detail.fetchone();
		return row["price"]


def truncateDetail():
	db = MySQLdb.connect(host=settings.DATABASES.get('default').get('HOST'),
						user=settings.DATABASES.get(
							'default').get('USER'),
						passwd=settings.DATABASES.get(
							'default').get('PASSWORD'),
						db=settings.DATABASES.get('default').get('NAME'),
						charset="utf8",
						local_infile=1)
	detail = db.cursor(MySQLdb.cursors.DictCursor)
	detail.execute('TRUNCATE TABLE bom_detail')
	db.commit();
	detail.close();
	db.close();

db = MySQLdb.connect(host=settings.DATABASES.get('default').get('HOST'),
						user=settings.DATABASES.get(
							'default').get('USER'),
						passwd=settings.DATABASES.get(
							'default').get('PASSWORD'),
						db=settings.DATABASES.get('default').get('NAME'),
						charset="utf8",
						local_infile=1)
bom = db.cursor(MySQLdb.cursors.DictCursor)

try:
	truncateDetail()	
	bom.execute("select * from bom")
	bom_data = bom.fetchall();
	fields = getFieldsList();

	for row in bom_data:
		goods_code = row["product_name"]
		total = row["price"]
		for i in range(0,len(fields)):
			fieldname = fields[i]
			print(fieldname,goods_code)
			if None != row[fieldname]:
				goods_id = fieldname
				goods_num = row[fieldname]
				if goods_num !="" and goods_num is not None :
					price = getPriceByGoodsId(goods_id)
					print(fieldname, goods_code,"num:", goods_num,goods_id,price,total)
					insertDetail(goods_code,goods_id,goods_num,price,total);
			
except Exception as e:
	db.close()
	print("error: unable fetch data",e.args)
	raise

db.close();
print("search complete")
