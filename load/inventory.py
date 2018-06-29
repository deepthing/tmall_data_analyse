#!/usr/bin/python

import MySQLdb
import sys
import imp
imp.reload(sys)
from decimal import *

#sys.setdefaultencoding('utf-8')
db = MySQLdb.connect("127.0.0.1","bsztz","bsztz","tmall");

goods = db.cursor(MySQLdb.cursors.DictCursor)

def update_inventroy(goods_id,period,opening,ending,order_num,order_amount,trans_num,trans_amount):
    global goods
    global db
    detail = goods
    diff = int(ending) - int(opening)
    value=[str(opening),str(ending), str(diff) ,str(order_num),round(order_amount,6),str(trans_num),round(trans_amount,6),goods_id,period]
    detail.execute('update t_goods_num_info set opening_inventory=%s,ending_inventory=%s,diff_inventory=%s, sale_out_number=%s,sale_out_amount=%s,trans_num=%s,trans_amount=%s where goods_id =%s and period=%s',value);
    db.commit();



def getInventory(goods_id,period):
    global goods
    fields = goods
    value =[goods_id,goods_id,period+'%%', goods_id,goods_id,period+'%%']
    sql = "select sum(opening) as opening, sum(ending) as ending from (select IFNULL(sum(init_total),0) as opening,0 as ending from load_inventory_info where goods_code=%s " \
        " and period =(select min(period) " \
        " from load_inventory_info where goods_code=%s and period like %s) union " \
        "select 0 , IFNULL(sum(final_total),0) from load_inventory_info where goods_code=%s " \
                " and period =(select max(period) " \
                " from load_inventory_info where goods_code=%s and period like %s) ) t "
    fields.execute(sql,value)
    if fields.rowcount ==0:
         return "0","0"
    else:
        row = fields.fetchone();
    return row["opening"], row["ending"] 



def getTranactionAmount(goods_id,period):
    global goods
    fields = goods
    value =[goods_id,period,goods_id]

    sql = "select IFNULL(sum(b.in_out_number),0) as order_num,IFNULL(sum(a.deal_amount),0) as order_amount" \
            " from t_transaction_group_info b left join t_tmall_group_bom_detail a"\
            " on b.order_id = a.order_id and a.goods_code = b.goods_code "\
            " where b.order_id in (select outter_order_id from load_transaction_info where goods_code =%s and SUBSTR(in_out_time FROM 1 FOR 7) = %s)" \
            " and b.goods_code = %s"

    fields.execute(sql,value)
    if fields.rowcount ==0:
        return "0"
    else:
        row = fields.fetchone();
        return row["order_num"],row["order_amount"]


def getTranactionNumber(goods_id,period):
    global goods
    fields = goods
    value =[goods_id,period+'%%',goods_id]

    sql = "select IFNULL(sum(b.in_out_number),0) as order_num,IFNULL(sum(a.deal_amount),0) as order_amount" \
        " from t_transaction_group_info b left join t_tmall_group_bom_detail a "\
        " on b.order_id = a.order_id and a.goods_code = b.goods_code "\
        " where a.order_id in (select order_id from t_tmall_bom_detail where goods_id =%s and period like %s)" \
        " and b.goods_code = %s"

    fields.execute(sql,value)
    if fields.rowcount ==0:
        return "0"
    else:
        row = fields.fetchone();
        return row["order_num"],row["order_amount"]



try:
    goods.execute("select * from t_goods_num_info")
    data = goods.fetchall();
    for row in data:
        goods_id = row["goods_id"]
        period  =row["period"]
        opening,ending = getInventory(goods_id,period)
        order_num,order_amount = getTranactionNumber(goods_id,period)
        trans_num,trans_amount = getTranactionAmount(goods_id,period)
        print(goods_id,period,opening,ending,order_num,order_amount,trans_num,trans_amount)

    update_inventroy(goods_id,period,opening,ending,order_num,order_amount,trans_num,trans_amount)
    db.close()
    print("inventory caculation complete")
except Exception as e:
    print(str(e))
    db.close()
    raise
    
