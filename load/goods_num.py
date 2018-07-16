#!/usr/bin/python
#coding:UTF-8
import MySQLdb
import sys 
from decimal import *
import imp

imp.reload(sys)
sys.setdefaultencoding('utf-8')



def updatePrice(goods_code,period,fee_type,price):
        print(goods_code,period,fee_type,price)
        db = MySQLdb.connect("127.0.0.1","bsztz","bsztz","tmall",charset='utf8');
        detail = db.cursor(MySQLdb.cursors.DictCursor)

        value=[str(price),goods_code,fee_type]
        detail.execute('update t_period_nums_info set '+period+'=%s where goods_id=%s and fee_type=%s', value);
        db.commit();
        detail.close();
        db.close();

def createColumn(period):
    	print("period:"+period)
        db = MySQLdb.connect("127.0.0.1","bsztz","bsztz","tmall",charset='utf8')
        detail = db.cursor()
        detail.execute('ALTER TABLE t_period_nums_info ADD '+period+' DECIMAL(18,2)')


def getData(period):
	db = MySQLdb.connect("127.0.0.1","bsztz","bsztz","tmall",charset='utf8');
        detail = db.cursor(MySQLdb.cursors.DictCursor)
        value=[period]
        detail.execute('select goods_id,' \
		'sum(sale_num) as sale_num,' \
		'sum(sale_out_number*-1) as sale_out_number,' \
		'sum(order_deal_num) as order_deal_num,' \
		'sum(sale_amount) as sale_amount,' \
		'sum(sale_out_amount) as sale_out_amount,' \
		'sum(order_deal_amount) as order_deal_amount,' \
		'sum(opening_inventory) as opening_inventory,' \
		'sum(purchase_in) as purchase_in,' \
		'sum(other_in) as other_in,'
		'sum(trade_out) as trade_out,'\
		'sum(other_out) as other_out,'\
		'sum(ending_inventory) as ending_inventory ,'\
		'sum(diff_inventory) as diff_inventory,'\
		'sum(in_out_num) as in_out_num,'\
		'sum(trans_amount) as  trans_amount  '\
		' from t_goods_num_info where 1=1'\
		' and period =%s '\
		' group by goods_id',value);
	return detail;	

db = MySQLdb.connect("127.0.0.1","bsztz","bsztz","tmall",charset='utf8');
bom = db.cursor(MySQLdb.cursors.DictCursor)

try:
        bom.execute("select DISTINCT period,CONCAT('P',REPLACE(period,'-','')) as col_period from t_goods_num_info order by period")
        bom_data = bom.fetchall();
        for row in bom_data:
                period = row['period']
		col_period = row['col_period']
		createColumn(col_period)
		data_period = getData(period)

		for sub_row in data_period:
			goods_id = sub_row['goods_id']
			sale_num = sub_row['sale_num']
			sale_out_number = sub_row['sale_out_number']
			order_deal_num = sub_row['order_deal_num']
			sale_amount = sub_row['sale_amount']
			sale_out_amount = sub_row['sale_out_amount']
			order_deal_amount = sub_row['order_deal_amount']
			opening_inventory = sub_row['opening_inventory']
			purchase_in = sub_row['purchase_in']
			other_in = sub_row['other_in']
			trade_out = sub_row['trade_out']
			other_out = sub_row['other_out']
			ending_inventory = sub_row['ending_inventory']
			diff_inventory = sub_row['diff_inventory']
			in_out_num = sub_row['in_out_num']
			trans_amount = sub_row['trans_amount']
			
			
			updatePrice(goods_id,col_period,'sale_num',sale_num);
			updatePrice(goods_id,col_period,'sale_out_number',sale_out_number);
			updatePrice(goods_id,col_period,'order_deal_num',order_deal_num);
			updatePrice(goods_id,col_period,'sale_amount',sale_amount);
			updatePrice(goods_id,col_period,'sale_out_amount',sale_out_amount);
			updatePrice(goods_id,col_period,'order_deal_amount',order_deal_amount);
			updatePrice(goods_id,col_period,'opening_inventory',opening_inventory);
			updatePrice(goods_id,col_period,'purchase_in',purchase_in);
			updatePrice(goods_id,col_period,'other_in',other_in);
			updatePrice(goods_id,col_period,'trade_out',trade_out);
			updatePrice(goods_id,col_period,'other_out',other_out);
			updatePrice(goods_id,col_period,'ending_inventory',ending_inventory);
			updatePrice(goods_id,col_period,'diff_inventory',diff_inventory);
			updatePrice(goods_id,col_period,'in_out_num',in_out_num);
			updatePrice(goods_id,col_period,'trans_amount',trans_amount);

except Exception as e:
        print("error: unable fetch data",e.args)
		raise

db.close();
print("search complete")
