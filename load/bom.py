#!/usr/bin/python
#coding:UTF-8
import MySQLdb
from decimal import *
import sys
 
reload(sys)
sys.setdefaultencoding('utf-8')



def insertDetail(goods_code,goods_id,num,price,total):
	
	db = MySQLdb.connect("127.0.0.1","root","bsztz","tmall",charset='utf8');
	detail = db.cursor(MySQLdb.cursors.DictCursor)
	rate = 0
	if float(total) > 0 :
		rate = (float(num) * float(price) / float(total)) *100

	value=[goods_code,goods_id,num,rate]
	detail.execute('insert into bom_detail (product_name,goods_id,goods_count,rate) values(%s,%s,%s,%s)',value);
	db.commit();
	detail.close();
	db.close();


def getFieldsList():
	db = MySQLdb.connect("127.0.0.1","root","bsztz","tmall",charset='utf8');
        fields = db.cursor(MySQLdb.cursors.DictCursor)
	fields.execute("desc BOM")
	data = fields.fetchall();
        lst = [];
	result = [];
        for row in data:
                lst.append(row["Field"])
        for i in range(3,len(lst)):
                result.append(lst[i])
	return result

def getPriceByGoodsId(goods_id):
	db = MySQLdb.connect("127.0.0.1","root","bsztz","tmall",charset='utf8');
        detail = db.cursor(MySQLdb.cursors.DictCursor)
        value=[goods_id]
        detail.execute('select price from t_bas_sku_price where sku_id =%s',value);
        if detail.rowcount ==0:
                 return "0"
        else:
                row = detail.fetchone();
                return row["price"]


def truncateDetail():
        db = MySQLdb.connect("127.0.0.1","root","bsztz","tmall",charset='utf8');
        detail = db.cursor(MySQLdb.cursors.DictCursor)
	detail.execute('TRUNCATE TABLE bom_detail')
        db.commit();
        detail.close();
        db.close();

db = MySQLdb.connect("127.0.0.1","root","bsztz","tmall",charset='utf8');
bom = db.cursor(MySQLdb.cursors.DictCursor)

try:
	truncateDetail()	
        bom.execute("select * from BOM")
        bom_data = bom.fetchall();
	fields = getFieldsList();

        for row in bom_data:
		goods_code = row["product_name"].decode('utf-8')
		total = row["price"]
		for i in range(0,len(fields)):
			fieldname = fields[i]
			print fieldname,goods_code
			if None <> row[fieldname]:
				goods_id = fieldname
				goods_num = row[fieldname]
				if goods_num <>"" and goods_num is not None:
					price = getPriceByGoodsId(goods_id)
					print fieldname, goods_code,"num:", goods_num,goods_id,price,total
					insertDetail(goods_code,goods_id,goods_num,price,total);
			
except Exception,e:
        print "error: unable fetch data",e.args

db.close();
print "search complete"
